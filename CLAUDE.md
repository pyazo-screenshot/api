# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pyazo API is a self-hosted screenshot and image upload service backend built with FastAPI. It provides REST endpoints for user authentication and image management with support for public image storage.

## Development Commands

```bash
# Install dependencies (uses uv)
uv sync

# Run development server
uvicorn pyazo_api.run:app --reload

# Run tests (requires PostgreSQL - see pytest.ini for test env config)
pytest

# Run single test
pytest tests/test_images.py::test_name

# Seed database with test data
python -m pyazo_api.seed

# Start PostgreSQL for local development
docker compose up -d db
```

## Architecture

The codebase follows a layered domain-driven architecture:

```
pyazo_api/
├── application/          # FastAPI app setup and HTTP layer
│   ├── __init__.py       # create_app() with lifespan, CORS, router registration
│   ├── db.py             # Connection pool (psycopg_pool) with lifespan management
│   └── routers/          # API route handlers (auth, images)
├── domain/               # Business logic layer
│   ├── auth/             # Authentication domain
│   │   ├── actions/      # login_action.py, register_action.py
│   │   ├── repository.py # UserRepository
│   │   └── dto.py        # User DTOs (User, UserGet, UserCredentials, etc.)
│   └── images/           # Images domain
│       ├── actions/      # save_image.py, get_images.py, delete_image.py
│       ├── repository.py # ImageRepository
│       └── dto.py        # Image DTO
├── config/               # Pydantic Settings configuration
│   ├── __init__.py       # Exports `settings` singleton
│   └── settings.py       # Settings class with env var loading
└── util/                 # Shared utilities (pagination, auth helpers, http_exceptions)
```

**Key Patterns:**

- **Actions**: Business logic encapsulated in action classes with FastAPI `Depends()` injection
- **Repositories**: Data access layer using raw SQL with psycopg3 async connection pool
- **DTOs**: Pydantic models for data transfer; `User.to_public()` converts to `UserGet`
- **Database**: Async connection pool via `psycopg_pool.AsyncConnectionPool` managed by FastAPI lifespan
- **Configuration**: `pydantic-settings` with automatic `.env` file loading

## Database

- PostgreSQL with psycopg3 async + connection pooling
- Migrations in `migrations/` (plain SQL files)
- Two tables: `users` (id, username, hashed_password) and `images` (id, owner_id, created_at)

## Configuration

Uses `pydantic-settings` for type-safe configuration. Settings loaded from environment variables and `.env` file.

Key settings (see `config/settings.py`):

- `ENV`: development/testing/production
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`
- `JWT_SECRET`, `JWT_ALGORITHM`
- `BLOCK_REGISTER`: Boolean to disable registration
- `IMAGES_PATH`: Image storage directory
