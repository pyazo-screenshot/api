package http

import (
	"log/slog"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"

	"github.com/pyazo-screenshot/api/auth"
	"github.com/pyazo-screenshot/api/db"
)

const userKey = "user"

func (s *Server) AuthRequired() gin.HandlerFunc {
	return func(c *gin.Context) {
		header := c.GetHeader("Authorization")
		scheme, token, ok := strings.Cut(header, " ")
		if !ok || !strings.EqualFold(scheme, "Bearer") || token == "" {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"detail": "Invalid access token"})
			return
		}

		username, err := auth.ParseToken(token, s.config.JWTSecret)
		if err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"detail": "Invalid access token"})
			return
		}

		user, err := db.GetUserByUsername(c.Request.Context(), s.pool, username)
		if err != nil {
			slog.Error("auth middleware: failed to get user", "error", err)
			c.AbortWithStatusJSON(http.StatusInternalServerError, gin.H{"detail": "Internal server error"})
			return
		}
		if user == nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"detail": "Invalid access token"})
			return
		}

		c.Set(userKey, user)
		c.Next()
	}
}

func CurrentUser(c *gin.Context) *db.User {
	u, _ := c.Get(userKey)
	return u.(*db.User)
}
