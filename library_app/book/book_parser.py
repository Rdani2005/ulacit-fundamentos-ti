from book.book import Book

class BookParser:
    """
    Utility class for converting between `Book` objects and dictionaries.

    This class is used to serialize and deserialize `Book` instances
    when storing them in or reading them from a JSON file.

    Methods
    -------
    from_book_to_dict(book: Book) -> dict
        Converts a Book instance into a dictionary representation.
    from_dic_to_book(book_dict: dict) -> Book
        Converts a dictionary into a Book instance.
    """
    @staticmethod
    def from_book_to_dict(book: Book) -> dict:
        """
        Convert a Book object into a dictionary.

        Parameters
        ----------
        book : Book
            The Book instance to convert.

        Returns
        -------
        dict
            A dictionary with keys: "id", "title", "author", "year", "available".

        Example
        -------
        >>> book = Book(1, "1984", "George Orwell", 1949, True)
        >>> BookParser.from_book_to_dict(book)
        {
            "id": 1,
            "title": "1984",
            "author": "George Orwell",
            "year": 1949,
            "available": True
        }
        """
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "available": book.available,
        }

    @staticmethod
    def from_dic_to_book(book_dict: dict) -> Book:
        """
        Convert a dictionary into a Book object.

        Parameters
        ----------
        book_dict : dict
            Dictionary containing book data. Expected keys:
            - "id"
            - "title"
            - "author"
            - "year"
            - "available"

        Returns
        -------
        Book
            A new Book instance created from the dictionary.

        Example
        -------
        >>> data = {
        ...     "id": 1,
        ...     "title": "1984",
        ...     "author": "George Orwell",
        ...     "year": 1949,
        ...     "available": True
        ... }
        >>> BookParser.from_dic_to_book(data)
        Book(book_id=1, title="1984", author="George Orwell", release_year=1949, available=True)
        """
        return Book(
            book_id=book_dict.get("id"),
            title=book_dict.get("title"),
            author=book_dict.get("author"),
            release_year=book_dict.get("year"),
            available=book_dict.get("available"),
        )