package http

import (
	"context"
	"errors"
	"log/slog"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"

	"github.com/pyazo-screenshot/api/auth"
	"github.com/pyazo-screenshot/api/db"
	"github.com/pyazo-screenshot/api/pages"
)

type credentials struct {
	Username string `json:"username" binding:"required"`
	Password string `json:"password" binding:"required"`
}

func (s *Server) loginToken(ctx context.Context, username, password string) (string, bool, error) {
	user, err := db.GetUserByUsername(ctx, s.pool, username)
	if err != nil {
		return "", false, err
	}
	if user == nil {
		return "", false, nil
	}

	ok, err := auth.VerifyPassword(user.HashedPassword, password)
	if err != nil || !ok {
		return "", false, nil
	}

	token, err := auth.CreateToken(user.Username, s.config.JWTSecret)
	if err != nil {
		return "", false, err
	}
	return token, true, nil
}

func (s *Server) registerToken(ctx context.Context, username, password string) (string, error) {
	hashed, err := auth.HashPassword(password)
	if err != nil {
		return "", err
	}

	if err := db.CreateUser(ctx, s.pool, username, hashed); err != nil {
		return "", err
	}

	return auth.CreateToken(username, s.config.JWTSecret)
}

func (s *Server) setSessionCookie(c *gin.Context, token string) {
	c.SetSameSite(http.SameSiteLaxMode)
	c.SetCookie(sessionCookieName, token, 60*60*24*365, "/", "", s.config.Env == "production", true)
}

func (s *Server) clearSessionCookie(c *gin.Context) {
	c.SetSameSite(http.SameSiteLaxMode)
	c.SetCookie(sessionCookieName, "", -1, "/", "", s.config.Env == "production", true)
}

func (s *Server) Login(c *gin.Context) {
	var creds credentials
	if err := c.ShouldBindJSON(&creds); err != nil {
		c.JSON(http.StatusUnprocessableEntity, gin.H{"detail": "Invalid request body"})
		return
	}

	token, ok, err := s.loginToken(c.Request.Context(), creds.Username, creds.Password)
	if err != nil {
		slog.Error("login: failed", "error", err)
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Internal server error"})
		return
	}
	if !ok {
		c.JSON(http.StatusUnauthorized, gin.H{"detail": "Invalid credentials"})
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

	token, err := s.registerToken(c.Request.Context(), creds.Username, creds.Password)
	if err != nil {
		if errors.Is(err, db.ErrUsernameTaken) {
			c.JSON(http.StatusConflict, gin.H{"detail": "Username already registered"})
			return
		}
		slog.Error("register: failed", "error", err)
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

func (s *Server) LoginPage(c *gin.Context) {
	render(c, http.StatusOK, pages.LoginPage(""))
}

func (s *Server) HandleLoginPage(c *gin.Context) {
	username := strings.TrimSpace(c.PostForm("username"))
	password := c.PostForm("password")
	if username == "" || password == "" {
		render(c, http.StatusUnprocessableEntity, pages.LoginPage("Please enter your username and password."))
		return
	}

	token, ok, err := s.loginToken(c.Request.Context(), username, password)
	if err != nil {
		slog.Error("web login: failed", "error", err)
		c.Status(http.StatusInternalServerError)
		return
	}
	if !ok {
		render(c, http.StatusUnauthorized, pages.LoginPage("The username and password combination is incorrect."))
		return
	}

	s.setSessionCookie(c, token)
	c.Redirect(http.StatusSeeOther, "/")
}

func (s *Server) RegisterPage(c *gin.Context) {
	render(c, http.StatusOK, pages.RegisterPage("", s.config.BlockRegister))
}

func (s *Server) HandleRegisterPage(c *gin.Context) {
	if s.config.BlockRegister {
		render(c, http.StatusForbidden, pages.RegisterPage("Registration is disabled.", true))
		return
	}

	username := strings.TrimSpace(c.PostForm("username"))
	password := c.PostForm("password")
	confirmPassword := c.PostForm("confirm_password")
	if username == "" || password == "" {
		render(c, http.StatusUnprocessableEntity, pages.RegisterPage("Please enter your username and password.", false))
		return
	}
	if password != confirmPassword {
		render(c, http.StatusUnprocessableEntity, pages.RegisterPage("The two passwords do not match.", false))
		return
	}

	token, err := s.registerToken(c.Request.Context(), username, password)
	if err != nil {
		if errors.Is(err, db.ErrUsernameTaken) {
			render(c, http.StatusConflict, pages.RegisterPage("Username already registered.", false))
			return
		}
		slog.Error("web register: failed", "error", err)
		c.Status(http.StatusInternalServerError)
		return
	}

	s.setSessionCookie(c, token)
	c.Redirect(http.StatusSeeOther, "/")
}

func (s *Server) LogoutPage(c *gin.Context) {
	s.clearSessionCookie(c)
	c.Redirect(http.StatusSeeOther, "/login")
}
