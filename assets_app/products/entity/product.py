"""Product domain entity and (de)serialization helpers.

This module defines:

- :class:`Product`: A domain entity representing a sellable item with
  identifying information, inventory state, price, description, and activation
  status.
- :class:`ProductParser`: Utilities to convert between the entity and a
  plain-JSON-serializable ``dict`` representation.

Design Notes
------------
- **Typed ID**: ``Product.id`` is a :class:`products.value_object.product_id.ProductId`
  (a ``DomainId`` wrapper) to prevent mixing different ID kinds.
- **Decimal price**: Prices are modeled with :class:`decimal.Decimal` to avoid
  floating-point rounding issues. When serialized to JSON, they are emitted as
  strings, and parsed back from strings.
- **JSON schema**: The serialized form uses ``camelCase`` for ``inStock`` to
  match common JSON conventions. The parser handles this mapping explicitly.
- **Import fix**: The base entity import uses
  ``domain.entity.domain_entity.DomainEntity`` (note the corrected module name).

Example
-------
>>> from decimal import Decimal
>>> from products.value_object.product_id import ProductId
>>> p = Product(
...     id=ProductId("SKU-ABC-001"),
...     name="Widget",
...     category="Gadgets",
...     in_stock=100,
...     price=Decimal("19.99"),
...     description="A very useful widget.",
...     active=True,
... )
>>> d = ProductParser.from_product_to_dict(p)
>>> d["price"], d["inStock"]  # Decimal serialized as str; snake->camel
('19.99', 100)
>>> p2 = ProductParser.from_dict_to_product(d)
>>> p2.get_id().get_value() == "SKU-ABC-001"
True
"""
from decimal import Decimal

from domain.entity.domain_enitty import DomainEntity
from inputs import Inputs
from products.value_object.product_id import ProductId


class Product(DomainEntity[ProductId]):
    """Domain entity representing a product in the catalog/inventory.

    Attributes:
        id: Typed product identifier (:class:`ProductId`).
        name: Human-readable product name.
        category: Category or family to which the product belongs.
        in_stock: Current on-hand inventory count.
        price: Unit price as :class:`~decimal.Decimal`.
        description: Free-form description or marketing copy.
        active: Whether the product is currently active/visible for sale.
    """
    name: str
    category: str
    in_stock: int
    price: Decimal
    description: str
    active: bool

    def __init__(
        self,
        id: ProductId,
        name: str,
        category: str,
        in_stock: int,
        price: Decimal,
        description: str,
        active: bool,
    ) -> None:
        """Initialize a :class:`Product`.

        Args:
            id: The typed identifier for this product.
            name: Product name.
            category: Product category or family.
            in_stock: On-hand quantity (non-negative by convention).
            price: Unit price as :class:`~decimal.Decimal`.
            description: Human-readable description.
            active: If ``True``, product is considered enabled/for sale.

        Notes:
            Add validation (e.g., non-negative ``in_stock``, non-negative
            ``price``, non-empty ``name``) according to your domain rules.
        """
        super().__init__(id)
        self.name = name
        self.category = category
        self.in_stock = in_stock
        self.price = price
        self.description = description
        self.active = active

    # getters
    def get_name(self) -> str:
        """Return the product name."""
        return self.name

    def get_category(self) -> str:
        """Return the product category."""
        return self.category

    def get_in_stock(self) -> int:
        """Return the current on-hand quantity."""
        return self.in_stock

    def get_price(self) -> Decimal:
        """Return the unit price."""
        return self.price

    def get_description(self) -> str:
        """Return the product description."""
        return self.description

    def get_active(self) -> bool:
        """Return whether the product is active/for sale."""
        return self.active

    # setters / mutators
    def set_in_stock(self, value: int) -> None:
        """Set the on-hand quantity.

        Args:
            value: New inventory count (expected non-negative).
        """
        self.in_stock = value

    def set_active(self, value: bool) -> None:
        """Enable/disable the product.

        Args:
            value: ``True`` to activate, ``False`` to deactivate.
        """
        self.active = value

    def __str__(self):
        """Return a human-readable representation of this product."""
        return f"SKU: {self.get_id().get_value()} Producto: {self.name} - Descripcion: {self.description} - cantidad: {self.get_in_stock()} - Precio Unitario: {self.get_price()} - Activo: {self.in_stock >= 0 and self.active}"


class ProductParser:
    """Utilities to convert :class:`Product` to/from JSON-friendly dictionaries.

    JSON schema produced/consumed:

    .. code-block:: json

        {
          "id": "SKU-ABC-001",
          "name": "Widget",
          "category": "Gadgets",
          "inStock": 100,
          "price": "19.99",
          "description": "A very useful widget.",
          "active": true
        }
    """

    @staticmethod
    def from_product_to_dict(product: Product) -> object:
        """Serialize a :class:`Product` entity to a JSON-friendly dict.

        Args:
            product: The product to serialize.

        Returns:
            A dictionary containing only JSON-serializable primitives.
        """
        return {
            "id": product.id.get_value(),
            "name": product.name,
            "category": product.category,
            "inStock": product.in_stock,
            "price": str(product.price),  # Decimal → str
            "description": product.description,
            "active": product.active,
        }

    @staticmethod
    def from_dict_to_product(data: dict) -> Product:
        """Deserialize a dictionary into a :class:`Product` entity.

        Args:
            data: A dictionary following the schema documented above.

        Returns:
            A reconstructed :class:`Product` instance.

        Raises:
            KeyError: If a required key is missing from ``data``.
            ValueError: If values cannot be coerced to the expected types.
        """
        return Product(
            ProductId(data["id"]),
            data["name"],
            data["category"],
            int(data["inStock"]),
            Decimal(data["price"]),
            data["description"],
            bool(data["active"]),
        )


class ProductFactory:
    """
    Factory class responsible for creating `Product` objects.

    This class handles user input to gather product information
    and then returns a fully initialized `Product` instance.

    Methods
    -------
    create_product() -> Product
        Prompts the user for product details and returns a new Product instance.
    """

    @staticmethod
    def create_product() -> Product:
        """
        Prompt the user for product details and create a Product instance.

        Returns
        -------
        Product
            A new Product object populated with user-provided data.

        Notes
        -----
        - Uses `Inputs.get_non_empty_input` to ensure no empty fields.
        - The product is created with `active=True` by default.

        Example
        -------
        >>> prod = ProductFactory.create_product(ProductId("PRD-0001"))
        ============= AGREGANDO PRODUCTO =============
        Nombre del producto: Mouse
        Categoría: Accesorios
        Stock inicial: 10
        Precio unitario: 19.99
        Descripción: Mouse óptico USB
        >>> prod.get_name()
        'Mouse'
        """
        print("============= AGREGANDO PRODUCTO =============")
        id: str = Inputs.get_non_empty_input("SKU del producto: ")
        name: str = Inputs.get_non_empty_input("Nombre del producto: ")
        category: str = Inputs.get_non_empty_input("Categoría: ")
        in_stock: int = Inputs.get_valid_number("Stock inicial: ")
        price: Decimal = Inputs.get_valid_number("Precio unitario: ")
        description: str = Inputs.get_non_empty_input("Descripción: ")

        active: bool = True

        return Product(
            ProductId(id),
            name,
            category,
            in_stock,
            price,
            description,
            active,
        )