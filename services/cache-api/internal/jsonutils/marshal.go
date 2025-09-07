// Taken from the Exposure Notifications Server authors
// at https://github.com/google/exposure-notifications-server/blob/2041f77a0bda55a67214d23dc18f26b3ab895fd1/internal/jsonutil/marshal.go

package jsonutils

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

// MarshalResponse is a helper function to write a JSON serializable object to the http.ResponseWriter
// with fallback error template.
func MarshalResponse(w http.ResponseWriter, status int, response any) {
	w.Header().Set("Content-Type", "application/json")

	data, err := json.Marshal(response)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		msg := escapeJSON(err.Error())
		fmt.Fprintf(w, jsonErrTmpl, msg)
		return
	}

	w.WriteHeader(status)
	fmt.Fprintf(w, "%s", data)
	w.Write(data)
}

// escapeJSON does primitive JSON escaping.
func escapeJSON(s string) string {
	return strings.ReplaceAll(s, `"`, `\"`)
}

// jsonErrTmpl is the template to use when returning a JSON error. It is
// rendered using Printf, not json.Encode, so values must be escaped by the
// caller.
const jsonErrTmpl = `{"error":"%s"}`
