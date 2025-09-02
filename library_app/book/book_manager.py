from typing import Optional, List


from book.book_repository import BookRepository
from book.book import Book

class BookManager:
    """
    Manages the collection of Book objects in memory and coordinates
    persistence with a BookRepository.

    Attributes
    ----------
    __book_repository : BookRepository
        Repository used for reading and writing book data to persistent storage.
    __books : List[Book]
        In-memory list of Book objects.

    Methods
    -------
    get_book_by_id(id: int) -> Optional[Book]
        Retrieve a book from the repository by its ID.
    show_books() -> None
        Display the list of available books in memory.
    deactivate_book(id: int) -> None
        Mark a book as unavailable and remove it from the in-memory list.
    add_book(book: Book) -> None
        Add a new book to the in-memory list and persist the changes.
    build_new_book_id() -> int
        Generate a new unique book ID based on the repository's last ID.
    """

    def __init__(self, book_repository: BookRepository) -> None:
        """
          Initialize the BookManager with a BookRepository.

          Parameters
          ----------
          book_repository : BookRepository
              The repository used for persistent storage operations.
          """
        self.__book_repository = book_repository
        self.__books: List[Book] = []

    def get_book_by_id(self, id: int) -> Optional[Book]:
        """
        Retrieve a book from the repository by its ID.

        Parameters
        ----------
        id : int
            The ID of the book to retrieve.

        Returns
        -------
        Optional[Book]
            The Book instance if found, otherwise None.
        """
        book = self.__book_repository.get_book_by_id(id)
        return book

    def show_books(self) -> None:
        """
        Print all available books in the in-memory list to the console.
        """
        print("---------- LISTA DE LIBROS DISPONIBLES -----------")
        for book in self.__books:
            print(book)

    def deactivate_book(self, id: int) -> None:
        """
        Mark a book as unavailable and remove it from the in-memory list.

        Parameters
        ----------
        id : int
            The ID of the book to deactivate.

        Notes
        -----
        - If the book does not exist, a message will be printed.
        - The book is removed from the in-memory list but changes
          are not persisted unless explicitly saved.
        """
        book = self.get_book_by_id(id)
        if book is None:
            print("El libro no existe.")
            return
        book.deactivate_book()
        self.__book_repository.update_book(book)
        self.__load_data()

    def add_book(self, book: Book) -> None:
        """
        Add a book to the in-memory list and save changes to the repository.

        Parameters
        ----------
        book : Book
            The book to add.
        """
        self.__books.append(book)
        self.__save_data()
        print("El libro ha sido guardado correctamente.")

    def __save_data(self) -> None:
        """
        Persist the current in-memory book list to the repository
        and reload the data into memory.
        """
        self.__book_repository.save_books(self.__books)
        self.__load_data()

    def __load_data(self) -> None:
        """
        Load the list of books from the repository into memory.
        """
        self.__books = self.__book_repository.get_books()

    def build_new_book_id(self) -> int:
        """
        Generate a new book ID by incrementing the repository's last ID.

        Returns
        -------
        int
            A unique book ID for a new entry.
        """
        last_book_id = self.__book_repository.get_last_book_id()
        return last_book_id + 1