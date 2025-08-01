package routes

import (
	"net/http"
	"os"

	"github.com/JeffreyJPZ/timestamped-for-f1-cache/internal/redis"
	"github.com/JeffreyJPZ/timestamped-for-f1-cache/pkg/cache"
)

type Router struct{}

// Routes registers the HTTP handlers for the cache API.
func (r *Router) Routes() *http.ServeMux {
	router := &http.ServeMux{}

	// Initialize Redis service.
	config := &redis.Config{
		Host:     os.Getenv("TIMESTAMPED_FOR_F1_CACHE_HOST"),
		Port:     os.Getenv("TIMESTAMPED_FOR_F1_CACHE_PORT"),
		User:     os.Getenv("TIMESTAMPED_FOR_F1_CACHE_USER"),
		Password: os.Getenv("TIMESTAMPED_FOR_F1_CACHE_PAsSWORD"),
		DB:       os.Getenv("TIMESTAMPED_FOR_F1_CACHE_DB"),
	}
	cache, err := redis.NewClient(config.ConnectionURL())

	if err != nil {
		panic(err)
	}

	router.HandleFunc("GET /v1/cache/get", r.handleCacheGet(cache))
	router.HandleFunc("PUT /v1/cache/set", r.handleCacheSet(cache))

	return router
}

// TODO: implement
func (r *Router) handleCacheGet(c cache.Cache) http.HandlerFunc {
	return nil
}

// TODO: implement
func (r *Router) handleCacheSet(c cache.Cache) http.HandlerFunc {
	return nil
}
