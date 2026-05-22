# AGENTS.md

Read `README.md` first for development, deployment, configuration, and API usage. This file is only for project facts an agent needs before editing.

## Project Shape

Pyazo is a single Go server. It serves the server-rendered web UI, REST API, static assets, and uploaded image files. There is no React frontend and no required nginx application container.

## Structure

```text
auth/           JWT creation/parsing and argon2id password hashing
assets/         CSS, small browser JS, logo, icons
cmd/            server entrypoint
config/         environment-backed Config and database URL construction
db/             pgx queries, models, migrations runner
http/           gin server, middleware, JSON API handlers, web page handlers
migrations/     embedded SQL migrations
pages/          templ sources and generated *_templ.go files
```

Route registration is in `http/server.go`.

## Dependencies

- Go 1.26
- gin for HTTP routing
- pgx for PostgreSQL
- golang-migrate for startup migrations
- templ for server-rendered HTML
- small plain JavaScript in `assets/app.js` for delete and infinite scroll
- PostgreSQL for runtime and HTTP tests
- optional `exiftool` for `clear_metadata=true` uploads

The templ CLI is versioned with the Go `tool` directive in `go.mod`. Run it with `go tool templ generate` or through `make templ`.

## Tooling

Use Makefile targets instead of ad-hoc commands:

```bash
make templ
make build
make lint
make test
```

`make lint` runs templ generation, `go mod tidy -diff`, `go vet`, `golangci-lint run`, and formatter diff checks.

`make test` runs templ generation and `go test -timeout=30s -race ./...`. It needs PostgreSQL; the local compose database uses `postgres/postgres@localhost/postgres`.

Do not edit generated `pages/*_templ.go` directly. Edit `pages/*.templ`, then run `make templ`, `make lint`, or `make test`.

## Auth And Serving Notes

The JSON API uses bearer JWTs. The web UI uses the same JWT in an HttpOnly `pyazo_token` cookie.

Uploaded files are served by Go from `IMAGES_PATH` through `ServeImageFile` as a fallback route. Keep `/auth`, `/images`, `/web/images`, `/assets`, `/login`, `/register`, and `/logout` reserved for application routes.
