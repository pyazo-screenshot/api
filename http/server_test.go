package http

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"mime/multipart"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/pyazo-screenshot/api/config"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

var testPool *pgxpool.Pool

func TestMain(m *testing.M) {
	gin.SetMode(gin.TestMode)

	ctx := context.Background()
	dsn := fmt.Sprintf("postgres://%s:%s@%s:5432/%s?sslmode=disable",
		envOr("POSTGRES_USER", "pyazo"),
		envOr("POSTGRES_PASSWORD", "pyazo"),
		envOr("POSTGRES_HOST", "localhost"),
		envOr("POSTGRES_DB", "pyazo"),
	)

	pool, err := pgxpool.New(ctx, dsn)
	if err != nil {
		fmt.Fprintf(os.Stderr, "db: %v\n", err)
		os.Exit(1)
	}
	testPool = pool

	// Clean leftover test data from previous runs
	cleanup(ctx, pool)
	code := m.Run()
	cleanup(ctx, pool)

	pool.Close()
	os.Exit(code)
}

func cleanup(ctx context.Context, pool *pgxpool.Pool) {
	pool.Exec(ctx, "DELETE FROM images WHERE owner_id IN (SELECT id FROM users WHERE username LIKE 'test_%')")
	pool.Exec(ctx, "DELETE FROM users WHERE username LIKE 'test_%'")
}

func envOr(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func newTestServer(t *testing.T) *Server {
	t.Helper()
	return NewServer(testPool, &config.Config{
		Env:           "testing",
		JWTSecret:     "test-jwt-secret",
		BlockRegister: false,
		ImagesPath:    t.TempDir(),
		CORSOrigin:    "*",
	})
}

func doJSON(router http.Handler, method, path string, body any, headers ...string) *httptest.ResponseRecorder {
	var buf bytes.Buffer
	if body != nil {
		json.NewEncoder(&buf).Encode(body)
	}
	req := httptest.NewRequest(method, path, &buf)
	if body != nil {
		req.Header.Set("Content-Type", "application/json")
	}
	for i := 0; i+1 < len(headers); i += 2 {
		req.Header.Set(headers[i], headers[i+1])
	}
	w := httptest.NewRecorder()
	router.ServeHTTP(w, req)
	return w
}

func parseBody(t *testing.T, w *httptest.ResponseRecorder) map[string]any {
	t.Helper()
	var m map[string]any
	require.NoError(t, json.NewDecoder(w.Body).Decode(&m))
	return m
}

func registerUser(t *testing.T, router http.Handler, username, password string) string {
	t.Helper()
	w := doJSON(router, "POST", "/auth/register", map[string]string{
		"username": username, "password": password,
	})
	require.Equal(t, http.StatusOK, w.Code, "register %s: %s", username, w.Body.String())
	token, ok := parseBody(t, w)["access_token"].(string)
	require.True(t, ok, "no access_token in register response")
	return token
}

func uploadImage(t *testing.T, srv *Server, token, filename string) map[string]any {
	t.Helper()
	var buf bytes.Buffer
	mw := multipart.NewWriter(&buf)
	fw, _ := mw.CreateFormFile("upload_file", filename)
	fw.Write([]byte("fake image data"))
	mw.Close()

	req := httptest.NewRequest("POST", "/images", &buf)
	req.Header.Set("Content-Type", mw.FormDataContentType())
	req.Header.Set("Authorization", "Bearer "+token)
	w := httptest.NewRecorder()
	srv.Router.ServeHTTP(w, req)
	require.Equal(t, http.StatusOK, w.Code, "upload: %s", w.Body.String())
	return parseBody(t, w)
}

func doMultipart(srv *Server, filename, token string) *httptest.ResponseRecorder {
	var buf bytes.Buffer
	mw := multipart.NewWriter(&buf)
	fw, _ := mw.CreateFormFile("upload_file", filename)
	fw.Write([]byte("data"))
	mw.Close()

	req := httptest.NewRequest("POST", "/images", &buf)
	req.Header.Set("Content-Type", mw.FormDataContentType())
	if token != "" {
		req.Header.Set("Authorization", "Bearer "+token)
	}
	w := httptest.NewRecorder()
	srv.Router.ServeHTTP(w, req)
	return w
}

// --- Auth ---

func TestRegister(t *testing.T) {
	srv := newTestServer(t)
	w := doJSON(srv.Router, "POST", "/auth/register",
		map[string]string{"username": "test_register", "password": "pass123"})
	require.Equal(t, http.StatusOK, w.Code)
	m := parseBody(t, w)
	assert.Equal(t, "bearer", m["token_type"])
	assert.NotNil(t, m["access_token"])
}

func TestRegisterDuplicate(t *testing.T) {
	srv := newTestServer(t)
	registerUser(t, srv.Router, "test_regdup", "pass123")

	w := doJSON(srv.Router, "POST", "/auth/register",
		map[string]string{"username": "test_regdup", "password": "pass123"})
	assert.Equal(t, http.StatusConflict, w.Code)
}

func TestRegisterBlocked(t *testing.T) {
	srv := NewServer(testPool, &config.Config{
		Env:           "testing",
		JWTSecret:     "test-jwt-secret",
		BlockRegister: true,
		ImagesPath:    t.TempDir(),
		CORSOrigin:    "*",
	})
	w := doJSON(srv.Router, "POST", "/auth/register",
		map[string]string{"username": "test_blocked", "password": "pass123"})
	assert.Equal(t, http.StatusForbidden, w.Code)
}

func TestLogin(t *testing.T) {
	srv := newTestServer(t)
	registerUser(t, srv.Router, "test_login", "pass123")

	w := doJSON(srv.Router, "POST", "/auth/login",
		map[string]string{"username": "test_login", "password": "pass123"})
	require.Equal(t, http.StatusOK, w.Code)
	assert.NotNil(t, parseBody(t, w)["access_token"])
}

func TestLoginWrongPassword(t *testing.T) {
	srv := newTestServer(t)
	registerUser(t, srv.Router, "test_loginbad", "pass123")

	w := doJSON(srv.Router, "POST", "/auth/login",
		map[string]string{"username": "test_loginbad", "password": "wrong"})
	assert.Equal(t, http.StatusUnauthorized, w.Code)
}

func TestLoginNonexistent(t *testing.T) {
	srv := newTestServer(t)
	w := doJSON(srv.Router, "POST", "/auth/login",
		map[string]string{"username": "test_nosuchuser", "password": "pass123"})
	assert.Equal(t, http.StatusUnauthorized, w.Code)
}

func TestMe(t *testing.T) {
	srv := newTestServer(t)
	token := registerUser(t, srv.Router, "test_me", "pass123")

	w := doJSON(srv.Router, "GET", "/auth/me", nil, "Authorization", "Bearer "+token)
	require.Equal(t, http.StatusOK, w.Code)
	assert.Equal(t, "test_me", parseBody(t, w)["username"])
}

func TestMeUnauthorized(t *testing.T) {
	srv := newTestServer(t)
	w := doJSON(srv.Router, "GET", "/auth/me", nil)
	assert.Equal(t, http.StatusUnauthorized, w.Code)
}

// --- Images ---

func TestUploadImage(t *testing.T) {
	srv := newTestServer(t)
	token := registerUser(t, srv.Router, "test_upload", "pass123")
	img := uploadImage(t, srv, token, "photo.png")

	assert.NotNil(t, img["id"])
	assert.NotNil(t, img["owner_id"])

	path := filepath.Join(srv.config.ImagesPath, img["id"].(string))
	assert.FileExists(t, path)
}

func TestUploadImageUnauthorized(t *testing.T) {
	srv := newTestServer(t)
	w := doMultipart(srv, "photo.png", "")
	assert.Equal(t, http.StatusUnauthorized, w.Code)
}

func TestUploadInvalidFileType(t *testing.T) {
	srv := newTestServer(t)
	token := registerUser(t, srv.Router, "test_upload_bad", "pass123")
	w := doMultipart(srv, "malware.exe", token)
	assert.Equal(t, http.StatusBadRequest, w.Code)
}

func TestListImages(t *testing.T) {
	srv := newTestServer(t)
	token := registerUser(t, srv.Router, "test_list", "pass123")
	uploadImage(t, srv, token, "a.png")
	uploadImage(t, srv, token, "b.jpg")

	w := doJSON(srv.Router, "GET", "/images", nil, "Authorization", "Bearer "+token)
	require.Equal(t, http.StatusOK, w.Code)
	m := parseBody(t, w)
	results, ok := m["results"].([]any)
	require.True(t, ok)
	assert.Len(t, results, 2)
	assert.Equal(t, float64(1), m["next_page"])
}

func TestDeleteImage(t *testing.T) {
	srv := newTestServer(t)
	token := registerUser(t, srv.Router, "test_delete", "pass123")
	img := uploadImage(t, srv, token, "todelete.png")
	id := img["id"].(string)

	w := doJSON(srv.Router, "DELETE", "/images/"+id, nil, "Authorization", "Bearer "+token)
	assert.Equal(t, http.StatusNoContent, w.Code)

	// File removed from disk
	assert.NoFileExists(t, filepath.Join(srv.config.ImagesPath, id))

	// Image removed from list
	w = doJSON(srv.Router, "GET", "/images", nil, "Authorization", "Bearer "+token)
	results := parseBody(t, w)["results"].([]any)
	assert.Empty(t, results)
}

func TestDeleteImageNotOwner(t *testing.T) {
	srv := newTestServer(t)
	tokenA := registerUser(t, srv.Router, "test_del_owner", "pass123")
	tokenB := registerUser(t, srv.Router, "test_del_other", "pass123")
	img := uploadImage(t, srv, tokenA, "owned.png")

	w := doJSON(srv.Router, "DELETE", "/images/"+img["id"].(string), nil,
		"Authorization", "Bearer "+tokenB)
	assert.Equal(t, http.StatusForbidden, w.Code)
}

func TestDeleteImageUnauthorized(t *testing.T) {
	srv := newTestServer(t)
	w := doJSON(srv.Router, "DELETE", "/images/someid", nil)
	assert.Equal(t, http.StatusUnauthorized, w.Code)
}

func TestDeleteImageNotFound(t *testing.T) {
	srv := newTestServer(t)
	token := registerUser(t, srv.Router, "test_del_nf", "pass123")

	w := doJSON(srv.Router, "DELETE", "/images/nonexistent.png", nil,
		"Authorization", "Bearer "+token)
	assert.Equal(t, http.StatusNotFound, w.Code)
}
