# !/bin/bash
# Adds date and date_start query params to respective config source files
# Call this periodically to ensure that response size is acceptable

parent_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
lower_bound_date=$(date -u -d @$(($(date +"%s") - 60)) +"%Y-%m-%dT%H:%M:%S") # Datetime 1 minute ago

# Car data
url="$(jq --arg lower_bound_date "$lower_bound_date" '.["rest.source.url"] = "https://api.openf1.org/v1/car_data?session_key=latest&date_start>\($lower_bound_date)"' ${parent_dir}/config/car-data-source.json)" && \
    echo -E "${url}" > "${parent_dir}/config/car-data-source.json"

# Intervals
url="$(jq --arg lower_bound_date "$lower_bound_date" '.["rest.source.url"] = "https://api.openf1.org/v1/car_data?session_key=latest&date>\($lower_bound_date)"' ${parent_dir}/config/intervals-source.json)" && \
    echo -E "${url}" > "${parent_dir}/config/intervals-source.json"

# Laps
url="$(jq --arg lower_bound_date "$lower_bound_date" '.["rest.source.url"] = "https://api.openf1.org/v1/laps?session_key=latest&date_start>\($lower_bound_date)"' ${parent_dir}/config/laps-source.json)" && \
    echo -E "${url}" > "${parent_dir}/config/laps-source.json"

# Location
url="$(jq --arg lower_bound_date "$lower_bound_date" '.["rest.source.url"] = "https://api.openf1.org/v1/location?session_key=latest&date>\($lower_bound_date)"' ${parent_dir}/config/location-source.json)" && \
    echo -E "${url}" > "${parent_dir}/config/location-source.json"

# Pit
url="$(jq --arg lower_bound_date "$lower_bound_date" '.["rest.source.url"] = "https://api.openf1.org/v1/pit?session_key=latest&date>\($lower_bound_date)"' ${parent_dir}/config/pit-source.json)" && \
    echo -E "${url}" > "${parent_dir}/config/pit-source.json"

# Position
url="$(jq --arg lower_bound_date "$lower_bound_date" '.["rest.source.url"] = "https://api.openf1.org/v1/position?session_key=latest&date>\($lower_bound_date)"' ${parent_dir}/config/position-source.json)" && \
    echo -E "${url}" > "${parent_dir}/config/position-source.json"

# Race Control
url="$(jq --arg lower_bound_date "$lower_bound_date" '.["rest.source.url"] = "https://api.openf1.org/v1/race_control?session_key=latest&date>\($lower_bound_date)"' ${parent_dir}/config/race-control-source.json)" && \
    echo -E "${url}" > "${parent_dir}/config/race-control-source.json"

# Weather
url="$(jq --arg lower_bound_date "$lower_bound_date" '.["rest.source.url"] = "https://api.openf1.org/v1/weather?session_key=latest&date>\($lower_bound_date)"' ${parent_dir}/config/weather-source.json)" && \
    echo -E "${url}" > "${parent_dir}/config/weather-source.json"