"""Inventory change record and (de)serialization helpers.

This module defines:

- :class:`ProductChanges`: a domain entity that records a single change
  to a product's inventory state (e.g., stock increase/decrease), including
  metadata such as type, timestamp, reason, and acting user.
- :class:`ProductChangesParser`: utilities to convert between the entity and a
  plain-JSON-serializable ``dict`` representation.

Typical use:
    - Persist a list of changes to a JSON file using a repository.
    - Rehydrate change records from JSON (e.g., during application startup).
    - Audit inventory adjustments over time.

"""

from datetime import datetime

from domain.entity.domain_enitty import DomainEntity
from history.value_object.product_changes_id import ProductChangesId
from products.value_object.product_id import ProductId


class ProductChanges(DomainEntity[ProductChangesId]):
    """Domain entity representing a single inventory change for a product.

    Each instance captures the kind of change, when it happened, how many units
    were affected, the reason, who performed it, and which product it refers to.

    Attributes:
        id: Typed unique identifier for this change record.
        type: Kind/category of change (e.g., "IN", "OUT", "ADJUSTMENT").
        date: Timestamp of when the change occurred (timezone awareness per app policy).
        stock: The quantity delta associated with the change. Conventionally:
            - positive for additions (e.g., receiving stock),
            - negative for removals (e.g., sales, write-offs).
            Your application may also store absolute values—define and enforce
            the convention you prefer.
        reason: Free-form human-readable rationale or note for the change.
        user: Identifier (username, email, etc.) of the actor who performed the change.
        product_id: The typed identifier of the affected product.

    Example:
        >>> change = ProductChanges(
        ...     id=ProductChangesId(101),
        ...     type="IN",
        ...     date=datetime(2025, 8, 17, 10, 0, 0),
        ...     stock=25,
        ...     reason="Supplier delivery PO-1234",
        ...     user="dsequeira",
        ...     product_id=ProductId("SKU-ABC-001"),
        ... )
        >>> change.stock
        25
    """
    type: str
    date: datetime
    stock: int
    reason: str
    user: str
    product_id: ProductId

    def __init__(
        self,
        id: ProductChangesId,
        type: str,
        date: datetime,
        stock: int,
        reason: str,
        user: str,
        product_id: ProductId,
    ) -> None:
        """Initialize a new :class:`ProductChanges` record.

               Args:
                   id: Unique identifier for this change record.
                   type: Category of the change (e.g., "IN", "OUT", "ADJUSTMENT").
                   date: When the change occurred.
                   stock: Quantity delta or absolute count, per your domain convention.
                   reason: Human-readable description of why the change happened.
                   user: The actor who performed/logged the change.
                   product_id: The identifier of the product impacted by the change.
               """
        super().__init__(id)
        self.type = type
        self.date = date
        self.stock = stock
        self.reason = reason
        self.user = user
        self.product_id = product_id

    def __str__(self) -> str:
        return f"SKU Del Producto: {self.product_id.get_value()} \n tipo: {self.type} \n date: {self.date} \n stock: {self.stock} \n reason: {self.reason} \n\n\n"


class ProductChangesParser:
    """Utility functions to convert :class:`ProductChanges` to/from dictionaries.

    The produced dictionaries are JSON-friendly and suitable for persistence in
    text formats. The schema intentionally uses primitives only:

        {
            "id": <int|str>,
            "type": <str>,
            "date": <ISO-8601 str>,
            "stock": <int>,
            "reason": <str>,
            "user": <str>,
            "product_id": <int|str>
        }
    """
    @staticmethod
    def from_product_changes_to_dict(change: ProductChanges) -> object:
        """Serialize a :class:`ProductChanges` entity into a JSON-friendly dict.

        Args:
            change: The entity instance to serialize.

        Returns:
            A dictionary with primitive fields only (IDs unwrapped via
            ``.get_value()`` and ``date`` rendered with ISO 8601).
        """
        return {
            "id": change.id.get_value(),
            "type": change.type,
            "date": change.date.isoformat(),  # datetime → str
            "stock": change.stock,
            "reason": change.reason,
            "user": change.user,
            "product_id": change.product_id.get_value(),
        }

    @staticmethod
    def from_dict_to_product_changes(data: dict) -> ProductChanges:
        """Deserialize a dict into a :class:`ProductChanges` entity.

        Args:
            data: A dictionary following the schema produced by
                :meth:`from_product_changes_to_dict`.

        Returns:
            A reconstructed :class:`ProductChanges` instance.

        Raises:
            KeyError: If required keys are missing from ``data``.
            ValueError: If types/values cannot be coerced to the expected forms.
        """
        return ProductChanges(
            ProductChangesId(int(data["id"])),
            data["type"],
            datetime.fromisoformat(data["date"]),
            int(data["stock"]),
            data["reason"],
            data["user"],
            ProductId(data["product_id"]),
        )
