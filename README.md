# Pyazo

Pyazo is a self-hosted screenshot and image upload utility. It allows you to take a screenshot of a part of your screen and automatically upload it to your own server. You can also directly upload an image from your computer.

It is comprised of a cross-platform client written in Python which defers the actual taking of the screenshot to the built-in OS tools (macOS and Windows) or common utilities (Linux distributions). The server is a RESTful Go API with support for basic user accounts and image management.

## Requirements

- Go >= 1.26
- PostgreSQL

## Configuration

Copy `.env-example` to `.env` and configure:

| Key               | Default               | Description                       |
| ----------------- | --------------------- | --------------------------------- |
| ENV               | production            | Set to development for debug mode |
| POSTGRES_USER     | pyazo                 | PostgreSQL username               |
| POSTGRES_PASSWORD |                       | PostgreSQL password               |
| POSTGRES_DB       | pyazo                 | Database name                     |
| POSTGRES_HOST     | localhost             | Database host                     |
| JWT_SECRET        |                       | JWT signing secret                |
| BLOCK_REGISTER    | true                  | Disable user registration         |
| IMAGES_PATH       | /images               | Image storage directory           |
| CORS_ORIGIN       | https://app.pyazo.com | Allowed CORS origin               |
| PORT              | 8000                  | HTTP listen port                  |

## Development

```bash
# Start PostgreSQL
docker compose up -d db

# Build
go build -o api ./cmd/

# Run
POSTGRES_PASSWORD=pyazo JWT_SECRET=secret BLOCK_REGISTER=false ./api

# Run tests
POSTGRES_PASSWORD=pyazo go test ./...
```

## Docker

```bash
docker compose build
docker compose up -d
```

Images are stored at the `IMAGES_PATH` volume (`/images` by default) and should be served by a reverse proxy.

## License and Credits

BSD 3-Clause
