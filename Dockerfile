FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev;

COPY pyazo_api/ ./pyazo_api/
RUN uv sync --frozen --no-dev;

FROM python:3.13-slim-trixie

EXPOSE 8000
WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]
ENV PYTHONUNBUFFERED=1
VOLUME /images

COPY --from=migrate/migrate /usr/local/bin/migrate /usr/bin/migrate

RUN apt update \
    && apt install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/* \
    && apt clean;

COPY migrations/ ./migrations/
COPY entrypoint.sh /entrypoint.sh
COPY --from=builder /app/ ./
