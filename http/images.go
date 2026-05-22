package http

import (
	"context"
	"crypto/rand"
	"fmt"
	"io"
	"log/slog"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"

	"github.com/pyazo-screenshot/api/db"
)

func newUUID() string {
	b := make([]byte, 16)
	rand.Read(b)
	b[6] = (b[6] & 0x0f) | 0x40
	b[8] = (b[8] & 0x3f) | 0x80
	return fmt.Sprintf("%x-%x-%x-%x-%x", b[0:4], b[4:6], b[6:8], b[8:10], b[10:])
}

var allowedExtensions = map[string]bool{
	"jpg": true, "jpeg": true, "tiff": true, "gif": true,
	"bmp": true, "png": true, "webp": true,
}

func imageJSON(img db.Image) gin.H {
	return gin.H{
		"id":         img.ID,
		"owner_id":   img.OwnerID,
		"created_at": img.CreatedAt,
	}
}

func (s *Server) UploadImage(c *gin.Context) {
	user := CurrentUser(c)

	file, header, err := c.Request.FormFile("upload_file")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"detail": "No file provided"})
		return
	}
	defer file.Close()

	parts := strings.Split(header.Filename, ".")
	if len(parts) < 2 {
		c.JSON(http.StatusUnsupportedMediaType, gin.H{"detail": "File type not supported"})
		return
	}
	ext := strings.ToLower(parts[len(parts)-1])
	if !allowedExtensions[ext] {
		c.JSON(http.StatusUnsupportedMediaType, gin.H{"detail": "File type not supported"})
		return
	}

	id := fmt.Sprintf("%s.%s", newUUID(), ext)
	path := filepath.Join(s.config.ImagesPath, id)

	dst, err := os.Create(path)
	if err != nil {
		slog.Error("upload: failed to create file", "error", err, "path", path)
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Failed to save image"})
		return
	}
	defer dst.Close()

	if _, err := io.Copy(dst, file); err != nil {
		os.Remove(path)
		slog.Error("upload: failed to write file", "error", err, "path", path)
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Failed to save image"})
		return
	}
	dst.Close()

	if c.Query("clear_metadata") == "true" {
		if err := exec.CommandContext(c.Request.Context(),
			"exiftool", "-overwrite_original_in_place", "-all=", path).Run(); err != nil {
			slog.Warn("upload: exiftool failed", "error", err, "path", path)
		}
	}

	if err := db.CreateImage(c.Request.Context(), s.pool, id, user.ID); err != nil {
		os.Remove(path)
		slog.Error("upload: failed to create image record", "error", err, "image_id", id)
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Failed to save image"})
		return
	}

	img, err := db.GetImageByID(c.Request.Context(), s.pool, id)
	if err != nil {
		slog.Error("upload: failed to get image", "error", err, "image_id", id)
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Internal server error"})
		return
	}

	c.JSON(http.StatusOK, imageJSON(*img))
}

func (s *Server) ListImages(c *gin.Context) {
	user := CurrentUser(c)

	page, _ := strconv.Atoi(c.DefaultQuery("page", "0"))
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "50"))
	if limit > 1000 {
		limit = 1000
	}
	offset := page * limit

	images, err := db.GetImagesByOwnerID(c.Request.Context(), s.pool, user.ID, limit, offset)
	if err != nil {
		slog.Error("list images: query failed", "error", err, "user_id", user.ID)
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Internal server error"})
		return
	}

	results := make([]gin.H, 0, len(images))
	for _, img := range images {
		results = append(results, imageJSON(img))
	}

	c.JSON(http.StatusOK, gin.H{
		"results":   results,
		"count":     len(images),
		"next_page": page + 1,
	})
}

func (s *Server) DeleteImage(c *gin.Context) {
	status, detail := s.deleteImage(c.Request.Context(), CurrentUser(c), c.Param("id"))
	if status == http.StatusNoContent {
		c.Status(http.StatusNoContent)
		return
	}
	c.JSON(status, gin.H{"detail": detail})
}

func (s *Server) ServeImageFile(c *gin.Context) {
	if c.Request.Method != http.MethodGet && c.Request.Method != http.MethodHead {
		c.Status(http.StatusNotFound)
		return
	}

	id := strings.TrimPrefix(c.Request.URL.Path, "/")
	ext := strings.TrimPrefix(strings.ToLower(filepath.Ext(id)), ".")
	if id == "" || strings.Contains(id, "/") || strings.Contains(id, "\\") ||
		strings.Contains(id, "..") || !allowedExtensions[ext] {
		c.Status(http.StatusNotFound)
		return
	}

	path := filepath.Join(s.config.ImagesPath, id)
	info, err := os.Stat(path)
	if err != nil || info.IsDir() {
		c.Status(http.StatusNotFound)
		return
	}

	c.File(path)
}

func (s *Server) deleteImage(ctx context.Context, user *db.User, imageID string) (int, string) {
	img, err := db.GetImageByID(ctx, s.pool, imageID)
	if err != nil {
		slog.Error("delete image: query failed", "error", err, "image_id", imageID)
		return http.StatusInternalServerError, "Internal server error"
	}
	if img == nil {
		return http.StatusNotFound, "Image not found"
	}
	if img.OwnerID != user.ID {
		return http.StatusForbidden, "Forbidden"
	}

	if err := os.Remove(filepath.Join(s.config.ImagesPath, img.ID)); err != nil {
		slog.Warn("delete image: failed to remove file", "error", err, "image_id", img.ID)
	}

	if err := db.DeleteImageByID(ctx, s.pool, imageID); err != nil {
		slog.Error("delete image: db delete failed", "error", err, "image_id", imageID)
		return http.StatusInternalServerError, "Internal server error"
	}

	return http.StatusNoContent, ""
}
