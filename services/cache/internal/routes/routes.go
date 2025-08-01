package routes

import (
	"net/http"
)

type Router struct{}

// Routes registers the HTTP handlers for the cache API.
func (r *Router) Routes() *http.ServeMux {
	router := &http.ServeMux{}

	router.HandleFunc("GET /v1/cache/get", r.handleCacheGet())
	router.HandleFunc("PUT /v1/cache/set", r.handleCacheSet())

	return router
}

// TODO: implement
func (r *Router) handleCacheGet() func(http.ResponseWriter, *http.Request) {
	return nil
}

// TODO: implement
func (r *Router) handleCacheSet() func(http.ResponseWriter, *http.Request) {
	return nil
}
