package db

import (
	"context"
	"errors"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgconn"
	"github.com/jackc/pgx/v5/pgxpool"
)

var ErrUsernameTaken = errors.New("username already registered")

type User struct {
	ID             int    `db:"id"`
	Username       string `db:"username"`
	HashedPassword string `db:"hashed_password"`
}

type Image struct {
	ID        string    `db:"id"`
	OwnerID   int       `db:"owner_id"`
	CreatedAt time.Time `db:"created_at"`
}

func NewPool(ctx context.Context, databaseURL string) (*pgxpool.Pool, error) {
	pool, err := pgxpool.New(ctx, databaseURL)
	if err != nil {
		return nil, err
	}
	if err := pool.Ping(ctx); err != nil {
		pool.Close()
		return nil, err
	}
	return pool, nil
}

func GetUserByUsername(ctx context.Context, pool *pgxpool.Pool, username string) (*User, error) {
	rows, err := pool.Query(ctx,
		"SELECT id, username, hashed_password FROM users WHERE username = $1", username)
	if err != nil {
		return nil, err
	}
	user, err := pgx.CollectExactlyOneRow(rows, pgx.RowToStructByName[User])
	if errors.Is(err, pgx.ErrNoRows) {
		return nil, nil
	}
	return &user, err
}

func CreateUser(ctx context.Context, pool *pgxpool.Pool, username, hashedPassword string) error {
	_, err := pool.Exec(ctx,
		"INSERT INTO users (username, hashed_password) VALUES ($1, $2)", username, hashedPassword)
	if err != nil {
		var pgErr *pgconn.PgError
		if errors.As(err, &pgErr) && pgErr.Code == "23505" {
			return ErrUsernameTaken
		}
	}
	return err
}

func GetImageByID(ctx context.Context, pool *pgxpool.Pool, id string) (*Image, error) {
	rows, err := pool.Query(ctx,
		"SELECT id, owner_id, created_at FROM images WHERE id = $1", id)
	if err != nil {
		return nil, err
	}
	img, err := pgx.CollectExactlyOneRow(rows, pgx.RowToStructByName[Image])
	if errors.Is(err, pgx.ErrNoRows) {
		return nil, nil
	}
	return &img, err
}

func GetImagesByOwnerID(ctx context.Context, pool *pgxpool.Pool, ownerID, limit, offset int) ([]Image, error) {
	rows, err := pool.Query(ctx,
		"SELECT id, owner_id, created_at FROM images WHERE owner_id = $1 ORDER BY created_at DESC LIMIT $2 OFFSET $3",
		ownerID, limit, offset)
	if err != nil {
		return nil, err
	}
	return pgx.CollectRows(rows, pgx.RowToStructByName[Image])
}

func CreateImage(ctx context.Context, pool *pgxpool.Pool, id string, ownerID int) error {
	_, err := pool.Exec(ctx,
		"INSERT INTO images (id, owner_id) VALUES ($1, $2)", id, ownerID)
	return err
}

func DeleteImageByID(ctx context.Context, pool *pgxpool.Pool, id string) error {
	_, err := pool.Exec(ctx, "DELETE FROM images WHERE id = $1", id)
	return err
}
