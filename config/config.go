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

func Load() *Config {
	return &Config{
		Env:              getenv("ENV", "production"),
		PostgresUser:     getenv("POSTGRES_USER", "pyazo"),
		PostgresPassword: getenv("POSTGRES_PASSWORD", ""),
		PostgresDB:       getenv("POSTGRES_DB", "pyazo"),
		PostgresHost:     getenv("POSTGRES_HOST", "localhost"),
		JWTSecret:        getenv("JWT_SECRET", ""),
		BlockRegister:    strings.ToLower(getenv("BLOCK_REGISTER", "true")) != "false",
		ImagesPath:       getenv("IMAGES_PATH", "/images"),
		CORSOrigin:       getenv("CORS_ORIGIN", "https://app.pyazo.com"),
		Port:             getenv("PORT", "8000"),
	}
}

func (c *Config) DatabaseURL() string {
	return fmt.Sprintf("postgres://%s:%s@%s:5432/%s?sslmode=disable",
		c.PostgresUser, c.PostgresPassword, c.PostgresHost, c.PostgresDB)
}

func getenv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
