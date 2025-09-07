// Defines error codes for the cache API.
package v1

type ErrorCode int

const (
	KEY_NOT_FOUND_ERROR ErrorCode = iota
	VALUE_INVALID_FORMAT_ERROR
	INVALID_REQUEST_ERROR
	CACHE_ERROR
)

var errorCodes = map[ErrorCode]string{
	KEY_NOT_FOUND_ERROR:        "KEY_NOT_FOUND",
	VALUE_INVALID_FORMAT_ERROR: "VALUE_INVALID_FORMAT",
	INVALID_REQUEST_ERROR:      "INVALID_REQUEST",
	CACHE_ERROR:                "CACHE_ERROR",
}

func (c ErrorCode) String() string {
	return errorCodes[c]
}
