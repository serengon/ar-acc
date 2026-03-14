import re


def strip_document(doc: str | None) -> str:
    if not doc:
        return ""
    return re.sub(r"[^0-9]", "", doc)


def format_cuil(cuil: str | None) -> str:
    """Format CUIL as XX-XXXXXXXX-X (persons)."""
    digits = strip_document(cuil)
    if len(digits) != 11:
        return digits
    return f"{digits[:2]}-{digits[2:10]}-{digits[10:]}"


def format_cuit(cuit: str | None) -> str:
    """Format CUIT as XX-XXXXXXXX-X (companies). Same structure as CUIL."""
    return format_cuil(cuit)


# Legacy aliases for international pipelines
format_cpf = format_cuil
format_cnpj = format_cuit


def _cuil_cuit_check_digit(digits: str) -> bool:
    """Validate CUIL/CUIT check digit (modulus 11 algorithm).

    CUIL (persons) and CUIT (companies) share the same XX-XXXXXXXX-X format.
    """
    if len(digits) != 11:
        return False
    weights = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(digits[i]) * weights[i] for i in range(10))
    remainder = 11 - (total % 11)
    if remainder == 11:
        expected = 0
    elif remainder == 10:
        expected = 9
    else:
        expected = remainder
    return int(digits[10]) == expected


def validate_cuil(cuil: str | None) -> bool:
    digits = strip_document(cuil)
    return _cuil_cuit_check_digit(digits)


def validate_cuit(cuit: str | None) -> bool:
    digits = strip_document(cuit)
    return _cuil_cuit_check_digit(digits)


# Legacy aliases
validate_cpf = validate_cuil
validate_cnpj = validate_cuit


def classify_document(doc: str | None) -> str:
    """Classify an Argentine document string for identity handling.

    Returns one of:
    - cuil_valid: 11-digit CUIL (persons, prefix 20/23/24/27)
    - cuit_valid: 11-digit CUIT (companies, prefix 30/33/34)
    - dni: 7-8 digit DNI
    - invalid: anything else
    """
    raw = (doc or "").strip()
    digits = strip_document(raw)

    if len(digits) == 11:
        prefix = digits[:2]
        if prefix in {"30", "33", "34"}:
            return "cuit_valid"
        return "cuil_valid"
    if len(digits) in {7, 8}:
        return "dni"
    return "invalid"
