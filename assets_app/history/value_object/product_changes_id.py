"""Typed identifier for product change records.

This module defines :class:`ProductChangesId`, a branded, strongly-typed
identifier for :class:`history.entity.product_changes.ProductChanges` entities.
It specializes :class:`domain.value_object.domain_id.DomainId` with an
``int`` payload to prevent accidental mixing with other ``DomainId[int]`` types
(e.g., ``ProductId[int]``).

Why a branded ID?
    Using a distinct subclass for each identifier domain (``ProductChangesId``,
    ``ProductId``, etc.) increases type safety and readability across your code
    base, even if the underlying value type is the same.

Design notes:
    - This class intentionally contains no extra fields or behavior; it serves
      purely as a type brand. If you need additional constraints (e.g., only
      positive integers), override ``__init__`` and validate ``value`` there.
    - The base ``DomainId`` is a ``@dataclass`` in this project, so equality
      and representation are value-based by default.

Examples:
    >>> pcid = ProductChangesId(123)
    >>> pcid.get_value()
    123
    >>> # Distinct types prevent cross-assignment:
    ... from products.value_object.product_id import ProductId
    ... isinstance(pcid, ProductId)
    False
"""
from domain.value_object.domain_id import DomainId


class ProductChangesId(DomainId[int]):
    """Branded typed identifier for a product-inventory change record.

    Inherits:
        DomainId[int]: Provides the ``value`` storage and value-based equality.

    Usage:
        >>> ProductChangesId(1)  # doctest: +ELLIPSIS
        ProductChangesId(value=1)
    """
    pass
