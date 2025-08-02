// The response types for the cache API.
package v1

type CacheGetResponse struct {
	Key   string `json:"key,omitempty"`
	Value string `json:"value,omitempty"`

	ErrorCode    string `json:"code,omitempty"`
	ErrorMessage string `json:"message,omitempty"`
}

type CacheSetResponse struct {
	Key   string `json:"key,omitempty"`
	Value string `json:"value,omitempty"`

	ErrorCode    string `json:"code,omitempty"`
	ErrorMessage string `json:"message,omitempty"`
}
