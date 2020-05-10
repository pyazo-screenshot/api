#!/bin/sh

uvicorn pyazo_api.run:app --host 0.0.0.0 --workers 4
