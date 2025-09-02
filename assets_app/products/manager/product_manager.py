"""Product application manager and utilities.

This module contains:
    - :func:`show_stock_alert`: A small utility to print a low-stock alert for a product.
    - :class:`ProductManager`: An application-service layer (manager) that
      orchestrates product-related operations by delegating persistence to a
      :class:`products.repository.product_repository.ProductRepository`.

Layering (DDD-inspired):
    UI / CLI / API  →  ProductManager (application service)  →  Repository  →  Storage

Notes:
    - The manager caches products in memory via ``self.products`` and keeps the
      cache synchronized with the repository using :meth:`load_data` / :meth:`save_data`.
"""
from decimal import Decimal, InvalidOperation

from domain.manager.domain_manager import Manager
from inputs import Inputs
from products.repository.product_repository import ProductRepository
from products.entity.product import Product
from typing import List, Optional

from products.value_object.product_id import ProductId


def show_stock_alert(product: Product) -> None:
    """Print a low-stock alert for the given product.

    The message is printed in Spanish and includes the product SKU and current stock.

    Args:
        product: The product whose stock level triggered the alert.

    Example:
        >>> # Assuming a product with in_stock == 1
        ... show_stock_alert(product)  # doctest: +SKIP
        el producto con SKU: <SKU> se esta quedando sin stock. Stock Actual: 1
    """
    print(f"el producto con SKU: {product.id.get_value()} se esta quedando sin stock. Stock Actual: {product.in_stock}")


class ProductManager(Manager[ProductRepository]):
    """Application-service manager for product operations.

    This manager coordinates read/write operations through a
    :class:`ProductRepository` and exposes simple use cases for listing,
    updating, deleting, and adjusting stock.

    Attributes:
        repository: The underlying :class:`ProductRepository` dependency provided
            to the base :class:`Manager`.
        products: An in-memory cache of :class:`Product` instances, loaded from
            and persisted to the repository.

    Lifecycle:
        On initialization, the manager loads products from the repository into
        ``self.products`` via :meth:`load_data`.
    """
    products: List[Product] = []

    def __init__(self, repository: ProductRepository):
        """Initialize the manager and load products from persistent storage.

        Args:
            repository: The repository used for persistence operations.
        """
        super().__init__(repository)
        self.load_data()

    def create_product(self, product: Product) -> None:
        self.products.append(product)
        self.save_data()


    def get_products_list(self) -> List[Product]:
        """Return the in-memory list of products.

        Returns:
            A list containing the currently cached products.
        """
        return self.products


    def get_product_by_id(self, id: ProductId) -> Optional[Product]:
        """Return the product with the given id."""
        return self.repository.get_by_id(id)

    def show_products_list(self) -> None:
        """Print the product list to stdout in a simple, readable format.

        Behavior:
            - If no products are cached, prints a Spanish message indicating the
              absence of records.
            - Otherwise, prints a header and then each product's string
              representation on its own line.
        """
        if not self.get_products_list() or len(self.get_products_list()) == 0:
            print("No hay productos registrados.")
            return

        print("============== Lista de productos ==============")
        for product in self.get_products_list():
            print(product)

    def update_product(self, product: Product) -> None:
        """Persist updates for a single product.

        The repository is instructed to replace any existing record that matches
        the given product's identifier.

        Args:
            product: The updated product entity to persist.
        """
        self.repository.update(product)
        self.load_data()

    def delete_product(self, product: Product) -> None:
        """Interactively delete a product after user confirmation.

        The user is prompted (Spanish prompt) to confirm deletion. If confirmed,
        the product is deleted by id and the in-memory cache is refreshed.

        Args:
            product: The product intended for deletion.
        """
        delete_product = Inputs.get_boolean(f"Desea borrar el producto con SKU: {product.id.get_value()}")
        if delete_product:
            self.repository.delete(product.get_id())
            self.load_data()

    def delete_product_stock(self, product: Product, amount: int) -> bool:
        """Decrease the on-hand stock for a product and persist the change.

        If the resulting stock is less than or equal to 1, a low-stock alert is
        printed via :func:`show_stock_alert`.

        Args:
            product: The product whose stock will be decreased.
            amount: The quantity to subtract from ``product.in_stock``.
                (No validation is performed here; negative results are allowed
                only if your domain permits them.)
        """
        if product.in_stock < amount:
            print("El stock actual del producto es inferior al monto solicitado.")
            return False
        product.in_stock -= amount
        if product.in_stock <= 1:
            show_stock_alert(product)
        self.update_product(product)
        return True

    def add_product_stock(self, product: Product, amount: int) -> None:
        """Increase the on-hand stock for a product and persist the change.

        Args:
            product: The product whose stock will be increased.
            amount: The quantity to add to ``product.in_stock``.
        """
        product.in_stock += amount
        self.update_product(product)

    def get_products_by_filter(
        self,
        category: Optional[str] = None,
        name: Optional[str] = None,
        *,
        description: Optional[str] = None,
        active: Optional[bool] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
        min_stock: Optional[int] = None,
        max_stock: Optional[int] = None,
        id: Optional[ProductId] = None,
        id_contains: Optional[str] = None,
        partial_match: bool = True,
        case_insensitive: bool = True,
    ) -> List[Product]:
        """Filter products by any combination of fields.

        Positional args keep backward compatibility with (category, name).

        Args:
            category: Match by category (partial by default).
            name: Match by product name (partial by default).
            description: Match by description (partial by default).
            active: Match exact active state.
            min_price, max_price: Price range (inclusive).
            min_stock, max_stock: Stock range (inclusive).
            id: Match by exact ProductId.
            id_contains: Match by substring of the textual SKU (ProductId.value).
            partial_match: If True, uses substring matching for text fields; if False, exact match.
            case_insensitive: If True, text comparisons ignore case.

        Returns:
            Filtered list of products.
        """
        products = self.get_products_list()

        def _norm(s: str) -> str:
            return s.casefold() if case_insensitive else s

        def _match_text(value: str, query: Optional[str]) -> bool:
            if query is None:
                return True
            v = _norm(value)
            q = _norm(query)
            return (q in v) if partial_match else (v == q)

        def _match_bool(value: bool, query: Optional[bool]) -> bool:
            return True if query is None else value is query

        def _match_range_num(value, lo, hi) -> bool:
            ok = True
            if lo is not None:
                ok = ok and value >= lo
            if hi is not None:
                ok = ok and value <= hi
            return ok

        result: List[Product] = []
        for p in products:
            # ID exacto
            if id is not None and p.get_id() != id:
                continue
            # ID por substring del SKU (si lo necesitas)
            if id_contains is not None:
                sku = str(p.get_id().get_value())  # asume ProductId.get_value()
                if not _match_text(sku, id_contains):
                    continue

            if not _match_text(p.category, category):
                continue
            if not _match_text(p.name, name):
                continue
            if not _match_text(p.description, description):
                continue
            if not _match_bool(p.active, active):
                continue
            if not _match_range_num(p.price, min_price, max_price):
                continue
            if not _match_range_num(p.in_stock, min_stock, max_stock):
                continue

            result.append(p)

        return result

    def load_data(self):
        """Refresh the in-memory product cache from persistent storage.

        Reads all products from the repository and assigns the result to
        ``self.products``.
        """
        self.products = self.repository.get_all()

    def save_data(self):
        """Persist the current in-memory product cache to storage.

        Writes ``self.products`` to the repository via :meth:`save_all`.
        """
        self.repository.save_all(
            self.products
        )
        self.load_data()

    @staticmethod
    def _prompt_optional_text(prompt: str) -> Optional[str]:
        s = input(prompt).strip()
        return s or None

    @staticmethod
    def _prompt_active_state() -> Optional[bool]:
        s = input("Estado (Enter=todos, 1=Activos, 0=Inactivos): ").strip()
        if s == "":
            return None
        if s == "1":
            return True
        if s == "0":
            return False
        print("Entrada inválida. Se considerará 'todos'.")
        return None

    @staticmethod
    def _prompt_optional_int(prompt: str) -> Optional[int]:
        s = input(prompt).strip()
        if s == "":
            return None
        try:
            return int(s)
        except ValueError:
            print("Número inválido. Se ignorará este criterio.")
            return None

    @staticmethod
    def _prompt_optional_decimal(prompt: str) -> Optional[Decimal]:
        s = input(prompt).strip()
        if s == "":
            return None
        try:
            return Decimal(s)
        except (InvalidOperation, ValueError):
            print("Decimal inválido. Se ignorará este criterio.")
            return None

    @staticmethod
    def _prompt_yes_no_default(prompt: str, default: bool) -> bool:
        d = "s" if default else "n"
        s = input(f"{prompt} (s/n) [default: {d}]: ").strip().lower()
        if s == "":
            return default
        return s in {"s", "si", "sí", "y", "yes"}

    def _print_products(self, products: List[Product]) -> None:
        if not products:
            print("No se encontraron productos con esos criterios.")
            return
        print(f"============== Resultados ({len(products)}) ==============")
        for p in products:
            print(p)

    # ======================================
    # Menú interactivo para filtrar productos
    # ======================================
    def filter_products_interactive(self) -> None:
        while True:
            print("\n=========== FILTROS DE PRODUCTOS ===========")
            print("1) Por categoría")
            print("2) Por nombre")
            print("3) Por descripción")
            print("4) Por estado (activo/inactivo)")
            print("5) Por rango de precio")
            print("6) Por rango de stock")
            print("7) Por SKU exacto")
            print("8) Por substring de SKU")
            print("9) Búsqueda combinada (varios criterios)")
            print("0) Volver/Salir")
            choice = input("Seleccione una opción: ").strip()

            if choice == "0":
                break

            partial_match = True
            case_insensitive = True

            if choice in {"1", "2", "3", "8", "9"}:
                partial_match = self._prompt_yes_no_default("¿Coincidencia parcial?", True)
                case_insensitive = self._prompt_yes_no_default("¿Ignorar mayúsculas/minúsculas?", True)

            if choice == "1":
                category = self._prompt_optional_text("Categoría (texto): ")
                res = self.get_products_by_filter(
                    category=category,
                    partial_match=partial_match,
                    case_insensitive=case_insensitive,
                )
                self._print_products(res)

            elif choice == "2":
                name = self._prompt_optional_text("Nombre (texto): ")
                res = self.get_products_by_filter(
                    name=name,
                    partial_match=partial_match,
                    case_insensitive=case_insensitive,
                )
                self._print_products(res)

            elif choice == "3":
                description = self._prompt_optional_text("Descripción (texto): ")
                res = self.get_products_by_filter(
                    description=description,
                    partial_match=partial_match,
                    case_insensitive=case_insensitive,
                )
                self._print_products(res)

            elif choice == "4":
                active = self._prompt_active_state()
                res = self.get_products_by_filter(active=active)
                self._print_products(res)

            elif choice == "5":
                min_price = self._prompt_optional_decimal("Precio mínimo (Enter para omitir): ")
                max_price = self._prompt_optional_decimal("Precio máximo (Enter para omitir): ")
                res = self.get_products_by_filter(min_price=min_price, max_price=max_price)
                self._print_products(res)

            elif choice == "6":
                min_stock = self._prompt_optional_int("Stock mínimo (Enter para omitir): ")
                max_stock = self._prompt_optional_int("Stock máximo (Enter para omitir): ")
                res = self.get_products_by_filter(min_stock=min_stock, max_stock=max_stock)
                self._print_products(res)

            elif choice == "7":
                sku = self._prompt_optional_text("SKU exacto: ")
                if sku:
                    res = self.get_products_by_filter(id=ProductId(sku))
                else:
                    res = []
                self._print_products(res)

            elif choice == "8":
                part = self._prompt_optional_text("Substring de SKU: ")
                res = self.get_products_by_filter(
                    id_contains=part,
                    partial_match=partial_match,
                    case_insensitive=case_insensitive,
                )
                self._print_products(res)

            elif choice == "9":
                print("== Criterios combinados (deje vacío para omitir) ==")
                category = self._prompt_optional_text("Categoría: ")
                name = self._prompt_optional_text("Nombre: ")
                description = self._prompt_optional_text("Descripción: ")
                active = self._prompt_active_state()
                min_price = self._prompt_optional_decimal("Precio mínimo: ")
                max_price = self._prompt_optional_decimal("Precio máximo: ")
                min_stock = self._prompt_optional_int("Stock mínimo: ")
                max_stock = self._prompt_optional_int("Stock máximo: ")
                sku_exact = self._prompt_optional_text("SKU exacto: ")
                sku_contains = self._prompt_optional_text("Substring de SKU: ")

                res = self.get_products_by_filter(
                    category=category,
                    name=name,
                    description=description,
                    active=active,
                    min_price=min_price,
                    max_price=max_price,
                    min_stock=min_stock,
                    max_stock=max_stock,
                    id=ProductId(sku_exact) if sku_exact else None,
                    id_contains=sku_contains,
                    partial_match=partial_match,
                    case_insensitive=case_insensitive,
                )
                self._print_products(res)

            else:
                print("Opción inválida. Intente de nuevo.")