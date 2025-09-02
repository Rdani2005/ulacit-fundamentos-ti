import os
import json

from typing import List, Optional

from book.book import Book
from book.book_parser import BookParser


"""
Module: book_repository
-----------------------
Provides a simple file-based repository for storing and retrieving
Book objects in JSON format.

Main Responsibilities:
- Ensure the storage directory exists.
- Save a full list of books (overwrite mode).
- Retrieve all books from file.
- Get the last stored book ID.
- Find a book by ID.
- Update an existing book by ID.

Notes:
- This repository assumes `BookParser` provides two functions:
  * from_book_to_dict(book: Book) -> dict
  * from_dic_to_book(data: dict) -> Book
- Read/write operations are synchronous and not atomic. In concurrent
  environments, file locking or a transactional approach is recommended.
"""

class BookRepository:
    """
    A JSON file-based repository for Book objects.

    Attributes
    ----------
    __filename : str
        The path to the JSON file where books are stored.

    JSON file example
    -----------------
    [
      {"id": 1, "title": "...", "author": "..."},
      {"id": 2, "title": "...", "author": "..."}
    ]
    """
    def __init__(self, filename: str) -> None:
        """
        Initialize the repository and ensure the directory exists.

        Parameters
        ----------
        filename : str
            Path (including filename) where the books will be stored.
        """
        self.__filename = filename
        os.makedirs(os.path.dirname(self.__filename), exist_ok=True)
        
    def save_books(self, books: List[Book]) -> None:
        """
        Save the complete list of books to the file (overwrites existing data).

        Parameters
        ----------
        books : List[Book]
            Collection of Book objects to serialize and store.

        Raises
        ------
        OSError
            If there is a file writing error.
        """
        with open(self.__filename, 'w', encoding='utf-8') as f:
            json.dump([BookParser.from_book_to_dict(book) for book in books], f, indent=4)

    def get_books(self) -> List[Book]:
        """
        Retrieve all books stored in the file.

        Returns
        -------
        List[Book]
            List of Book objects. Returns an empty list if the file does not exist.

        Raises
        ------
        ValueError
            If the file content is not valid JSON.
        OSError
            If there is a file reading error.
        """
        if not os.path.exists(self.__filename):
            return []
        with open(self.__filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [BookParser.from_dic_to_book(book) for book in data]

    def get_last_book_id(self) -> int:
        """
        Get the ID of the last book in the file (based on file order).

        Returns
        -------
        int
            The last book's ID. Returns 0 if the file does not exist or is empty.

        Raises
        ------
        ValueError
            If the file content is not valid JSON.
        OSError
            If there is a file reading error.
        """
        if not os.path.exists(self.__filename):
            return 0
        with open(self.__filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not data:
                return 0
            return int(data[-1]['id'])

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Find and return a book by its ID.

        Parameters
        ----------
        book_id : int
            The ID of the book to search for.

        Returns
        -------
        Optional[Book]
            The Book instance if found, otherwise None.

        Raises
        ------
        ValueError
            If the file content is not valid JSON.
        OSError
            If there is a file reading error.
        """
        with open(self.__filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            books = [BookParser.from_dic_to_book(book) for book in data]
            for book in books:
                if book.id == book_id:
                    return book
            return None

    def update_book(self, updated_book: Book) -> bool:
        """
        Update an existing book by matching its ID.

        This method replaces the entire book record in the JSON file
        with the serialized data from `updated_book`.

        Parameters
        ----------
        updated_book : Book
            The book object with updated values. Must have an existing ID.

        Returns
        -------
        bool
            True if the book was found and updated, False if not found.

        Raises
        ------
        ValueError
            If the file content is not valid JSON.
        OSError
            If there is a file reading or writing error.
        """
        if not os.path.exists(self.__filename):
            return False

        with open(self.__filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for i, book_dict in enumerate(data):
            if int(book_dict.get('id')) == updated_book.id:
                data[i] = BookParser.from_book_to_dict(updated_book)
                with open(self.__filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                return True

        return False