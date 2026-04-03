package http

import (
	"crypto/rand"
	"fmt"
	"io"
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
		c.JSON(http.StatusBadRequest, gin.H{"detail": "Invalid file type"})
		return
	}
	ext := strings.ToLower(parts[len(parts)-1])
	if !allowedExtensions[ext] {
		c.JSON(http.StatusBadRequest, gin.H{"detail": "Invalid file type"})
		return
	}

	id := fmt.Sprintf("%s.%s", newUUID(), ext)
	path := filepath.Join(s.config.ImagesPath, id)

	dst, err := os.Create(path)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Failed to save image"})
		return
	}
	defer dst.Close()

	if _, err := io.Copy(dst, file); err != nil {
		os.Remove(path)
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Failed to save image"})
		return
	}
	dst.Close()

	if c.Query("clear_metadata") == "true" {
		exec.CommandContext(c.Request.Context(),
			"exiftool", "-overwrite_original_in_place", "-all=", path).Run()
	}

	if err := db.CreateImage(c.Request.Context(), s.pool, id, user.ID); err != nil {
		os.Remove(path)
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Failed to save image"})
		return
	}

	img, err := db.GetImageByID(c.Request.Context(), s.pool, id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Internal server error"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"id":         img.ID,
		"owner_id":   img.OwnerID,
		"created_at": img.CreatedAt,
	})
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
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Internal server error"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"results":   images,
		"count":     len(images),
		"next_page": page + 1,
	})
}

func (s *Server) DeleteImage(c *gin.Context) {
	user := CurrentUser(c)
	imageID := c.Param("id")

	img, err := db.GetImageByID(c.Request.Context(), s.pool, imageID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Internal server error"})
		return
	}
	if img == nil {
		c.JSON(http.StatusNotFound, gin.H{"detail": "Image not found"})
		return
	}
	if img.OwnerID != user.ID {
		c.JSON(http.StatusForbidden, gin.H{"detail": "Forbidden"})
		return
	}

	os.Remove(filepath.Join(s.config.ImagesPath, img.ID))

	if err := db.DeleteImageByID(c.Request.Context(), s.pool, imageID); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"detail": "Internal server error"})
		return
	}

	c.Status(http.StatusNoContent)
}
