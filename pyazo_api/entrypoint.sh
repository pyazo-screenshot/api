#!/bin/sh

python pyazo_api/migrate.py
exec uvicorn pyazo_api.run:app --host 0.0.0.0 --workers 4
