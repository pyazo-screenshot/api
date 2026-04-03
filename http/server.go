package http

import (
	"log/slog"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/pyazo-screenshot/api/config"
)

type Server struct {
	pool   *pgxpool.Pool
	config *config.Config
	Router *gin.Engine
}

func NewServer(pool *pgxpool.Pool, cfg *config.Config) *Server {
	if cfg.Env == "production" {
		gin.SetMode(gin.ReleaseMode)
	}

	s := &Server{pool: pool, config: cfg}

	r := gin.New()
	r.Use(requestLogger(), gin.Recovery())
	r.Use(s.cors())
	s.registerRoutes(r)
	s.Router = r
	return s
}

func requestLogger() gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()
		c.Next()
		status := c.Writer.Status()
		attrs := []any{
			"method", c.Request.Method,
			"path", c.Request.URL.Path,
			"status", status,
			"duration", time.Since(start),
			"ip", c.ClientIP(),
		}
		if status >= 500 {
			slog.Error("request", attrs...)
		} else {
			slog.Info("request", attrs...)
		}
	}
}

func (s *Server) registerRoutes(r *gin.Engine) {
	a := r.Group("/auth")
	{
		a.POST("/login", s.Login)
		a.POST("/register", s.Register)
		a.GET("/me", s.AuthRequired(), s.Me)
	}

	img := r.Group("/images", s.AuthRequired())
	{
		img.POST("", s.UploadImage)
		img.GET("", s.ListImages)
		img.DELETE("/:id", s.DeleteImage)
	}
}

func (s *Server) cors() gin.HandlerFunc {
	return func(c *gin.Context) {
		origin := s.config.CORSOrigin
		c.Header("Access-Control-Allow-Origin", origin)
		c.Header("Access-Control-Allow-Credentials", "true")
		c.Header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS, PATCH")
		c.Header("Access-Control-Allow-Headers", "Authorization, Content-Type")

		if c.Request.Method == http.MethodOptions {
			c.AbortWithStatus(http.StatusNoContent)
			return
		}
		c.Next()
	}
}
