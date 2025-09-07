# Build binary
FROM golang:1.25-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

# Build executables for gRPC and HTTP
RUN CGO_ENABLED=0 GOOS=linux go build -o timestamped-for-f1-cache-api-grpc ./cmd/server/grpc
RUN CGO_ENABLED=0 GOOS=linux go build -o timestamped-for-f1-cache-api-http ./cmd/server/http

# Copy binary to production image
FROM alpine:3.22

WORKDIR /app

COPY --from=builder /app/timestamped-for-f1-cache-api-grpc ./
COPY --from=builder /app/timestamped-for-f1-cache-api-http ./
RUN chmod +x ./timestamped-for-f1-cache-api-grpc
RUN chmod +x ./timestamped-for-f1-cache-api-http

RUN apk --no-cache add ca-certificates tzdata

RUN adduser -D nonroot
USER nonroot:nonroot

ENTRYPOINT ["/app/timestamped-for-f1-cache-api-grpc"]

