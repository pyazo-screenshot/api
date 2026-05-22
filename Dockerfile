FROM golang:1.26-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go tool templ generate && go build -o /pyazo ./cmd/

FROM alpine:3.23

EXPOSE 8000

COPY --from=builder /pyazo /pyazo
COPY --from=builder /app/assets /assets
ENTRYPOINT ["/pyazo"]
