package main

import (
	"context"
	"log/slog"
	"os"

	"github.com/pyazo-screenshot/api/config"
	"github.com/pyazo-screenshot/api/db"
	pyhttp "github.com/pyazo-screenshot/api/http"
)

func main() {
	cfg, err := config.Load()
	if err != nil {
		slog.Error("config", "error", err)
		os.Exit(1)
	}

	if cfg.Env == "production" {
		slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stdout, nil)))
	}

	if err := db.RunMigrations(cfg.DatabaseURL()); err != nil {
		slog.Error("failed to run migrations", "error", err)
		os.Exit(1)
	}

	pool, err := db.NewPool(context.Background(), cfg.DatabaseURL())
	if err != nil {
		slog.Error("failed to connect to database", "error", err)
		os.Exit(1)
	}
	defer pool.Close()

	s := pyhttp.NewServer(pool, cfg)
	addr := ":" + cfg.Port
	slog.Info("server starting", "addr", addr)
	if err := s.Router.Run(addr); err != nil {
		slog.Error("server failed", "error", err)
		os.Exit(1)
	}
}
