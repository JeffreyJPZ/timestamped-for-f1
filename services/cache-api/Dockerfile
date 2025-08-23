# Build binary
FROM golang:1.25-alpine AS build

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . ./

RUN CGO_ENABLED=0 GOOS=linux go build -o cache-api .

# Copy binary to production image
FROM alpine:3.22

WORKDIR /app

COPY --from=build /app/cache-api .

RUN apk --no-cache add ca-certificates tzdata

USER nonroot:nonroot

ENTRYPOINT ["/app/cache-api"]

