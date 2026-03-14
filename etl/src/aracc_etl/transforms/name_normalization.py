import re
import unicodedata


def _remove_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_name(name: str | None) -> str:
    if not name:
        return ""
    result = name.strip().upper()
    result = _remove_accents(result)
    # Collapse multiple whitespace
    result = re.sub(r"\s+", " ", result)
    return result
