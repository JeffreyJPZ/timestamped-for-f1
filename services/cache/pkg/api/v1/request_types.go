// The request body types for the cache API.
package v1

type CacheSetRequest struct {
	Key            string  `json:"key"`
	Value          string  `json:"value"`
	ExpirationTime float64 `json:"expirationTime"` // Time in seconds
}
