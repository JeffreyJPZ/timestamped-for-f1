#!/bin/bash
# Adds date and date_start query params to appropriate config source files
# Call this periodically to ensure that response size is acceptable

# OpenF1 API

BASE_URL="https://api.openf1.org/v1"
parent_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
lower_bound_date=$(date -u -d @$(($(date +"%s") - 60)) +"%Y-%m-%dT%H:%M:%S") # Datetime 1 minute ago

# Change this to choose the exact F1 session for the connector
session_key="latest"

declare -A date_param_name=(
    ["car-data"]="date_start"
    ["intervals"]="date"
    ["laps"]="date_start"
    ["location"]="date"
    ["pit"]="date"
    ["position"]="date"
    ["race-control"]="date"
    ["weather"]="date"
)

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

echo "Updating date filters for connectors..."

for connector in "${!date_param_name[@]}"; do
    echo "Updating date configuration for ${connector}..."
    
    # Check if config file exists
    if ! check_config_file "$connector"; then
        echo "Skipping ${connector}-source-connector due to missing config file"
        echo
        continue
    fi

    date_param="${date_param_name[$connector]}"
    
    api_endpoint="${connector}"
    # Convert hyphens to underscores for OpenF1 API
    api_endpoint="${api_endpoint//-/_}"
    
    url="$(jq '.["rest.source.url"] = "'"${BASE_URL}"'/'"${api_endpoint}"'?session_key='"${session_key}"'&'"${date_param}"'>'"${lower_bound_date}"'"' \
        "${parent_dir}/config/${connector}-source.json")" && \
    echo -E "${url}" > "${parent_dir}/config/${connector}-source.json"
    
    echo "Updated ${connector} configuration with ${date_param} parameter with value ${lower_bound_date}"
    echo
done

echo "All connector configurations have been updated."