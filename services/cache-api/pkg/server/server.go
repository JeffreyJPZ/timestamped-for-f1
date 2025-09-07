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

	grpc_cache_service "github.com/JeffreyJPZ/timestamped-for-f1-cache-api/internal/grpc"
	pb "github.com/JeffreyJPZ/timestamped-for-f1-cache-api/pkg/api/grpc/v1"
	"google.golang.org/grpc"
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
		return nil, fmt.Errorf("failed to create listener on address %s. Error: %v", address, err)
	}

	return &Server{
		ip:       listener.Addr().(*net.TCPAddr).IP.String(),
		port:     strconv.Itoa(listener.Addr().(*net.TCPAddr).Port),
		listener: listener,
	}, nil
}

// ServeHTTPWithHandler enables the server to accept incoming HTTP requests on its listener.
// When it is executed, it blocks when the server begins serving,
// and shuts down gracefully when its context is closed. After it is closed, the server cannot be reused.
func (s *Server) ServeHTTPWithHandler(ctx context.Context, handler http.Handler) error {
	// Create http server struct with defaults.
	sHTTP := &http.Server{
		ReadHeaderTimeout: 5 * time.Second, // This allows handlers to set per-request timeouts.
		Handler:           handler,
	}

	// Handle server shutdown.
	shutdownErrCh := make(chan error, 1)
	go func() {
		// Wait for server context to close.
		<-ctx.Done()

		// Create a timed context with a server shutdown grace period of 5 seconds.
		timeoutCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
		defer cancel()

		shutdownErrCh <- sHTTP.Shutdown(timeoutCtx)
	}()

	// Run the server and block.
	if err := sHTTP.Serve(s.Listener()); err != nil && !errors.Is(err, http.ErrServerClosed) {
		return fmt.Errorf("failed to serve on address %s. Error: %v", s.Address(), err)
	}

	// Return any error during the shutdown process.
	if err := <-shutdownErrCh; err != nil {
		return fmt.Errorf("shutdown failure on address %s. Error: %v", s.Address(), err)
	}

	return nil
}

// ServeGRPC enables the server to accept gRPC requests on its listener.
// When it is executed, it blocks when the server begins serving,
// and shuts down gracefully when its context is closed. After it is closed, the server cannot be reused.
func (s *Server) ServeGRPC(ctx context.Context) error {

	// Register unary interceptor with timeout of 5 seconds.
	interceptor := grpc.UnaryInterceptor(func(ctx context.Context, req any, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (resp any, err error) {
		timeoutCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
		defer cancel()

		return handler(timeoutCtx, req)
	})

	sGRPC := grpc.NewServer(interceptor)

	// Start and register cache service.
	cache_service, err := grpc_cache_service.NewService()
	if err != nil {
		return fmt.Errorf("failed to serve on address %s. Error: %v", s.Address(), err)
	}

	pb.RegisterCacheServer(sGRPC, cache_service)

	// Handle server shutdown.
	shutdownErrCh := make(chan error, 1)
	go func() {
		// Wait for server context to close.
		<-ctx.Done()

		// Create a timed context with a server shutdown grace period of 5 seconds.
		timeoutCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
		defer cancel()

		errCh := make(chan error, 1)
		go func() {
			sGRPC.GracefulStop()
			close(errCh)
		}()

		select {
		case <-errCh:
			// Server successfully shut down.
			shutdownErrCh <- nil
		case <-timeoutCtx.Done():
			// Timeout elapsed.
			shutdownErrCh <- fmt.Errorf("shutdown timed out on address %s", s.Address())
		}
	}()

	// Run the server and block.
	if err := sGRPC.Serve(s.Listener()); err != nil && !errors.Is(err, grpc.ErrServerStopped) {
		return fmt.Errorf("failed to serve on address %s. Error: %v", s.Address(), err)
	}

	// Return any error during the shutdown process.
	if err := <-shutdownErrCh; err != nil {
		return fmt.Errorf("shutdown failure on address %s. Error: %v", s.Address(), err)
	}

	return nil
}

// Address returns the server's IP and port in the form of a network address "ip:port".
func (s *Server) Address() string {
	return net.JoinHostPort(s.ip, s.port)
}

// IP returns the IP address that the server's listener is bound to.
func (s *Server) IP() string {
	return s.ip
}

// Port returns the port that the server's listener is bound to.
func (s *Server) Port() string {
	return s.port
}

// Listener returns the server listener for the server.
func (s *Server) Listener() net.Listener {
	return s.listener
}
