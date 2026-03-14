from typing import Any


def deduplicate_rows(
    rows: list[dict[str, Any]],
    key_fields: list[str],
) -> list[dict[str, Any]]:
    seen: set[tuple[Any, ...]] = set()
    result: list[dict[str, Any]] = []
    for row in rows:
        key = tuple(row.get(f) for f in key_fields)
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result
