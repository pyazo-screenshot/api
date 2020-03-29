#!/bin/sh

cd pyazo_api
alembic upgrade head
cd ..
uvicorn pyazo_api.run:app --host 0.0.0.0