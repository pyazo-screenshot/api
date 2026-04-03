package http

import (
	"log/slog"
	"net/http"

	"github.com/gin-gonic/gin"

	"github.com/pyazo-screenshot/api/auth"
	"github.com/pyazo-screenshot/api/db"
)

type credentials struct {
	Username string `json:"username" binding:"required"`
	Password string `json:"password" binding:"required"`
}

func (s *Server) Login(c *gin.Context) {
	var creds credentials
	if err := c.ShouldBindJSON(&creds); err != nil {
		c.JSON(http.StatusUnprocessableEntity, gin.H{"detail": "Invalid request body"})
		return
	}

	user, err := db.GetUserByUsername(c.Request.Context(), s.pool, creds.Username)
	if err != nil {
		slog.Error("login: failed to get user", "error", err)
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Internal server error"})
		return
	}
	if user == nil {
		c.JSON(http.StatusUnauthorized, gin.H{"detail": "Invalid credentials"})
		return
	}

	ok, err := auth.VerifyPassword(user.HashedPassword, creds.Password)
	if err != nil || !ok {
		c.JSON(http.StatusUnauthorized, gin.H{"detail": "Invalid credentials"})
		return
	}

	token, err := auth.CreateToken(user.Username, s.config.JWTSecret)
	if err != nil {
		slog.Error("login: failed to create token", "error", err)
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Internal server error"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"access_token": token,
		"token_type":   "bearer",
	})
}

func (s *Server) Register(c *gin.Context) {
	if s.config.BlockRegister {
		c.JSON(http.StatusForbidden, gin.H{"detail": "Registration disabled"})
		return
	}

	var creds credentials
	if err := c.ShouldBindJSON(&creds); err != nil {
		c.JSON(http.StatusUnprocessableEntity, gin.H{"detail": "Invalid request body"})
		return
	}

	hashed, err := auth.HashPassword(creds.Password)
	if err != nil {
		slog.Error("register: failed to hash password", "error", err)
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Internal server error"})
		return
	}

	if err := db.CreateUser(c.Request.Context(), s.pool, creds.Username, hashed); err != nil {
		if err == db.ErrUsernameTaken {
			c.JSON(http.StatusConflict, gin.H{"detail": "Username already registered"})
			return
		}
		slog.Error("register: failed to create user", "error", err)
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Internal server error"})
		return
	}

	// Auto-login after registration
	token, err := auth.CreateToken(creds.Username, s.config.JWTSecret)
	if err != nil {
		slog.Error("register: failed to create token", "error", err)
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Internal server error"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"access_token": token,
		"token_type":   "bearer",
	})
}

func (s *Server) Me(c *gin.Context) {
	user := CurrentUser(c)
	c.JSON(http.StatusOK, gin.H{
		"id":       user.ID,
		"username": user.Username,
	})
}
