"""Manager for product change history (inventory events).

This module provides :class:`ProductChangesManager`, an application-service
layer that orchestrates creation, listing, and persistence of
:class:`history.entity.product_changes.ProductChanges` records using a
:class:`history.repository.product_changes_repository.ProductChangesRepository`.

Layering (DDD-inspired)
-----------------------
UI / CLI / API  →  ProductChangesManager  →  Repository  →  Storage

Notes
-----
- Console output is intentionally printed in Spanish to match the rest of the
  CLI/UX in your project.
- The in-memory cache (``self.product_changes``) is synchronized with the
  repository via :meth:`load_data` and :meth:`save_all`.

Example
-------
>>> # repo = ProductChangesRepository("changes.json")  # doctest: +SKIP
>>> # mgr = ProductChangesManager(repo)                # doctest: +SKIP
>>> # mgr.show_all_changes()                           # doctest: +SKIP
"""

from domain.manager.domain_manager import Manager
from history.repository.product_changes_repository import ProductChangesRepository
from history.value_object.product_changes_id import ProductChangesId
from products.entity.product import Product
from history.entity.product_changes import ProductChanges

from typing import List

from products.value_object.product_id import ProductId


class ProductChangesManager(Manager[ProductChangesRepository]):
    """Application-service manager for product inventory change records.

    Responsibilities:
        - Maintain an in-memory cache of :class:`ProductChanges`.
        - Create new change records and persist them.
        - Display change history for a given product or user, or list all changes.

    Attributes:
        repository: The injected :class:`ProductChangesRepository` used for
            persistence operations.
        product_changes: In-memory list of change records, populated from
            persistence on initialization via :meth:`load_data`.
    """
    product_changes = List[ProductChanges]

    def __init__(self, repository: ProductChangesRepository):
        """Initialize the manager and load change records from storage.

        Args:
            repository: The repository used to load and persist change records.
        """
        super().__init__(repository)
        self.load_data()

    def create_product_change(self, product_change: ProductChanges) -> None:
        """Append a new change record and persist the updated collection.

        Args:
            product_change: The :class:`ProductChanges` instance to add.

        Side Effects:
            - Updates the in-memory cache.
            - Writes the full collection to the repository (JSON file).
            - Reloads the cache from storage for consistency.
        """
        self.product_changes.append(product_change)
        self.save_all()

    def show_product_changes(self, product: Product) -> None:
        """Print the change history for a specific product.

        The output is printed in Spanish and includes a header with the product
        identifier (SKU). Only changes whose ``product_id`` matches the
        provided product's id are shown.

        Args:
            product: The product whose change history should be displayed.

        """
        print(f"========== Historial de Cambios para Producto {product.id.get_value()} ==========")
        for change in self.product_changes:
            if change.product_id.get_value() == product.get_id().get_value():
              print(change)

    def show_all_changes_by_user(self, user: str) -> None:
        """Print all change records performed by the specified user.

        Args:
            user: The user identifier (e.g., username or email) to filter by.
        """
        print(f"========== Historial de Cambios para Usuario {user} ==========")
        for change in self.product_changes:
            if change.user == user:
                print(change)

    def show_all_changes(self) -> None:
        """Print all change records currently loaded in memory."""
        for change in self.product_changes:
            print(change)

    def get_last_id(self) -> ProductChangesId:
        self.load_data()
        if (len(self.product_changes) == 0):
            return ProductChangesId(1)
        last_id = self.product_changes[-1].get_id().get_value()
        return ProductChangesId(last_id + 1)

    def load_data(self) -> None:
        """Refresh the in-memory cache from persistent storage.

        Reads all change records from the repository and assigns them to
        ``self.product_changes``.
        """
        self.product_changes = self.repository.get_all()

    def save_all(self) -> None:
        """Persist the current in-memory cache and reload it from storage.

        Side Effects:
            - Writes the entire collection to the repository.
            - Calls :meth:`load_data` to refresh the in-memory cache.
        """
        self.repository.save_all(self.product_changes)
        self.load_data()