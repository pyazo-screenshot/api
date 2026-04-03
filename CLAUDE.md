# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pyazo API is a self-hosted screenshot and image upload service backend built with Go (gin + pgx). It provides REST endpoints for user authentication and image management.

## Development Commands

```bash
# Build
go build -o api ./cmd/

# Run (requires PostgreSQL)
POSTGRES_PASSWORD=pyazo JWT_SECRET=secret BLOCK_REGISTER=false ./api

# Run tests (requires PostgreSQL)
POSTGRES_PASSWORD=pyazo go test ./...

# Start PostgreSQL for local development
docker compose up -d db
```

## Architecture

Flat package structure with protocol-layer separation:

```
auth/           # JWT and argon2id password hashing (passlib-compatible)
config/         # Config struct loaded from env vars
db/             # pgx queries, User/Image structs
http/           # gin handlers, middleware, server setup
cmd/api/        # Entrypoint, embedded migrations
migrations/     # SQL migration files (golang-migrate)
```

## Database

- PostgreSQL with pgx + connection pooling
- Migrations embedded in binary, run on startup via golang-migrate
- Two tables: `users` (id, username, hashed_password) and `images` (id, owner_id, created_at)

## Configuration

Environment variables (see `config/config.go`):

- `ENV`: development/testing/production
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`
- `JWT_SECRET`, `BLOCK_REGISTER`, `IMAGES_PATH`
- `CORS_ORIGIN`, `PORT`
