package redis

import (
	"fmt"
	"net/url"
)

type Config struct {
	Host     string
	Port     string
	User     string
	Password string
	DB       string
}

// ConnectionURL creates a Redis URL over TCP.
// If the receiver is nil, then ConnectionURL returns an empty string.
func (c *Config) ConnectionURL() string {
	if c == nil {
		return ""
	}

	// Format host and port in the format "host:port".
	h := c.Host
	if p := c.Port; p != "" {
		h = fmt.Sprintf("%s:%s", h, p)
	}

	// Create URL with database added to path.
	u := &url.URL{
		Scheme: "redis",
		Host:   h,
		Path:   c.DB,
	}

	// Add user and password if provided.
	if c.User != "" || c.Password != "" {
		u.User = url.UserPassword(c.User, c.Password)
	}

	return u.String()
}
