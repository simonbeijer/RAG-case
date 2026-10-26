chat:
	cd backend && uv run python -m app.cli
setup:
	cd backend && uv sync

ingest:
	cd backend && uv run python -m app.ingest

test:
	cd backend && uv run pytest
api:
	cd backend && uv run uvicorn app.api:app --reload