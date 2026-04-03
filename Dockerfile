FROM golang:1.26-trixie AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o /pyazo ./cmd/

FROM debian:trixie-slim

EXPOSE 8000

COPY --from=builder /pyazo /pyazo
ENTRYPOINT ["/pyazo"]
