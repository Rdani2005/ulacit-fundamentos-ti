class Book:
    """
    Represents a book entity with its main attributes and behaviors.

    Attributes
    ----------
    __id : int
        Unique identifier for the book.
    __title : str
        Title of the book.
    __author : str
        Author of the book.
    __release_year : str
        Year the book was published.
    __available : bool
        Availability status of the book (True if available, False if not).

    Methods
    -------
    id -> int
        Returns the book's unique ID.
    title -> str
        Returns the book's title.
    author -> str
        Returns the book's author.
    year -> str
        Returns the book's release year.
    available -> bool
        Returns the availability status.
    deactivate_book() -> None
        Marks the book as unavailable.
    __str__() -> str
        Returns a human-readable string representation of the book.
    __eq__(other) -> bool
        Compares two books by ID.
    """
    @property
    def id(self):
        """Get the unique ID of the book."""
        return self.__id

    @property
    def title(self):
        """Get the title of the book."""
        return self.__title

    @property
    def author(self):
        """Get the author of the book."""
        return self.__author

    @property
    def year(self):
        """Get the release year of the book."""
        return self.__release_year

    @property
    def available(self):
        """Check whether the book is available."""
        return self.__available

    def deactivate_book(self):
        """
        Mark the book as unavailable.

        This method sets the `available` property to False.
        """
        self.__available = False

    def activate_book(self):
        """
        Mark the book as available.

        This method sets the `available` property to True.
        """
        self.__available = True

    def __init__(self, book_id: int, title: str, author: str, release_year: str, available: bool) -> None:
        """
        Initialize a Book instance.

        Parameters
        ----------
        book_id : int
            Unique identifier for the book.
        title : str
            Title of the book.
        author : str
            Author of the book.
        release_year : str
            Year the book was published.
        available : bool
            Availability status of the book.
        """
        self.__id = book_id
        self.__title = title
        self.__author = author
        self.__release_year = release_year
        self.__available = available

    def __str__(self) -> str:
        """
        Return a string representation of the book.

        Returns
        -------
        str
            A formatted string with the book's title, author, year, and availability.
        """
        return f" ID: {self.id} | Titulo: {self.title} | Autor: ({self.author}) | Anno:  {self.year} | Disponible: {self.available}"

    def __eq__(self, other):
        """
        Compare two books for equality based on their IDs.

        Parameters
        ----------
        other : Book
            The book to compare against.

        Returns
        -------
        bool
            True if both books have the same ID, False otherwise.
        """
        if isinstance(other, Book):
            return self.__id == other.__id
        return False
