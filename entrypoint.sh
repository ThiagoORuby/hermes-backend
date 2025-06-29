#!/bin/sh

poetry run alembic upgrade head

poetry run uvicorn api.app.app:app --host 0.0.0.0 --port 8000
