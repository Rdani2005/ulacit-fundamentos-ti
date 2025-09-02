from book.book import Book
from inputs import Inputs

class BookFactory:
    """
    Factory class responsible for creating `Book` objects.

    This class handles user input to gather book information
    and then returns a fully initialized `Book` instance.

    Methods
    -------
    create_book(book_id: int) -> Book
        Prompts the user for book details and returns a new Book instance.
    """
    @staticmethod
    def create_book(book_id: int):
        """
        Prompt the user for book details and create a Book instance.

        Parameters
        ----------
        book_id : int
            The unique ID to assign to the new book.

        Returns
        -------
        Book
            A new Book object populated with user-provided data.

        Notes
        -----
        - Uses `Inputs.get_non_empty_input` to ensure no empty fields.
        - The book is created with `available=True` by default.

        Example
        -------
        >>> new_book = BookFactory.create_book(1)
        ============= AGREGANDO LIBRO =============
        Nombre del libro: 1984
        Autor del libro: George Orwell
        Año de Publicacion: 1949
        >>> print(new_book)
        Book(id=1, title="1984", author="George Orwell", year=1949, available=True)
        """
        print("============= AGREGANDO LIBRO =============")
        name: str = Inputs.get_non_empty_input("Nombre del libro: ")
        author: str = Inputs.get_non_empty_input("Autor del libro: ")
        published_year: str = Inputs.get_non_empty_input("Año de Publicacion: ")
        available: bool = True

        return Book(book_id, name, author, published_year, available)