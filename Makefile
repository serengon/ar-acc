.PHONY: dev stop api etl frontend lint type-check test test-api test-etl test-frontend check seed clean

# ── Development ─────────────────────────────────────────
setup-env:
	bash scripts/init_env.sh

dev:
	docker compose up -d

stop:
	docker compose down

# ── API ─────────────────────────────────────────────────
api:
	cd api && uv run uvicorn aracc.main:app --reload --host 0.0.0.0 --port 8000

# ── ETL ─────────────────────────────────────────────────
etl:
	cd etl && uv run aracc-etl --help

etl-sources:
	cd etl && uv run aracc-etl sources

seed:
	bash infra/scripts/seed-dev.sh

# ── Frontend ────────────────────────────────────────────
frontend:
	cd frontend && npm run dev

# ── Quality ─────────────────────────────────────────────
lint:
	cd api && uv run ruff check src/ tests/
	cd etl && uv run ruff check src/ tests/
	cd frontend && npm run lint

type-check:
	cd api && uv run mypy src/
	cd etl && uv run mypy src/
	cd frontend && npm run type-check

test-api:
	cd api && uv run pytest

test-etl:
	cd etl && uv run pytest

test-frontend:
	cd frontend && npm test

test: test-api test-etl test-frontend

check: lint type-check test
	@echo "All checks passed."

# ── Cleanup ─────────────────────────────────────────────
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf frontend/dist
