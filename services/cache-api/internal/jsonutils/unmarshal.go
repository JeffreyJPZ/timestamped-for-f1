// Taken from the Exposure Notifications Server authors
// at https://github.com/google/exposure-notifications-server/blob/2041f77a0bda55a67214d23dc18f26b3ab895fd1/internal/jsonutil/unmarshal.go

// Package jsonutil provides common utilities for properly handling JSON payloads in HTTP body.
package jsonutils

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"strings"
)

const (
	// Max request size of 64KB. None of the current API requests for this
	// server are near that limit. Prevents us from unnecessarily parsing JSON
	// payloads that are much large than we anticipate.
	maxBodyBytes = 64_000
)

// Unmarshal provides a common implementation of JSON unmarshalling with well defined error handling.
func Unmarshal(w http.ResponseWriter, r *http.Request, data any) (int, error) {
	if t := r.Header.Get("content-type"); len(t) < 16 || t[:16] != "application/json" {
		return http.StatusUnsupportedMediaType, fmt.Errorf("content-type is not application/json")
	}

	defer r.Body.Close()
	r.Body = http.MaxBytesReader(w, r.Body, maxBodyBytes)

	d := json.NewDecoder(r.Body)
	d.DisallowUnknownFields()

	if err := d.Decode(&data); err != nil {
		var syntaxErr *json.SyntaxError
		var unmarshalError *json.UnmarshalTypeError
		switch {
		case errors.As(err, &syntaxErr):
			return http.StatusBadRequest, fmt.Errorf("malformed json at position %d", syntaxErr.Offset)
		case errors.Is(err, io.ErrUnexpectedEOF):
			return http.StatusBadRequest, fmt.Errorf("malformed json")
		case errors.As(err, &unmarshalError):
			return http.StatusBadRequest, fmt.Errorf("invalid value %q at position %d", unmarshalError.Field, unmarshalError.Offset)
		case strings.HasPrefix(err.Error(), "json: unknown field"):
			fieldName := strings.TrimPrefix(err.Error(), "json: unknown field ")
			return http.StatusBadRequest, fmt.Errorf("unknown field %s", fieldName)
		case errors.Is(err, io.EOF):
			return http.StatusBadRequest, fmt.Errorf("body must not be empty")
		case err.Error() == "http: request body too large":
			return http.StatusRequestEntityTooLarge, err
		default:
			return http.StatusInternalServerError, fmt.Errorf("failed to decode json: %w", err)
		}
	}
	if d.More() {
		return http.StatusBadRequest, fmt.Errorf("body must contain only one JSON object")
	}

	return http.StatusOK, nil
}
