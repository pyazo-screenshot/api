FROM python:3.10-bullseye AS builder

WORKDIR /app
ENV PATH="/root/.local/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && python -m venv .venv \
    && poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root --no-interaction

COPY pyazo_api/ ./pyazo_api/
RUN set -x \
    && poetry install --no-dev --no-interaction \
    && rm -rf pyazo_api.egg-info


FROM python:3.10-slim-bullseye

EXPOSE 8000
WORKDIR /app
ENTRYPOINT ["pyazo_api/entrypoint.sh"]
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

RUN mkdir -p media/private media/public \
    && apt update \
    && apt install -y postgresql-client-13 \
    && rm -rf /var/lib/apt/lists/* \
    && apt clean

COPY --from=builder /app/ ./
