"""Interactive CLI menu for product and inventory-change operations.

This module defines :class:`Menu`, a simple command-line interface that
coordinates user-driven actions over products and their change history by
delegating to the application-service managers:

- :class:`products.manager.product_manager.ProductManager`
- :class:`history.manager.product_changes_manager.ProductChangesManager`

Responsibilities
----------------
- Create products via a factory and persist them.
- List products and filter them interactively.
- Increase or decrease product stock and log each change in the history.
- Delete products (with confirmation) and record the deletion in the history.
- Display change history (all, by product, or by user).

Design Notes
------------
- Console prompts and messages are in Spanish to match the existing UX.
- This menu assumes the following manager API is available in your project:
    * ``ProductManager.create_product(product: Product) -> None``
    * ``ProductManager.get_product_by_id(id: ProductId) -> Optional[Product]``
    * ``ProductManager.delete_product_stock(product: Product, amount: int) -> bool``
      (expected to return ``True`` on success; adjust if your implementation
      returns ``None`` or raises)
    * ``ProductManager.add_product_stock(product: Product, amount: int) -> None``
    * ``ProductManager.filter_products_interactive() -> None``
    * ``ProductChangesManager.create_product_change(change: ProductChanges) -> None``
    * ``ProductChangesManager.get_last_id() -> ProductChangesId``
      (expected to return the next/sequential identifier)
    * ``ProductChangesManager.show_all_changes() -> None``
    * ``ProductChangesManager.show_product_changes(product: Product) -> None``
    * ``ProductChangesManager.show_all_changes_by_user(user: str) -> None``

Example
-------
>>> # menu = Menu(product_manager, product_changes_manager)   # doctest: +SKIP
>>> # menu.menu(user="dsequeira")                             # doctest: +SKIP
"""

import datetime

from history.manager.product_changes_manager import ProductChangesManager
from inputs import Inputs
from products.entity.product import ProductFactory, Product
from products.manager.product_manager import ProductManager
from history.entity.product_changes import ProductChanges
from products.value_object.product_id import ProductId


class Menu:
    """Simple console-driven menu for product management and history logging."""
    product_manager: ProductManager
    product_changes_manager: ProductChangesManager

    def __init__(self, product_manager: ProductManager, product_changes_manager: ProductChangesManager):
        """Initialize the menu with its collaborating managers.

             Args:
                 product_manager: Manager that orchestrates product use cases.
                 product_changes_manager: Manager that orchestrates inventory-change
                     history use cases.
             """
        self.product_manager = product_manager
        self.product_changes_manager = product_changes_manager

    def create_product(self, user: str) -> None:
        """Create a new product and log an initial history entry.

        Steps:
            1) Builds a product using :class:`ProductFactory`.
            2) Persists it through :class:`ProductManager`.
            3) Appends a :class:`ProductChanges` record noting creation.

        Args:
            user: The actor performing the operation (used in history logging).
        """
        new_product = ProductFactory.create_product()
        self.product_manager.create_product(new_product)
        print("Producto Creado Correctamente.")

        self.product_changes_manager.create_product_change(
            ProductChanges(
                self.product_changes_manager.get_last_id(),
                "Producto Creado",
                datetime.datetime.now(),
                new_product.in_stock,
                "Agregado nuevo producto.",
                user,
                new_product.get_id()
            )
        )

    def show_products(self) -> None:
        """Display the current list of products."""
        self.product_manager.show_products_list()

    def show_all_history_changes(self) -> None:
        """Display all recorded inventory changes."""
        self.product_changes_manager.show_all_changes()

    def show_product_changes_by_product(self):
        """Prompt for a product ID and display its change history.

        Behavior:
            - Asks the user for a SKU.
            - Retrieves the product; if absent or inactive, informs the user.
            - Otherwise, prints the product's change history.
        """
        product = self.product_manager.get_product_by_id(
            ProductId(Inputs.get_non_empty_input("Cual es el SKU del producto a consultar?"))
        )
        if product is None or product.active == False:
            print("El Producto no existe.")
            return
        self.product_changes_manager.show_product_changes(product)

    def show_product_changes_by_user(self) -> None:
        """Prompt for a username and display all changes associated with it."""
        user = Inputs.get_non_empty_input("Cual es el usuario a consultar?")
        self.product_changes_manager.show_all_changes_by_user(user)

    def reduce_product_stock(self, user: str) -> None:
        """Reduce stock for a product and log the change.

        Prompts:
            - Product SKU
            - Reason for the change
            - Quantity to subtract

        Args:
            user: The actor performing the operation (used in history logging).
        """
        product = self.product_manager.get_product_by_id(
            ProductId(Inputs.get_non_empty_input("Cual es el producto a reducir su stock?"))
        )
        reason = Inputs.get_non_empty_input("Cual es el motivo?")
        amount = Inputs.get_valid_number("Cual es la cantidad de productos a reducir")

        if product is None or product.active == False:
            print("El Producto no existe.")
            return

        if self.product_manager.delete_product_stock(product, amount):
            print("El Producto actualizado correctamente.")
            self.product_changes_manager.create_product_change(
                ProductChanges(
                    self.product_changes_manager.get_last_id(),
                    "STOCK REDUCIDO",
                    datetime.datetime.now(),
                    amount,
                    reason,
                    user,
                    product.get_id()
                )
            )
            return
        print("El Producto no se actualizado correctamente.")

    def get_more_stock_for_product(self, user: str) -> None:
        """Increase stock for a product and log the change.

        Prompts:
            - Product SKU
            - Reason for the change
            - Quantity to add

        Args:
            user: The actor performing the operation (used in history logging).
        """
        product = self.product_manager.get_product_by_id(
            ProductId(Inputs.get_non_empty_input("Cual es el producto a aumentar su stock?"))
        )
        reason = Inputs.get_non_empty_input("Cual es el motivo?")
        amount = Inputs.get_valid_number("Cual es la cantidad de productos a aumentar")

        if product is None or product.active == False:
            print("El Producto no existe.")
            return

        self.product_manager.add_product_stock(product, amount)
        print("El Producto actualizado correctamente.")
        self.product_changes_manager.create_product_change(
                ProductChanges(
                    self.product_changes_manager.get_last_id(),
                    "STOCK AUMENTADO",
                    datetime.datetime.now(),
                    amount,
                    reason,
                    user,
                    product.get_id()
                )
        )


    def filter_products(self):
        """Run the interactive product filter flow."""
        self.product_manager.filter_products_interactive()

    def delete_product(self, user: str) -> None:
        """Delete a product (after prompts) and log the deletion.

        Prompts:
            - Product SKU
            - Reason for deletion

        Args:
            user: The actor performing the operation (used in history logging).

        Notes:
            Assumes ``ProductManager.delete_product`` handles user confirmation
            internally. If not, add confirmation here before deleting.
        """
        product = self.product_manager.get_product_by_id(
            ProductId(Inputs.get_non_empty_input("Cual es el producto a borrar?"))
        )
        reason = Inputs.get_non_empty_input("Cual es el motivo?")
        if product is None or product.active == False:
            print("El Producto no existe.")
        self.product_manager.delete_product(product)
        print("Producto eliminado correctamente.")
        self.product_changes_manager.create_product_change(
                ProductChanges(
                    self.product_changes_manager.get_last_id(),
                    "PRODUCTO ELIMINADO",
                    datetime.datetime.now(),
                    0,
                    reason,
                    user,
                    product.get_id()
                )
        )

    def menu(self, user: str) -> None:
        """Display the main menu and dispatch chosen actions.

        Flow:
            - Prints options 1–10.
            - Reads a numeric option via :class:`Inputs`.
            - Invokes the corresponding method.
            - Recursively re-enters the menu unless the user chooses to exit.

        Args:
            user: Current user performing the actions (used for history logging).
        """
        print("\n\n\n========== Menu Principal ==========")
        print("1. Crear Producto")
        print("2. Ver Productos")
        print("3. Filtrar Productos")
        print("4. Eliminar Stock de Producto")
        print("5. Aumentar Stock de Producto")
        print("6. Eliminar Producto")
        print("7. Mostrar Historial de Cambios")
        print("8. Mostrar Historial de Cambios por Producto")
        print("9. Mostrar Historial de Cambios por Usuario")
        print("10. Salir")

        option = Inputs.get_valid_number("Elija una opcion: ")

        if option == 1:
            self.create_product(user)
        elif option == 2:
            self.show_products()
        elif option == 3:
            self.filter_products()
        elif option == 4:
            self.reduce_product_stock(user)
        elif option == 5:
            self.get_more_stock_for_product(user)
        elif option == 6:
            self.delete_product(user)
        elif option == 7:
            self.show_all_history_changes()
        elif option == 8:
            self.show_product_changes_by_product()
        elif option == 9:
            self.show_product_changes_by_user()
        elif option == 10:
            exit(0)
        else:
            print("La Opcion es Invalida.")
        self.menu(user)