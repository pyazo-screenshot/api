package http

import (
	"context"
	"log/slog"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"

	"github.com/pyazo-screenshot/api/auth"
	"github.com/pyazo-screenshot/api/db"
)

const (
	userKey           = "user"
	sessionCookieName = "pyazo_token"
)

func (s *Server) userFromToken(ctx context.Context, token string) (*db.User, bool, error) {
	username, err := auth.ParseToken(token, s.config.JWTSecret)
	if err != nil {
		return nil, false, nil
	}

	user, err := db.GetUserByUsername(ctx, s.pool, username)
	if err != nil {
		return nil, false, err
	}
	if user == nil {
		return nil, false, nil
	}
	return user, true, nil
}

func (s *Server) AuthRequired() gin.HandlerFunc {
	return func(c *gin.Context) {
		header := c.GetHeader("Authorization")
		scheme, token, ok := strings.Cut(header, " ")
		if !ok || !strings.EqualFold(scheme, "Bearer") || token == "" {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"detail": "Invalid access token"})
			return
		}

		user, valid, err := s.userFromToken(c.Request.Context(), token)
		if err != nil {
			slog.Error("auth middleware: failed to get user", "error", err)
			c.AbortWithStatusJSON(http.StatusInternalServerError, gin.H{"detail": "Internal server error"})
			return
		}
		if !valid {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"detail": "Invalid access token"})
			return
		}

		c.Set(userKey, user)
		c.Next()
	}
}

func (s *Server) WebAuthRequired() gin.HandlerFunc {
	return func(c *gin.Context) {
		cookie, err := c.Request.Cookie(sessionCookieName)
		if err != nil || cookie.Value == "" {
			c.Redirect(http.StatusFound, "/login")
			c.Abort()
			return
		}

		user, valid, err := s.userFromToken(c.Request.Context(), cookie.Value)
		if err != nil {
			slog.Error("web auth middleware: failed to get user", "error", err)
			c.AbortWithStatus(http.StatusInternalServerError)
			return
		}
		if !valid {
			c.Redirect(http.StatusFound, "/login")
			c.Abort()
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
