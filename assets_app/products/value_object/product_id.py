"""Typed identifier for products.

This module defines :class:`ProductId`, a branded, strongly-typed identifier
for :class:`products.entity.product.Product` entities. It specializes
:class:`domain.value_object.domain_id.DomainId` with a ``str`` payload to
prevent accidental mixing with other ``DomainId[str]`` types (e.g., ``CustomerId``).

Why a branded ID?
    Using a distinct subclass for each identifier domain (``ProductId``,
    ``OrderId``, etc.) improves readability and type safety across your code
    base, even if the underlying value type is the same. For products, a
    string is common (SKU, UPC/EAN as text, or an internal code).

Design notes:
    - This class intentionally contains no extra fields or behavior; it serves
      purely as a type brand. If you need additional constraints (e.g., non-empty,
      specific SKU pattern), override ``__init__`` and validate ``value`` there.
    - The base ``DomainId`` in this project is a ``@dataclass`` (value-based
      equality and helpful ``repr`` by default). Consider ``frozen=True`` at the
      base if you want immutable, hashable IDs.

Examples:
    >>> pid = ProductId("SKU-ABC-001")
    >>> pid.get_value()
    'SKU-ABC-001'
    >>> # Distinct types prevent cross-assignment/mix-ups:
    ... class CustomerId(DomainId[str]): ...
    ...
    ... isinstance(pid, CustomerId)
    False
"""

from domain.value_object.domain_id import DomainId

class ProductId(DomainId[str]):
    """Branded typed identifier for a product.

    Inherits:
        DomainId[str]: Provides the ``value`` storage and value-based equality.

    Usage:
        >>> ProductId("SKU-ABC-001")  # doctest: +ELLIPSIS
        ProductId(value='SKU-ABC-001')
    """
    pass
