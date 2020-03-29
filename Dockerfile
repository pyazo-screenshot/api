FROM python:3.8-alpine AS builder

WORKDIR /app
ENV PATH="/root/.poetry/bin:$PATH"

RUN apk add --no-cache build-base git libffi-dev curl postgresql-dev \
  && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
  && python -m venv .venv \
  && poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root --no-interaction

COPY pyazo_api/ ./pyazo_api/
RUN set -x \
  && poetry install --no-dev --no-interaction \
  && rm -rf pyazo_api.egg-info


FROM python:3.8-alpine

EXPOSE 8000
WORKDIR /app
CMD ["sh", "pyazo_api/entrypoint.sh"]
ENV PATH="/app/.venv/bin:$PATH" \
  PYTHONUNBUFFERED=1

RUN apk add --no-cache libc-dev binutils libpq && mkdir /public

COPY --from=builder /app/ ./
