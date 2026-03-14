"""Sanitize monetary values from government data sources.

Some sources (notably PNCP) contain data-entry errors where municipal
officials entered values 1000x-1000000x too high. These outliers
distort any aggregation (sum, average) downstream.
"""

from __future__ import annotations

# R$ 10 billion — largest legitimate single contract is ~R$ 1-5B
# (multi-year defense/infrastructure). p99.99 of PNCP ≈ R$ 714M.
MAX_CONTRACT_VALUE: float = 10_000_000_000.0


def cap_contract_value(value: float | None) -> float | None:
    """Return None for values above threshold (source data entry errors).

    Values above MAX_CONTRACT_VALUE are replaced with None so that
    downstream aggregations (sum, avg) skip them. The original value
    should be preserved in a ``raw_value`` field for auditability.
    """
    if value is None:
        return None
    if value > MAX_CONTRACT_VALUE:
        return None
    return value
