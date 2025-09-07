// The request body types for the cache API.
package v1

type CacheSetRequest struct {
	// The new key for the cache item.
	Key string `json:"key"`
	// The new value of the cache item.
	Value string `json:"value"`
	// The TTL for the cache item, in seconds.
	ExpirationTime float64 `json:"expirationTime"`
}
