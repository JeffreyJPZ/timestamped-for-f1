package routes

import (
	"fmt"
	"net/http"
	"os"

	"github.com/JeffreyJPZ/timestamped-for-f1-cache-api/internal/jsonutils"
	"github.com/JeffreyJPZ/timestamped-for-f1-cache-api/internal/redis"
	cache_api "github.com/JeffreyJPZ/timestamped-for-f1-cache-api/pkg/api"
	cache_api_http_v1 "github.com/JeffreyJPZ/timestamped-for-f1-cache-api/pkg/api/http/v1"
	"github.com/JeffreyJPZ/timestamped-for-f1-cache-api/pkg/cache"
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
		fmt.Printf("failed to connect to Redis. Error: %v", err)
	}

	// Register routes.
	router.HandleFunc(makePattern(http.MethodGet, "v1/get/{key}"), r.handleCacheGet(cache))
	router.HandleFunc(makePattern(http.MethodPut, "v1/set"), r.handleCacheSet(cache))

	return router
}

// handleCacheGet extracts a key from the URL path and creates a response
// indicating whether the key was in the cache or not.
func (r *Router) handleCacheGet(c cache.Cache) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set(cache_api_http_v1.HeaderAPIVersion, cache_api_http_v1.APIVersion)

		var response *cache_api_http_v1.CacheGetResponse

		// Extract key from wildcard in path.
		key := r.PathValue("key")

		// Get value from cache.
		ctx := r.Context()
		result, err := c.Get(ctx, key)
		if err != nil {
			response = &cache_api_http_v1.CacheGetResponse{
				Code:    cache_api.KEY_NOT_FOUND_ERROR.String(),
				Message: fmt.Errorf("key %s does not exist in cache", key).Error(),
			}
			jsonutils.MarshalResponse(w, http.StatusNotFound, *response)
			return
		}

		value, ok := result.(string)
		if !ok {
			response = &cache_api_http_v1.CacheGetResponse{
				Code:    cache_api.VALUE_INVALID_FORMAT_ERROR.String(),
				Message: fmt.Errorf("failed to coerce value %v associated with key %s to string", result, key).Error(),
			}
			jsonutils.MarshalResponse(w, http.StatusBadRequest, *response)
			return
		}

		response = &cache_api_http_v1.CacheGetResponse{
			Key:   key,
			Value: value,
		}
		jsonutils.MarshalResponse(w, http.StatusOK, *response)
	}
}

// handleCacheSet parses a key-value pair from the request body
// and creates/replaces the entry in the cache for the key.
func (r *Router) handleCacheSet(c cache.Cache) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set(cache_api_http_v1.HeaderAPIVersion, cache_api_http_v1.APIVersion)

		var data *cache_api_http_v1.CacheSetRequest
		var response *cache_api_http_v1.CacheSetResponse

		// Parse body (stored at data).
		status, err := jsonutils.Unmarshal(w, r, data)
		if status != http.StatusOK || err != nil || data == nil {
			response = &cache_api_http_v1.CacheSetResponse{
				Code:    cache_api.INVALID_REQUEST_ERROR.String(),
				Message: fmt.Errorf("failed to parse request body").Error(),
			}
			jsonutils.MarshalResponse(w, http.StatusBadRequest, *response)
			return
		}

		// Set key-value in cache.
		ctx := r.Context()
		err = c.Set(ctx, data.Key, data.Value, data.ExpirationTime)
		if err != nil {
			response = &cache_api_http_v1.CacheSetResponse{
				Code:    cache_api.CACHE_ERROR.String(),
				Message: fmt.Errorf("failed to set value %s for key %s", data.Value, data.Key).Error(),
			}
			jsonutils.MarshalResponse(w, http.StatusInternalServerError, *response)
			return
		}

		response = &cache_api_http_v1.CacheSetResponse{
			Key:   data.Key,
			Value: data.Value,
		}
		jsonutils.MarshalResponse(w, http.StatusOK, *response)
	}
}

// makePattern formats the given HTTP method and path as "method path".
func makePattern(method string, path string) string {
	return fmt.Sprintf("%s %s", method, path)
}
