FROM golang:1.26-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o /pyazo ./cmd/

FROM alpine:3.23

EXPOSE 8000

COPY --from=builder /pyazo /pyazo
ENTRYPOINT ["/pyazo"]
