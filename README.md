# Pyazo

Pyazo is a self-hosted screenshot and image upload service.

This repository contains the full server application: a Go HTTP server with a server-rendered web UI, REST API endpoints for clients, PostgreSQL persistence, and filesystem image storage. There is no separate React frontend or nginx image-serving container required.

## Requirements

- Go 1.26 or newer
- PostgreSQL
- Docker, optional for local PostgreSQL and container deployment
- `exiftool`, optional and only used when uploads request `clear_metadata=true`

## Configuration

Configuration is read from environment variables.

| Key | Default | Description |
| --- | --- | --- |
| `ENV` | `production` | `development`, `testing`, or `production` |
| `POSTGRES_USER` | `pyazo` | PostgreSQL username |
| `POSTGRES_PASSWORD` | required | PostgreSQL password |
| `POSTGRES_DB` | `pyazo` | PostgreSQL database name |
| `POSTGRES_HOST` | `localhost` | PostgreSQL host |
| `JWT_SECRET` | required | JWT signing secret |
| `BLOCK_REGISTER` | `true` | Set to `false` to allow registration |
| `IMAGES_PATH` | `/images` | Directory where uploaded images are stored |
| `CORS_ORIGIN` | `https://app.pyazo.com` | Allowed CORS origin for API clients |
| `PORT` | `8000` | HTTP listen port |

Uploaded images are stored on disk under `IMAGES_PATH`. Database migrations run automatically on startup.

## Development

Start PostgreSQL:

```bash
docker compose up -d db
```

Run the server locally:

```bash
mkdir -p /tmp/pyazo-images

POSTGRES_USER=postgres \
POSTGRES_PASSWORD=postgres \
POSTGRES_DB=postgres \
JWT_SECRET=secret \
BLOCK_REGISTER=false \
IMAGES_PATH=/tmp/pyazo-images \
go run ./cmd/
```

Open `http://localhost:8000/register` to create a local user, then use `http://localhost:8000/` for the image list.

Useful commands:

```bash
make templ    # regenerate templ output
make build    # generate templates and build ./api
make lint     # generate templates, tidy check, vet, golangci-lint
make test     # generate templates and run tests with race detector
```

`make test` requires PostgreSQL. With the provided `compose.yaml`, the test defaults already match `postgres/postgres@localhost/postgres`.

## Deployment

Build the container:

```bash
docker build -t pyazo .
```

Run it with a persistent image volume and a reachable PostgreSQL database:

```bash
docker run -d \
  --name pyazo \
  -p 8000:8000 \
  -v pyazo-images:/images \
  -e POSTGRES_HOST=postgres.example.internal \
  -e POSTGRES_USER=pyazo \
  -e POSTGRES_PASSWORD=change-me \
  -e POSTGRES_DB=pyazo \
  -e JWT_SECRET=change-me \
  -e BLOCK_REGISTER=true \
  pyazo
```

The Go server serves:

- the web UI at `/`
- login/register/logout routes
- static assets from `/assets`
- uploaded images at `/{image-id.ext}`
- the REST API under `/auth` and `/images`

A reverse proxy is optional. Use one if you need TLS termination, public `:80`/`:443`, caching headers, rate limits, or centralized logs. The old frontend/nginx container is not required for serving the application or uploaded images.

Back up both PostgreSQL and the `IMAGES_PATH` directory. PostgreSQL stores users and image records; `IMAGES_PATH` stores the actual image files.

## API

Authentication endpoints:

- `POST /auth/login`
- `POST /auth/register`
- `GET /auth/me`

Image endpoints require `Authorization: Bearer <token>`:

- `POST /images` with multipart field `upload_file`
- `GET /images?page=0&limit=50`
- `DELETE /images/{id}`

The web UI uses an HttpOnly session cookie. API clients should continue using bearer tokens.

## License

BSD 3-Clause
