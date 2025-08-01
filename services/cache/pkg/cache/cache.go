package cache

import (
	"context"
	"time"
)

type Cache interface {
	// Get returns a pair of values where the first value is the value associated with the key if there was a cache hit,
	// or nil if the key was not found. The second value indicates whether there was an error.
	Get(ctx context.Context, key string) (any, error)

	// Set returns a value with a key and a TTL provided by the given expiration time.
	// Returns nil if the key was successfully set, otherwise returns an error.
	Set(ctx context.Context, key string, value any, expirationTime time.Duration) error
}
