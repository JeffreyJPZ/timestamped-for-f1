package server

import (
	"context"
	"fmt"
	"net/http"
	"os/signal"
	"syscall"

	"github.com/JeffreyJPZ/timestamped-for-f1-cache/pkg/server"
)

func main() {
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)

	defer func() {
		stop()
	}()

	err := serve(ctx)
	stop()

	if err != nil {
		panic(err)
	}
}

func serve(ctx context.Context) error {
	srv, err := server.NewServer("", "5555")

	if err != nil {
		return fmt.Errorf("server.main: failed to start server. Error: %v", err)
	}

	return srv.ServeHTTPWithHandler(ctx, &http.ServeMux{})
}
