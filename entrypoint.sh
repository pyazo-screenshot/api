#!/bin/sh
set -e

migrate -path=migrations/ -database postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:5432/$POSTGRES_DB?sslmode=disable up

exec .venv/bin/uvicorn pyazo_api.run:app --host 0.0.0.0 --workers 4
