"""Typed identifier value object.

This module defines :class:`DomainId[V]`, a lightweight, strongly-typed wrapper
around an underlying primitive or structured value used as an identifier.
It is commonly employed in Domain-Driven Design (DDD) to make entity/aggregate
IDs explicit and type-safe (e.g., ``UserId``, ``OrderId``), reducing accidental
mix-ups between unrelated identifiers that share the same primitive type.

Type Parameters:
    V: The underlying value type (e.g., ``int``, ``str``, ``uuid.UUID``, or a
       small immutable record).

Design Notes:
    - This class is a ``@dataclass`` to provide value-based equality,
      ordering (if enabled), and a helpful ``repr``. By default, instances are
      **mutable**; if you want immutable, hashable IDs, set
      ``@dataclass(frozen=True, slots=True)`` in your project.
    - The explicit ``__init__`` mirrors the dataclass-generated signature for
      clarity and to allow custom validation if needed. If you do not plan to
      extend it, you may remove the custom ``__init__`` and let ``@dataclass``
      generate one automatically.
    - Keep the underlying ``value`` small and immutable where possible (e.g.,
      ``int``, ``str``, ``UUID``) to preserve identifier semantics.

Examples:
    >>> from uuid import UUID
    >>> # Define branded ID types by subclassing with a concrete V:
    ... class UserId(DomainId[UUID]):
    ...     pass
    ...
    ... class OrderId(DomainId[int]):
    ...     pass
    ...
    ... uid = UserId(UUID("12345678-1234-5678-1234-567812345678"))
    ... oid = OrderId(42)
    ...
    ... uid.get_value() == uid.value
    True
    >>> # Value-based equality compares the wrapped 'value':
    ... UserId(UUID(int=1)) == UserId(UUID(int=1))
    True
"""

from typing import Generic, TypeVar
from dataclasses import dataclass

V = TypeVar("V")  # underlying value type for DomainId


@dataclass
class DomainId(Generic[V]):
    """Generic, typed identifier wrapper.

    Wraps a single value of type :data:`V` to represent a domain identifier.
    Using a dedicated type (e.g., ``UserId``) instead of bare primitives
    (``int``, ``str``) helps prevent accidental misrouting of IDs across
    domain boundaries.

    Attributes:
        value: The underlying identifier value of type :data:`V`.
    """

    value: V

    def __init__(self, value: V) -> None:
        """Initialize the identifier with its underlying value.

        Args:
            value: The concrete value that uniquely identifies a domain object.
                   Prefer immutable primitives (``int``, ``str``, ``UUID``).

        Notes:
            If validation or normalization is required (e.g., ensuring a
            non-empty string or canonical UUID format), implement it here
            before assigning to :attr:`value`.
        """
        self.value = value

    def get_value(self) -> V:
        """Return the underlying identifier value.

        Returns:
            The wrapped value of type :data:`V`.
        """
        return self.value
