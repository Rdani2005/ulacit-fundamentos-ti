"""File-backed JSON repository for product inventory change records.

This module provides a concrete implementation of the repository pattern for
:class:`history.entity.product_changes.ProductChanges` entities using a single
JSON file as the persistence store.

Behavior Overview:
    - The repository overwrites the entire file on every save operation
      (:meth:`save_all`), treating the file as the canonical list of change
      records.
    - Reads are performed eagerly: :meth:`get_all` loads the full file into
      memory and returns a list of deserialized :class:`ProductChanges`.
    - Lookup, update, and delete operations are implemented in terms of
      :meth:`get_all`, then persisted back via :meth:`save_all`.

Design Notes:
    - This implementation is best suited for small/medium datasets or
      development/testing scenarios. For high write concurrency or large
      datasets, prefer a database-backed repository.
    - Operations are **not** atomic and there is no file locking; concurrent
      writers may race. If you need robustness, introduce OS-level locking
      or transactional storage.
    - Serialized datetimes use ISO 8601 strings (``datetime.isoformat``) and
      are parsed with ``datetime.fromisoformat`` (see parser class).

Error Handling:
    - If the file does not exist, :meth:`get_all` returns an empty list.
    - Low-level I/O and JSON parsing exceptions (e.g., :class:`OSError`,
      :class:`json.JSONDecodeError`) are allowed to propagate to the caller.
      Wrap calls in your application layer if you prefer custom error handling.
"""

from typing import Optional, List

from domain.repository.domain_repository import DomainRepository
from history.value_object.product_changes_id import ProductChangesId
from history.entity.product_changes import ProductChanges, ProductChangesParser

import json
import os

class ProductChangesRepository(DomainRepository[ProductChangesId, ProductChanges]):
    """JSON file–backed repository for :class:`ProductChanges`.

    This concrete repository expects the base class constructor to receive a
    ``filename`` (path to the JSON file). Each method reads/writes that file.

    Schema:
        The on-disk representation is a JSON array of objects produced by
        :meth:`ProductChangesParser.from_product_changes_to_dict`. Unicode is
        preserved (``ensure_ascii=False``).

    Example:
        >>> repo = ProductChangesRepository("changes.json")  # doctest: +SKIP
        >>> repo.save_all([])  # Persist an empty list                  # doctest: +SKIP
        >>> repo.get_all()                                             # doctest: +SKIP
        []
    """
    def save_all(self, entities: List[ProductChanges]) -> None:
        """Persist the full collection of change records to disk.

        The file is overwritten atomically from the perspective of this process
        (open → write → close). There is no inter-process locking.

        Args:
            entities: The list of :class:`ProductChanges` to serialize.

        Raises:
            OSError: If the file cannot be opened or written.
            TypeError: If an entity cannot be serialized by the parser.
        """
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(
                [ProductChangesParser.from_product_changes_to_dict(c) for c in entities],
                f,
                indent=4,
                ensure_ascii=False,
            )

    def get_all(self) -> List[ProductChanges]:
        """Load and return all change records from disk.

        If the file does not exist, an empty list is returned.

        Returns:
            A list of :class:`ProductChanges` instances.

        Raises:
            OSError: If the file exists but cannot be opened.
            json.JSONDecodeError: If the file contents are not valid JSON.
            KeyError/ValueError: If a record cannot be parsed by the parser.
        """
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [ProductChangesParser.from_dict_to_product_changes(d) for d in data]

    def get_by_id(self, id: ProductChangesId) -> Optional[ProductChanges]:
        """Find a change record by its identifier.

        Args:
            id: The typed identifier of the desired change record.

        Returns:
            The matching :class:`ProductChanges` if found; otherwise ``None``.

        Notes:
            This implementation performs a linear scan over all records.
            For large datasets or frequent lookups, consider indexing or a
            database-backed repository.
        """
        product_changes = self.get_all()
        for p in product_changes:
            if p.get_id().get_value() == id.get_value():
                return p
        return None

    def update(self, entity: ProductChanges) -> None:
        """Update an existing change record with the same identifier.

        The first record whose id equals ``entity.get_id()`` is replaced by
        ``entity``. If no record exists, the method is a no-op.

        Args:
            entity: The updated :class:`ProductChanges` instance to persist.

        Raises:
            OSError: If saving the updated collection fails.
        """
        changes = self.get_all()
        updated = False

        for i, c in enumerate(changes):
            if c.get_id() == entity.get_id():
                changes[i] = entity
                updated = True
                break

        if updated:
            self.save_all(changes)


    def delete(self, id: ProductChangesId) -> None:
        """Delete a change record by its identifier.

        If the identifier does not exist, the method is a no-op.

        Args:
            id: The typed identifier of the record to remove.

        Raises:
            OSError: If saving the updated collection fails.
        """
        changes = self.get_all()
        filtered = [c for c in changes if c.get_id() != id]

        if len(filtered) != len(changes):
            self.save_all(filtered)
