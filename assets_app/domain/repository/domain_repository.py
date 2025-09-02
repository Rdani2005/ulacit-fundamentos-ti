"""Generic repository abstraction for domain entities.

This module defines :class:`DomainRepository[K, E]`, an abstract base class
implementing the Repository pattern for Domain-Driven Design (DDD). A
repository provides a collection-like interface for loading and persisting
domain entities without exposing storage details.

Type Parameters:
    K: The identifier type for entities handled by the repository. This is
       expected to be a subtype of ``DomainId[Any]`` in your codebase (e.g.,
       ``UserId``, ``OrderId``).
    E: The entity type handled by the repository. This is expected to be a
       subtype of ``DomainEntity[Any]`` (e.g., ``User``, ``Order``).

Design Notes:
    - The attribute :attr:`filename` is provided as a convenient storage handle
      for file-backed implementations (e.g., JSON, CSV). Non-file
      implementations (e.g., SQL, NoSQL, in-memory) may still accept and ignore
      this argument or reinterpret it as a connection string / DSN.
    - Concrete subclasses must implement the abstract methods to define how
      entities are persisted and retrieved.
    - Equality / identity semantics for updates are intentionally unspecified.
      Typical implementations use the entity's id (:attr:`DomainEntity.id`) to
      locate existing records.

Example:
    >>> from typing import Any, Optional, List
    >>> from dataclasses import dataclass
    >>>
    >>> # Minimal stubs to illustrate usage:
    ... class DomainId(Generic[Any]):  # pragma: no cover - example only
    ...     def __init__(self, value: Any) -> None:
    ...         self.value = value
    ...
    ... class DomainEntity(Generic[Any]):  # pragma: no cover - example only
    ...     def __init__(self, id: DomainId[Any]) -> None:
    ...         self.id = id
    ...
    ... @dataclass
    ... class User(DomainEntity["UserId"]):  # pragma: no cover - example only
    ...     name: str
    ...     def __init__(self, id: "UserId", name: str) -> None:
    ...         super().__init__(id)
    ...         self.name = name
    ...
    ... class UserId(DomainId[int]):  # pragma: no cover - example only
    ...     pass
    ...
    ... class InMemoryUserRepo(DomainRepository["UserId", User]):
    ...     def __init__(self) -> None:
    ...         super().__init__(filename=":memory:")
    ...         self._items: dict[int, User] = {}
    ...
    ...     def save_all(self, entities: List[User]) -> None:
    ...         for e in entities:
    ...             self._items[e.id.value] = e
    ...
    ...     def get_all(self) -> List[User]:
    ...         return list(self._items.values())
    ...
    ...     def get_by_id(self, id: "UserId") -> Optional[User]:
    ...         return self._items.get(id.value)
    ...
    ...     def update(self, entity: User) -> None:
    ...         if entity.id.value not in self._items:
    ...             raise KeyError("Entity not found")
    ...         self._items[entity.id.value] = entity
    ...
    ...     def delete(self, id: "UserId") -> None:
    ...         self._items.pop(id.value, None)
"""

from abc import abstractmethod, ABC
from typing import Generic, Optional, TypeVar, List

K = TypeVar("K", bound="DomainId[Any]")  # key/id type
E = TypeVar("E", bound="DomainEntity[Any]")  # entity type

class DomainRepository(Generic[K, E], ABC):
    """Abstract base class for repositories of domain entities.

    Concrete implementations encapsulate the persistence mechanism for
    entities of type :data:`E`, identified by keys of type :data:`K`.

    Attributes:
        filename: A storage locator hint, typically a filesystem path for
            file-backed repositories. Implementations may ignore or reinterpret
            this value.

    Lifecycle:
        Subclasses should initialize storage resources in ``__init__`` and
        release them as appropriate (context manager support may be added
        by subclasses if needed).
    """
    filename: str

    def __init__(self, filename: str) -> None:
        """Create a repository configured with a storage locator.

        Args:
            filename: Path or locator for the underlying storage. For example,
                a JSON file path, an SQLite filename, or a symbolic value such
                as ``':memory:'`` for in-memory implementations.
        """
        self.filename = filename

    @abstractmethod
    def save_all(self, entities: List[E]) -> None:
        """Persist a collection of entities, inserting or replacing as needed.

        Implementations should write all provided entities atomically when
        possible to avoid partial saves.

        Args:
            entities: The list of entities to persist.

        Raises:
            IOError: If an underlying I/O error occurs during persistence.
            ValueError: If entities contain invalid data for the storage layer.
        """
        ...

    @abstractmethod
    def get_all(self) -> List[E]:
        """Return all entities present in the repository.

        Implementations should return an empty list if no entities are stored.

        Returns:
            A list of all stored entities.

        Raises:
            IOError: If an underlying I/O error occurs during retrieval.
        """
        ...

    @abstractmethod
    def get_by_id(self, id: K) -> Optional[E]:
        """Retrieve a single entity by its identifier.

        Args:
            id: The typed identifier of the entity to fetch.

        Returns:
            The matching entity if found; otherwise ``None``.

        Raises:
            IOError: If an underlying I/O error occurs during retrieval.
        """
        ...

    @abstractmethod
    def update(self, entity: E) -> None:
        """Update an existing entity in the repository.

        Implementations should locate the stored record using the entity's id
        and replace it with the provided data.

        Args:
            entity: The updated entity to persist.

        Raises:
            KeyError: If the entity does not exist.
            IOError: If an underlying I/O error occurs during persistence.
            ValueError: If the entity is invalid for the storage layer.
        """
        ...

    @abstractmethod
    def delete(self, id: K) -> None:
        """Remove an entity from the repository by its identifier.

        Args:
            id: The typed identifier of the entity to delete.

        Raises:
            KeyError: If no entity with the given id exists.
            IOError: If an underlying I/O error occurs during mutation.
        """
        ...