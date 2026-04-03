package auth

import (
	"crypto/rand"
	"crypto/subtle"
	"encoding/base64"
	"fmt"
	"strings"

	"golang.org/x/crypto/argon2"
)

// Passlib-compatible argon2id defaults
const (
	defaultMemory      = 65536
	defaultIterations  = 3
	defaultParallelism = 4
	defaultSaltLen     = 16
	defaultKeyLen      = 32
)

func HashPassword(password string) (string, error) {
	salt := make([]byte, defaultSaltLen)
	if _, err := rand.Read(salt); err != nil {
		return "", err
	}

	hash := argon2.IDKey([]byte(password), salt, defaultIterations, defaultMemory, defaultParallelism, defaultKeyLen)

	return fmt.Sprintf("$argon2id$v=%d$m=%d,t=%d,p=%d$%s$%s",
		argon2.Version,
		defaultMemory, defaultIterations, defaultParallelism,
		base64Encode(salt), base64Encode(hash),
	), nil
}

func VerifyPassword(encoded, password string) (bool, error) {
	parts := strings.Split(encoded, "$")
	if len(parts) != 6 || parts[1] != "argon2id" {
		return false, fmt.Errorf("invalid argon2id hash format")
	}

	var memory uint32
	var iterations uint32
	var parallelism uint8
	if _, err := fmt.Sscanf(parts[3], "m=%d,t=%d,p=%d", &memory, &iterations, &parallelism); err != nil {
		return false, err
	}

	salt, err := base64Decode(parts[4])
	if err != nil {
		return false, err
	}

	expectedHash, err := base64Decode(parts[5])
	if err != nil {
		return false, err
	}

	hash := argon2.IDKey([]byte(password), salt, iterations, memory, parallelism, uint32(len(expectedHash)))
	return subtle.ConstantTimeCompare(hash, expectedHash) == 1, nil
}

func base64Encode(data []byte) string {
	return base64.RawStdEncoding.EncodeToString(data)
}

func base64Decode(s string) ([]byte, error) {
	// Passlib uses standard base64 without padding
	return base64.RawStdEncoding.DecodeString(s)
}
