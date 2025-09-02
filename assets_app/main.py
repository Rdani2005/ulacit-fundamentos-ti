"""Application entry point for the Assets Store CLI.

This module wires up the application dependencies (via the composition root)
and starts the interactive command-line menu.

Flow
----
1) Call :func:`config.composition_root.bootstrap` to construct the container.
2) Build the :class:`menu.menu.Menu` using managers from the container.
3) Prompt the user for a username and enter the main menu loop.

Notes
-----
- Console messages and prompts are intentionally in Spanish to match the
  existing UX across the application.
"""
from config.composition_root import bootstrap
from inputs import Inputs

from menu.menu import Menu
class Main:
    """Orchestrates initialization and execution of the CLI application.

    Attributes:
        menu: The interactive menu responsible for user-facing operations.
    """

    menu: Menu
    def __init__(self):
        """Initialize the application by building the dependency graph.

        Steps:
            - Invoke :func:`bootstrap` to obtain the process-wide container.
            - Construct the top-level :class:`Menu` with the configured managers.
        """
        container = bootstrap()
        self.menu = Menu(
            container.product_manager,
            container.product_changes_manager
        )

    def run(self):
        """Start the CLI, prompt for the current user, and open the main menu.

        This method blocks while the menu loop is active.
        """
        print("Bienvenido a Assets Store!")
        user = Inputs.get_non_empty_input("Digite su usuario para ingresar: ")
        self.menu.menu(user)

if __name__ == "__main__":
    Main().run()