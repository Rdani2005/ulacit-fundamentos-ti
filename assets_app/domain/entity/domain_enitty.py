"""Domain entity base class.

This module provides a minimal, strongly-typed base class for Domain-Driven
Design (DDD) entities that are identified by a typed identifier.

Terminology:
    - *Entity*: An object defined by its identity rather than by its attributes.
    - *Identifier (Id)*: A stable, unique key that distinguishes one entity
      from another.

Type parameters:
    K: The identifier type for the entity. This should be a subtype of
       ``DomainId[Any]`` in your codebase (e.g., ``UserId``, ``OrderId``).

Notes:

Example:
    >>> # Assuming you have a generic DomainId type similar to:
    ... # class DomainId(Generic[T]): ...  This module intentionally does not prescribe equality or hashing semantics.
    In many DDD codebases, entity equality is defined by comparing identifiers
    (e.g., two entities are equal if their IDs are equal). Implement that logic
    in concrete subclasses (e.g., by overriding ``__eq__`` / ``__hash__``) to
    match your domain’s conventions.

    ...
    ... # A concrete id type:
    ... class UserId:  # typically extends DomainId[int]
    ...     def __init__(self, value: int) -> None:
    ...         self.value = value
    ...
    ... # A concrete entity:
    ... class User(DomainEntity["UserId"]):
    ...     def __init__(self, id: "UserId", name: str) -> None:
    ...         super().__init__(id)
    ...         self.name = name
    ...
    ... uid = UserId(1)
    ... user = User(uid, "Alice")
    ... user.get_id() is uid
    True
"""

from abc import ABC
from typing import Generic, TypeVar

# K is the type of the entity's identifier (key).
# It is expected to be a subtype of DomainId[Any] in project.
K = TypeVar("K", bound="DomainId[Any]")  # key/id type

class DomainEntity(Generic[K], ABC):
    """Abstract base class for domain entities identified by a typed key.

    This class models the minimal contract for DDD entities: each entity owns
    an identifier of type ``K``. Subclasses can extend behavior and add domain
    attributes/operations as needed.

    Attributes:
        id: The unique identifier for this entity (type ``K``).
    """
    id: K

    def __init__(self, id: K) -> None:
        """Initialize the entity with its unique identifier.

        Args:
            id: The unique identifier of this entity.

        Notes:
            The parameter name ``id`` intentionally matches the attribute name.
            Although this shadows Python’s built-in ``id()`` function within the
            scope of this method, it is conventional and clear in DDD contexts.
        """
        self.id = id

    def get_id(self) -> K:
        """Return this entity's unique identifier.

        Returns:
            The identifier of type ``K`` associated with this entity.
        """
        return self.id
