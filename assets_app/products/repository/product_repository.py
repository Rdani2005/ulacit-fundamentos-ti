"""JSON-backed repository for products.

This module implements a concrete :class:`DomainRepository` for
:class:`products.entity.product.Product` entities persisted as a single JSON
array on disk. It uses :class:`products.entity.product.ProductParser` to
serialize/deserialize entities.

Behavior overview
-----------------
- **Storage model**: one JSON file containing a list of product objects
  (JSON-friendly dictionaries).
- **Write strategy**: :meth:`save_all` overwrites the entire file with the
  provided collection.
- **Read strategy**: :meth:`get_all` loads and parses the whole file.
- **Lookup/update/delete**: implemented in terms of reading the current file,
  modifying the in-memory list, and writing it back.

Suitability
-----------
This implementation is ideal for development, tests, small datasets, or
single-user tools. For large datasets, concurrency, or transactional needs,
use a database-backed repository.

Notes
-----
- Errors from the filesystem and JSON parser (e.g., :class:`OSError`,
  :class:`json.JSONDecodeError`) are allowed to propagate.
- :meth:`get_all` returns an empty list if the file does not exist.
"""
from typing import Optional, List

from domain.repository.domain_repository import DomainRepository, K, E
from products.value_object.product_id import ProductId
from products.entity.product import Product, ProductParser

import os
import json

class ProductRepository(DomainRepository[ProductId, Product]):
    """File-based repository for :class:`Product` entities.

    The base class constructor should be provided a ``filename`` (path to the
    JSON file). Each method reads/writes that file.

    JSON schema
    -----------
    The on-disk representation is an array of objects produced by
    :meth:`ProductParser.from_product_to_dict`, for example:

    .. code-block:: json

        [
          {
            "id": "SKU-ABC-001",
            "name": "Widget",
            "category": "Gadgets",
            "inStock": 100,
            "price": "19.99",
            "description": "A very useful widget.",
            "active": true
          }
        ]
    """

    def save_all(self, entities: List[Product]) -> None:
        """Persist the entire collection of products to disk.

        The file is overwritten (open → write → close).

        Args:
            entities: The list of products to serialize.

        Raises:
            OSError: If the file cannot be opened or written.
            TypeError: If an entity cannot be serialized by the parser.
        """
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([ProductParser.from_product_to_dict(product) for product in entities], f, indent=4)

    def get_all(self) -> List[Product]:
        """Load and return all products from disk.

        If the file does not exist, an empty list is returned.

        Returns:
            A list of :class:`Product` instances.

        Raises:
            OSError: If the file exists but cannot be opened.
            json.JSONDecodeError: If the file contains invalid JSON.
            KeyError/ValueError: If a record cannot be parsed by the parser.
        """
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [ProductParser.from_dict_to_product(product) for product in data]

    def get_by_id(self, id: ProductId) -> Optional[E]:
        """Retrieve a product by its identifier.

        Args:
            id: The typed product identifier to look up.

        Returns:
            The matching :class:`Product` if found; otherwise ``None``.

        Notes:
            This implementation performs a linear scan over the file contents.
            Consider indexing or a database for frequent lookups at scale.

        Raises:
            OSError: If the file cannot be opened.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            products = [ProductParser.from_dict_to_product(product) for product in data]
            for product in products:
                if product.get_id().get_value() == id.get_value():
                    return product
            return None

    def update(self, entity: Product) -> None:
        """Replace an existing product with the same identifier.

        The first product whose id equals ``entity.get_id()`` is replaced.
        If no record exists, the method is a no-op.

        Args:
            entity: The updated product to persist.

        Raises:
            OSError: If saving the updated collection fails.
        """
        products = self.get_all()
        updated = False

        for i, p in enumerate(products):
            if p.get_id() == entity.get_id():
                products[i] = entity
                updated = True
                break

        if updated:
            self.save_all(products)

    def delete(self, id: ProductId) -> None:
        """Delete a product by its identifier.

        If the identifier does not exist, the method is a no-op.

        Args:
            id: The typed product identifier of the record to remove.

        Raises:
            OSError: If saving the updated collection fails.
        """
        products = self.get_all()
        new_products: List[Product] = []
        for p in products:
            if p.get_id().get_value() == id.get_value():
                p.active = False
            new_products.append(p)
        self.save_all(new_products)
