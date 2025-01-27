#!/bin/bash
# Create/update config files for rest connectors

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

# Check if config file exists at given path
check_config_file() {
    local connector=$1
    local config_file="config/${connector}-source.json"
    
    if [ ! -f "$config_file" ]; then
        echo "Error: Config file not found: $config_file"
        return 1
    fi
    return 0
}

# Loop through each connector and update its configuration
for connector in "${connectors[@]}"; do
    echo "Updating configuration for ${connector}-source-connector..."
    
    if ! check_config_file "$connector" ; then
        echo "Skipping ${connector}-source-connector due to missing config file"
        echo
        continue
    fi
    
    response=$(curl -X PUT \
        -H 'Host: connect.example.com' \
        -H 'Accept: application/json' \
        -H 'Content-Type: application/json' \
        -d "@config/${connector}-source.json" \
        -s -w "\n%{http_code}" \
        "${BASE_URL}/${connector}-source-connector/config")
    
    http_code=$(echo "$response" | tail -n 1)
    response_body=$(echo "$response" | sed \$d)
    
    case $http_code in
        200)
            echo "Successfully updated ${connector}-source-connector"
            ;;
        201)
            echo "Successfully created ${connector}-source-connector"
            ;;
        404)
            echo "Error: Connector ${connector}-source-connector not found"
            echo "Response: $response_body"
            ;;
        *)
            echo "Error: Unexpected status code $http_code for ${connector}-source-connector"
            echo "Response: $response_body"
            ;;
    esac
    
    echo
done

echo "Connector update process complete."