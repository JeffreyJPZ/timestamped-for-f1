package grpc

import (
	"context"
	"fmt"
	"os"

	"github.com/JeffreyJPZ/timestamped-for-f1-cache-api/internal/redis"
	cache_api "github.com/JeffreyJPZ/timestamped-for-f1-cache-api/pkg/api"
	pb "github.com/JeffreyJPZ/timestamped-for-f1-cache-api/pkg/api/grpc/v1"
	cache "github.com/JeffreyJPZ/timestamped-for-f1-cache-api/pkg/cache"
)

// CacheService implements the gRPC cache service.
type CacheService struct {
	pb.UnimplementedCacheServer
	cache cache.Cache
}

// NewService initializes a gRPC service with a cache.
func NewService() (*CacheService, error) {
	// Initialize Redis service.
	config := &redis.Config{
		Host:     os.Getenv("TIMESTAMPED_FOR_F1_CACHE_HOST"),
		Port:     os.Getenv("TIMESTAMPED_FOR_F1_CACHE_PORT"),
		User:     os.Getenv("TIMESTAMPED_FOR_F1_CACHE_USERNAME"),
		Password: os.Getenv("TIMESTAMPED_FOR_F1_CACHE_PASSWORD"),
		DB:       os.Getenv("TIMESTAMPED_FOR_F1_CACHE_DB"),
	}
	cache, err := redis.NewClient(config.ConnectionURL())

	if err != nil {
		return nil, fmt.Errorf("failed to initialize cache service. Error: %v", err)
	}

	return &CacheService{
		cache: cache,
	}, nil
}

func (s *CacheService) Get(ctx context.Context, key *pb.CacheKey) (*pb.CacheResult, error) {
	result, err := s.cache.Get(ctx, key.GetKey())
	if err != nil {
		return &pb.CacheResult{
				Code:    cache_api.KEY_NOT_FOUND_ERROR.String(),
				Message: fmt.Errorf("key %s does not exist in cache", key.GetKey()).Error(),
			},
			fmt.Errorf("key %s does not exist in cache. Error: %v", key.GetKey(), err)
	}

	value, ok := result.(string)
	if !ok {
		return &pb.CacheResult{
				Code:    cache_api.VALUE_INVALID_FORMAT_ERROR.String(),
				Message: fmt.Errorf("failed to coerce value %v associated with key %s to string", result, key.GetKey()).Error(),
			},
			fmt.Errorf("failed to coerce value %v associated with key %s to string", result, key)
	}

	return &pb.CacheResult{
		Key:   key.GetKey(),
		Value: value,
	}, nil
}

func (s *CacheService) Set(ctx context.Context, item *pb.CacheItem) (*pb.CacheResult, error) {
	err := s.cache.Set(ctx, item.GetKey(), item.GetValue(), item.GetExpirationTime())
	if err != nil {
		return &pb.CacheResult{
				Code:    cache_api.CACHE_ERROR.String(),
				Message: fmt.Errorf("failed to set value %s for key %s", item.GetValue(), item.GetKey()).Error(),
			},
			fmt.Errorf("failed to set value %s for key %s. Error: %v", item.GetValue(), item.GetKey(), err)
	}

	return &pb.CacheResult{
		Key:   item.GetKey(),
		Value: item.GetValue(),
	}, nil
}
