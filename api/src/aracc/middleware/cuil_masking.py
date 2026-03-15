"""Middleware that masks CUIL/CUIT numbers in API responses to protect personal data.

CUIL (Clave Unica de Identificacion Laboral) is an 11-digit Argentine tax ID for persons.
CUIT (Clave Unica de Identificacion Tributaria) is an 11-digit Argentine tax ID for companies.
Both share the format: XX-XXXXXXXX-X.
Politically Exposed Persons (PEPs) have their CUILs kept visible.
"""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, StreamingResponse

from aracc.constants import PEP_ROLES

if TYPE_CHECKING:
    from starlette.middleware.base import RequestResponseEndpoint
    from starlette.requests import Request

# Matches 11-digit CUIL/CUIT in formatted (XX-XXXXXXXX-X) or raw (XXXXXXXXXXX) form.
# Uses negative lookbehind/lookahead to avoid matching inside longer digit sequences.
_CUIL_FORMATTED = re.compile(r"\d{2}-\d{8}-\d")
_CUIL_RAW = re.compile(r"(?<!\d)\d{11}(?!\d)")


def mask_formatted_cuil(cuil: str) -> str:
    """Mask a formatted CUIL/CUIT, keeping only the last 4 visible digits.

    Example: 20-12345678-9 -> **-*****678-9
    """
    return f"**-*****{cuil[8:]}"


def mask_raw_cuil(cuil: str) -> str:
    """Mask a raw 11-digit CUIL/CUIT, keeping only the last 4 digits.

    Example: 20123456789 -> *******6789
    """
    return f"*******{cuil[7:]}"


def _is_pep_record(record: dict[str, Any]) -> bool:
    """Determine whether a JSON record describes a PEP.

    Checks for explicit ``is_pep`` boolean or political keywords in the
    ``role`` / ``cargo`` fields.
    """
    if record.get("is_pep") is True:
        return True

    for field in ("role", "cargo"):
        value = record.get(field)
        if isinstance(value, str) and any(kw in value.strip().lower() for kw in PEP_ROLES):
            return True

    return False


def _collect_pep_cuils(data: Any) -> set[str]:
    """Walk a JSON structure and return the set of CUIL/CUIT strings belonging to PEPs."""
    pep_cuils: set[str] = set()

    if isinstance(data, dict):
        if _is_pep_record(data):
            for field in ("cuil", "cuit"):
                cuil_val = data.get(field)
                if isinstance(cuil_val, str) and cuil_val:
                    # Normalise to digits-only for comparison.
                    pep_cuils.add(re.sub(r"\D", "", cuil_val))
        for value in data.values():
            pep_cuils |= _collect_pep_cuils(value)
    elif isinstance(data, list):
        for item in data:
            pep_cuils |= _collect_pep_cuils(item)

    return pep_cuils


def _digits_only(cuil: str) -> str:
    return re.sub(r"\D", "", cuil)


def mask_cuils_in_json(text: str, pep_cuils: set[str] | None = None) -> str:
    """Replace CUIL/CUIT patterns in *text* with masked versions.

    CUILs/CUITs whose digits-only form appears in *pep_cuils* are left untouched.
    """
    safe: set[str] = pep_cuils or set()

    def _replace_formatted(m: re.Match[str]) -> str:
        if _digits_only(m.group()) in safe:
            return m.group()
        return mask_formatted_cuil(m.group())

    def _replace_raw(m: re.Match[str]) -> str:
        if m.group() in safe:
            return m.group()
        return mask_raw_cuil(m.group())

    text = _CUIL_FORMATTED.sub(_replace_formatted, text)
    text = _CUIL_RAW.sub(_replace_raw, text)
    return text


class CUILMaskingMiddleware(BaseHTTPMiddleware):
    """Starlette middleware that masks CUIL/CUIT numbers in JSON responses."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type:
            return response

        # Read the full body from the streaming response.
        body_bytes = b""
        if isinstance(response, StreamingResponse):
            chunks: list[bytes] = []
            async for chunk in response.body_iterator:
                if isinstance(chunk, str):
                    chunks.append(chunk.encode("utf-8"))
                elif isinstance(chunk, bytes):
                    chunks.append(chunk)
                else:
                    chunks.append(bytes(chunk))
            body_bytes = b"".join(chunks)
        else:
            body_bytes = getattr(response, "body", b"")

        if not body_bytes:
            return response

        body_text = body_bytes.decode("utf-8")

        # Parse JSON to discover PEP CUILs, then mask the rest.
        pep_cuils: set[str] = set()
        try:
            data = json.loads(body_text)
            pep_cuils = _collect_pep_cuils(data)
        except (json.JSONDecodeError, TypeError):
            pass

        masked_text = mask_cuils_in_json(body_text, pep_cuils)
        masked_bytes = masked_text.encode("utf-8")

        return Response(
            content=masked_bytes,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
