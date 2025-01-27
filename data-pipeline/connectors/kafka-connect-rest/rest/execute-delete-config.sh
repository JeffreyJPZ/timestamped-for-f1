#!/bin/bash
# Delete connectors and config files for rest connectors using Kafka Connect REST interface
# Assumes connector names are {connector}-source-connector

connectors=(
    "car-data"
    "drivers"
    "intervals"
    "laps"
    "location"
    "meetings"
    "pit"
    "position"
    "race-control"
    "sessions"
    "stints"
    "weather"
)

# Base URL for the connect service
BASE_URL="http://localhost:8083/connectors"

for connector in "${connectors[@]}"; do
    echo "Deleting connector: ${connector}-source-connector..."
    
    response=$(curl -X DELETE \
        -H 'Host: connect.example.com' \
        -s -w "\n%{http_code}" \
        "${BASE_URL}/${connector}-source-connector")
    
    http_code=$(echo "$response" | tail -n 1)
    
    if [ "$http_code" -eq 204 ]; then
        echo "Successfully deleted ${connector}-source-connector"
    else
        echo "Failed to delete ${connector}-source-connector (HTTP Status: ${http_code})"
    fi
    
    echo
done

echo "Connector deletion process complete."