from config.composition_root import bootstrap
from menu.menu import Menu
class Main:
    menu: Menu

    def __init__(self):
        container = bootstrap()
        self.menu = Menu(
            container.loan_manager,
            container.book_manager,
            container.student_manager
        )

    def run(self):
        self.menu.menu()

if __name__ == "__main__":
    Main().run()