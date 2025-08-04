// The response types for the cache API.
package v1

type CacheGetResponse struct {
	// The key for the cache item, if the item exists.
	Key string `json:"key,omitempty"`
	// The value of the cache item, if the item exists.
	Value string `json:"value,omitempty"`

	// Unique error code, if the cache item does not exist.
	Code string `json:"code,omitempty"`
	// Error details, if the cache item does not exist.
	Message string `json:"message,omitempty"`
}

type CacheSetResponse struct {
	// The key for the cache item, if the item exists.
	Key string `json:"key,omitempty"`
	// The value of the cache item, if the item exists.
	Value string `json:"value,omitempty"`

	// Unique error code, if the cache item does not exist.
	Code string `json:"code,omitempty"`
	// Error details, if the cache item does not exist.
	Message string `json:"message,omitempty"`
}
