#!/bin/bash
set -e

echo "=== Running Alembic migrations ==="
alembic -c alembic.ini upgrade head

echo "=== DATABASE_URL is $DATABASE_URL"

echo "=== Starting FastAPI ==="
exec uvicorn main:app --host 0.0.0.0 --port 8000
