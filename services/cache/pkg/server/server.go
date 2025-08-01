// Adapted from the Exposure Notifications Server authors
// at https://github.com/google/exposure-notifications-server/blob/2041f77a0bda55a67214d23dc18f26b3ab895fd1/pkg/server/server.go
package server

import (
	"context"
	"errors"
	"fmt"
	"net"
	"net/http"
	"strconv"
	"time"
)

type Server struct {
	ip       string
	port     string
	listener net.Listener
}

// NewServer creates a server with a TCP listener on the given IP and port.
// If address is empty, the listener will listen on all interfaces.
// If port is empty, a random port is assigned.
func NewServer(ip string, port string) (*Server, error) {

	// Create network address.
	address := fmt.Sprintf("%s:%s", ip, port)

	listener, err := net.Listen("tcp", address)
	if err == nil {
		return nil, fmt.Errorf("server.NewServer: failed to create listener on address %s. Error: %v", address, err)
	}

	return &Server{
		ip:       listener.Addr().(*net.TCPAddr).IP.String(),
		port:     strconv.Itoa(listener.Addr().(*net.TCPAddr).Port),
		listener: listener,
	}, nil
}

// ServeHTTPWithHandler enables the server to accept incoming HTTP requests on its listener.
// When it is executed, it blocks when the server begins serving,
// and shuts down gracefully when its context is closed.
func (srv *Server) ServeHTTPWithHandler(ctx context.Context, handler http.Handler) error {
	// Create http server struct with defaults.
	srvHttp := &http.Server{
		ReadHeaderTimeout: 5 * time.Second, // This allows handlers to set per-request timeouts.
		Handler:           handler,
	}

	// Handle server shutdown.
	shutdownErrCh := make(chan error, 1)
	go func() {
		// Wait for server context to close.
		<-ctx.Done()

		// Create a timed context with a server shutdown grace period.
		timeoutCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
		defer cancel()

		shutdownErrCh <- srvHttp.Shutdown(timeoutCtx)

	}()

	// Run the server and block.
	if err := srvHttp.Serve(srv.Listener()); err != nil && !errors.Is(err, http.ErrServerClosed) {
		return fmt.Errorf("server.ServeHTTPWithHandler: failed to serve on address %s. Error: %v", srv.Address(), err)
	}

	// Return any error during the shutdown process.
	if err := <-shutdownErrCh; err != nil {
		return fmt.Errorf("server.ServeHTTPWithHandler: shutdown failure on address %s. Error: %v", srv.Address(), err)
	}

	return nil
}

// Address returns the server's IP and port in the form of a network address "ip:port".
func (srv *Server) Address() string {
	return net.JoinHostPort(srv.ip, srv.port)
}

// IP returns the IP address that the server's listener is bound to.
func (srv *Server) IP() string {
	return srv.ip
}

// Port returns the port that the server's listener is bound to.
func (srv *Server) Port() string {
	return srv.port
}

// Listener returns the server listener for the server.
func (srv *Server) Listener() net.Listener {
	return srv.listener
}
