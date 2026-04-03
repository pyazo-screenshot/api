package http

import (
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
		if !strings.HasPrefix(header, "Bearer ") {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"detail": "Invalid access token"})
			return
		}

		username, err := auth.ParseToken(strings.TrimPrefix(header, "Bearer "), s.config.JWTSecret)
		if err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"detail": "Invalid access token"})
			return
		}

		user, err := db.GetUserByUsername(c.Request.Context(), s.pool, username)
		if err != nil || user == nil {
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
