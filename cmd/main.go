package main

import (
	"context"
	"errors"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

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
		slog.SetDefault(slog.New(slog.NewTextHandler(os.Stdout, nil)))
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

	srv := &http.Server{
		Addr:    addr,
		Handler: s.Router,
	}

	go func() {
		slog.Info("server starting", "addr", addr)
		if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			slog.Error("server failed", "error", err)
			os.Exit(1)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	slog.Info("shutting down server")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		slog.Error("server forced to shutdown", "error", err)
		os.Exit(1)
	}
}
