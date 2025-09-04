package grpc

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/JeffreyJPZ/timestamped-for-f1-cache-api/pkg/server"
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
	s, err := server.NewServer(
		os.Getenv("TIMESTAMPED_FOR_F1_CACHE_API_IP"),
		os.Getenv("TIMESTAMPED_FOR_F1_CACHE_API_PORT"),
	)

	if err != nil {
		return fmt.Errorf("failed to start server. Error: %v", err)
	}

	return s.ServeGRPC(ctx)
}
