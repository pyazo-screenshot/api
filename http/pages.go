package http

import (
	"log/slog"
	stdhttp "net/http"
	"strconv"

	"github.com/a-h/templ"
	"github.com/gin-gonic/gin"

	"github.com/pyazo-screenshot/api/db"
	"github.com/pyazo-screenshot/api/pages"
)

const webImageLimit = 30

func render(c *gin.Context, status int, component templ.Component) {
	c.Render(status, pages.TemplRenderer{
		Ctx:       c.Request.Context(),
		Component: component,
	})
}

func parsePositiveInt(value string, fallback int) int {
	n, err := strconv.Atoi(value)
	if err != nil || n < 0 {
		return fallback
	}
	return n
}

func (s *Server) webImagePage(c *gin.Context, user *db.User) ([]db.Image, int, int, bool, error) {
	page := parsePositiveInt(c.DefaultQuery("page", "0"), 0)
	limit := parsePositiveInt(c.DefaultQuery("limit", strconv.Itoa(webImageLimit)), webImageLimit)
	if limit == 0 || limit > 100 {
		limit = webImageLimit
	}

	images, err := db.GetImagesByOwnerID(c.Request.Context(), s.pool, user.ID, limit+1, page*limit)
	if err != nil {
		return nil, 0, 0, false, err
	}

	hasMore := len(images) > limit
	if hasMore {
		images = images[:limit]
	}
	return images, page + 1, limit, hasMore, nil
}

func (s *Server) ImagesPage(c *gin.Context) {
	user := CurrentUser(c)
	images, nextPage, limit, hasMore, err := s.webImagePage(c, user)
	if err != nil {
		slog.Error("web images: query failed", "error", err, "user_id", user.ID)
		c.Status(stdhttp.StatusInternalServerError)
		return
	}

	render(c, stdhttp.StatusOK, pages.ImagesPage(user.Username, images, nextPage, limit, hasMore))
}

func (s *Server) ImageCardsPage(c *gin.Context) {
	user := CurrentUser(c)
	images, nextPage, limit, hasMore, err := s.webImagePage(c, user)
	if err != nil {
		slog.Error("web images: query failed", "error", err, "user_id", user.ID)
		c.Status(stdhttp.StatusInternalServerError)
		return
	}

	render(c, stdhttp.StatusOK, pages.ImagesFragment(images, nextPage, limit, hasMore))
}

func (s *Server) DeleteImagePage(c *gin.Context) {
	status, detail := s.deleteImage(c.Request.Context(), CurrentUser(c), c.Param("id"))
	if status != stdhttp.StatusNoContent {
		c.String(status, detail)
		return
	}

	c.Status(stdhttp.StatusNoContent)
}
