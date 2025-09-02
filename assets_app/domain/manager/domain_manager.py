"""Application service manager base class.

This module defines :class:`Manager[R]`, a thin, typed façade for application
services that orchestrate domain operations using a repository. It follows a
common layering in Domain-Driven Design (DDD):

    UI/API  ->  Manager (application service)  ->  Repository  ->  Storage

Type Parameters:
    R: The concrete repository type used by the manager. ``R`` is bounded to
       ``DomainRepository[Any, Any]`` in your codebase (e.g., ``UserRepository``,
       ``OrderRepository``).

Example:
    >>> from dataclasses import dataclass
    >>> from typing import Any, List, Optional, Generic, TypeVar
    >>>
    >>> # Minimal stubs mirroring your project’s abstractions:
    ... K = TypeVar("K")
    ... E = TypeVar("E")
    ...
    ... class DomainId(Generic[K]):  # pragma: no cover - example only
    ...     def __init__(self, value: K) -> None:
    ...         self.value = value
    ...
    ... class DomainEntity(Generic[K]):  # pragma: no cover - example only
    ...     def __init__(self, id: DomainId[Any]) -> None:
    ...         self.id = id
    ...
    ... class DomainRepository(Generic[K, E]):  # pragma: no cover - example only
    ...     def __init__(self, filename: str) -> None:
    ...         self.filename = filename
    ...     def save_all(self, entities: List[E]) -> None: ...
    ...     def get_all(self) -> List[E]: ...
    ...     def get_by_id(self, id: K) -> Optional[E]: ...
    ...     def update(self, entity: E) -> None: ...
    ...     def delete(self, id: K) -> None: ...
    ...
    ... # Concrete domain types:
    ... class UserId(DomainId[int]): ...
    ...
    ... @dataclass
    ... class User(DomainEntity[UserId]):
    ...     name: str
    ...     def __init__(self, id: UserId, name: str) -> None:
    ...         super().__init__(id)
    ...         self.name = name
    ...
    ... # Concrete repository and manager:
    ... class InMemoryUserRepo(DomainRepository[UserId, User]):
    ...     def __init__(self) -> None:
    ...         super().__init__(filename=":memory:")
    ...         self._items: dict[int, User] = {}
    ...     def save_all(self, entities: List[User]) -> None:
    ...         for e in entities:
    ...             self._items[e.id.value] = e
    ...     def get_all(self) -> List[User]:
    ...         return list(self._items.values())
    ...     def get_by_id(self, id: UserId) -> Optional[User]:
    ...         return self._items.get(id.value)
    ...     def update(self, entity: User) -> None:
    ...         self._items[entity.id.value] = entity
    ...     def delete(self, id: UserId) -> None:
    ...         self._items.pop(id.value, None)
    ...
    ... class UserManager(Manager[InMemoryUserRepo]):
    ...     def list_users(self) -> list[User]:
    ...         return self.repository.get_all()
    ...
    ... repo = InMemoryUserRepo()
    ... mgr = UserManager(repo)
    ... repo.save_all([User(UserId(1), "Alice")])
    ... [u.name for u in mgr.list_users()]
    ['Alice']
"""


from abc import ABC
from typing import Generic, TypeVar

R = TypeVar("R", bound="DomainRepository[Any, Any]")  # repository type

class Manager(Generic[R], ABC):
    """Abstract base class for application-service managers.

    A manager coordinates high-level use cases by delegating persistence
    operations to a repository of type :data:`R`.

    Attributes:
        repository: The repository instance used to load and persist domain
            entities as part of application workflows.
    """
    repository: R

    def __init__(self, repository: R) -> None:
        """Initialize the manager with its backing repository.

        Args:
            repository: The concrete repository instance that this manager
                will use to perform data access as part of its use cases.
        """
        self.repository = repository

