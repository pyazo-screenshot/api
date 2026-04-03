package main

import (
	"context"
	"log"

	"github.com/golang-migrate/migrate/v4"
	_ "github.com/golang-migrate/migrate/v4/database/postgres"
	"github.com/golang-migrate/migrate/v4/source/iofs"
	"github.com/pyazo-screenshot/api/config"
	"github.com/pyazo-screenshot/api/db"
	pyhttp "github.com/pyazo-screenshot/api/http"
	"github.com/pyazo-screenshot/api/migrations"
)

func main() {
	cfg := config.Load()

	runMigrations(cfg.DatabaseURL())

	pool, err := db.NewPool(context.Background(), cfg.DatabaseURL())
	if err != nil {
		log.Fatal("failed to connect to database: ", err)
	}
	defer pool.Close()

	s := pyhttp.NewServer(pool, cfg)
	log.Fatal(s.Router.Run(":" + cfg.Port))
}

func runMigrations(databaseURL string) {
	source, err := iofs.New(migrations.FS, ".")
	if err != nil {
		log.Fatal("failed to read migrations: ", err)
	}

	m, err := migrate.NewWithSourceInstance("iofs", source, databaseURL)
	if err != nil {
		log.Fatal("failed to create migrate instance: ", err)
	}

	if err := m.Up(); err != nil && err != migrate.ErrNoChange {
		log.Fatal("failed to run migrations: ", err)
	}
}
