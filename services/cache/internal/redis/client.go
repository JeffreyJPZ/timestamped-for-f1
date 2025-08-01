package redis

import (
	"context"
	"time"

	"github.com/redis/go-redis/v9"
)

type RedisClient struct {
	client *redis.Client
}

// NewClient initializes a new Redis client with the given URL and options.
func NewClient(url string) (*RedisClient, error) {
	opt, err := redis.ParseURL(url)
	if err != nil {
		return nil, err
	}

	r := redis.NewClient(opt)

	return &RedisClient{client: r}, nil
}

// Get gets a string value from Redis associated with the given key, returning nil if the key was not found,
// or an error if the value is not a string.
func (r *RedisClient) Get(ctx context.Context, key string) (any, error) {
	value, err := r.client.Get(ctx, key).Result()
	if err != nil {
		return nil, err
	}

	return value, nil
}

// Set assigns a value to the given key in Redis, returning nil if the key was successfully set,
// otherwise returning an error.
func (r *RedisClient) Set(ctx context.Context, key string, value any, expirationTime time.Duration) error {
	err := r.client.Set(ctx, key, value, expirationTime).Err()
	if err != nil {
		return err
	}

	return nil
}
