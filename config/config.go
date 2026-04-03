package config

import (
	"fmt"
	"os"
	"strings"
)

type Config struct {
	Env              string
	PostgresUser     string
	PostgresPassword string
	PostgresDB       string
	PostgresHost     string
	JWTSecret        string
	BlockRegister    bool
	ImagesPath       string
	CORSOrigin       string
	Port             string
}

func Load() (*Config, error) {
	var missing []string
	cfg := &Config{
		Env:              optional("ENV", "production"),
		PostgresUser:     optional("POSTGRES_USER", "pyazo"),
		PostgresPassword: required("POSTGRES_PASSWORD", &missing),
		PostgresDB:       optional("POSTGRES_DB", "pyazo"),
		PostgresHost:     optional("POSTGRES_HOST", "localhost"),
		JWTSecret:        required("JWT_SECRET", &missing),
		BlockRegister:    strings.ToLower(optional("BLOCK_REGISTER", "true")) != "false",
		ImagesPath:       optional("IMAGES_PATH", "/images"),
		CORSOrigin:       optional("CORS_ORIGIN", "https://app.pyazo.com"),
		Port:             optional("PORT", "8000"),
	}
	if len(missing) > 0 {
		return nil, fmt.Errorf("missing required env vars: %s", strings.Join(missing, ", "))
	}
	return cfg, nil
}

func required(key string, missing *[]string) string {
	v := os.Getenv(key)
	if v == "" {
		*missing = append(*missing, key)
	}
	return v
}

func optional(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func (c *Config) DatabaseURL() string {
	return fmt.Sprintf("postgres://%s:%s@%s:5432/%s?sslmode=disable",
		c.PostgresUser, c.PostgresPassword, c.PostgresHost, c.PostgresDB)
}
