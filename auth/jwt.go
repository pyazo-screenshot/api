package auth

import (
	"time"

	"github.com/golang-jwt/jwt/v5"
)

func CreateToken(username, secret string) (string, error) {
	claims := jwt.MapClaims{
		"sub": username,
		"exp": jwt.NewNumericDate(time.Now().Add(7300 * 24 * time.Hour)),
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(secret))
}

func ParseToken(tokenStr, secret string) (string, error) {
	token, err := jwt.Parse(tokenStr, func(t *jwt.Token) (any, error) {
		return []byte(secret), nil
	}, jwt.WithValidMethods([]string{"HS256"}))
	if err != nil {
		return "", err
	}

	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok {
		return "", jwt.ErrTokenInvalidClaims
	}

	sub, err := claims.GetSubject()
	if err != nil {
		return "", err
	}
	return sub, nil
}
