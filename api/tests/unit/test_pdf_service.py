import sys
from types import ModuleType
from unittest.mock import MagicMock

import pytest

from aracc.models.investigation import Annotation, InvestigationResponse, Tag

FAKE_PDF = b"%PDF-1.4 fake pdf content for testing"


def _make_investigation(**overrides: object) -> InvestigationResponse:
    defaults = {
        "id": "inv-1",
        "title": "Test Investigation",
        "description": "Test description",
        "created_at": "2026-01-15T10:00:00Z",
        "updated_at": "2026-01-15T10:00:00Z",
        "entity_ids": [],
        "share_token": None,
    }
    defaults.update(overrides)
    return InvestigationResponse(**defaults)  # type: ignore[arg-type]


def _make_annotation(**overrides: object) -> Annotation:
    defaults = {
        "id": "ann-1",
        "entity_id": "ent-1",
        "investigation_id": "inv-1",
        "text": "Annotation text",
        "created_at": "2026-01-15T12:00:00Z",
    }
    defaults.update(overrides)
    return Annotation(**defaults)  # type: ignore[arg-type]


def _make_tag(**overrides: object) -> Tag:
    defaults = {
        "id": "tag-1",
        "investigation_id": "inv-1",
        "name": "reviewed",
        "color": "#3498db",
    }
    defaults.update(overrides)
    return Tag(**defaults)  # type: ignore[arg-type]


@pytest.fixture(autouse=True)
def _mock_weasyprint() -> object:  # type: ignore[misc]
    """Install a fake weasyprint module so tests run without system libraries."""
    mock_html_cls = MagicMock()
    mock_html_cls.return_value.write_pdf.return_value = FAKE_PDF

    fake_module = ModuleType("weasyprint")
    fake_module.HTML = mock_html_cls  # type: ignore[attr-defined]

    sys.modules["weasyprint"] = fake_module
    yield
    sys.modules.pop("weasyprint", None)


@pytest.mark.anyio
async def test_render_pdf_produces_valid_pdf() -> None:
    from aracc.services.pdf_service import render_investigation_pdf

    investigation = _make_investigation()
    annotations = [_make_annotation()]
    tags = [_make_tag()]
    entities = [{"name": "Test Entity", "type": "Person", "document": "***.***.***-34"}]

    result = await render_investigation_pdf(
        investigation, annotations, tags, entities, lang="pt"
    )

    assert isinstance(result, bytes)
    assert result[:5] == b"%PDF-"


@pytest.mark.anyio
async def test_render_pdf_handles_empty_data() -> None:
    from aracc.services.pdf_service import render_investigation_pdf

    investigation = _make_investigation(description=None)

    result = await render_investigation_pdf(investigation, [], [], [], lang="pt")

    assert isinstance(result, bytes)
    assert result[:5] == b"%PDF-"


@pytest.mark.anyio
async def test_render_pdf_lang_pt() -> None:
    from aracc.services.pdf_service import render_investigation_pdf

    investigation = _make_investigation()

    result = await render_investigation_pdf(investigation, [], [], [], lang="pt")

    assert isinstance(result, bytes)
    assert result[:5] == b"%PDF-"


@pytest.mark.anyio
async def test_render_pdf_lang_en() -> None:
    from aracc.services.pdf_service import render_investigation_pdf

    investigation = _make_investigation()

    result = await render_investigation_pdf(investigation, [], [], [], lang="en")

    assert isinstance(result, bytes)
    assert result[:5] == b"%PDF-"
