.PHONY: all fmt lint test build

bin:
	mkdir bin
bin/golangci-lint: bin
	GOBIN=$(PWD)/bin go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@v2.11.4

fmt:
	go mod tidy
	bin/golangci-lint fmt

lint: bin/golangci-lint
	go mod tidy -diff
	go vet ./...
	bin/golangci-lint run
	bin/golangci-lint fmt -d

test:
	go test -timeout=30s -race ./...
