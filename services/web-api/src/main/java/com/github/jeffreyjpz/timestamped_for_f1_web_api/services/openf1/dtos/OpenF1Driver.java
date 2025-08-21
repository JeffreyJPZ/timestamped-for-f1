package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.OptBoolean;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class OpenF1Driver {
    
    @JsonProperty(value = "broadcast_name", isRequired = OptBoolean.TRUE)
    private final String broadcast_name;

    @JsonProperty(value = "country_code", isRequired = OptBoolean.TRUE)
    private final String country_code;

    @JsonProperty(value = "driver_number", isRequired = OptBoolean.TRUE)
    private final Integer driver_number;

    @JsonProperty(value = "first_name", isRequired = OptBoolean.TRUE)
    private final String first_name;

    @JsonProperty(value = "full_name", isRequired = OptBoolean.TRUE)
    private final String full_name;

    @JsonProperty(value = "headshot_url", isRequired = OptBoolean.TRUE)
    private final String headshot_url;

    @JsonProperty(value = "last_name", isRequired = OptBoolean.TRUE)
    private final String last_name;

    @JsonProperty(value = "meeting_key", isRequired = OptBoolean.TRUE)
    private final Integer meeting_key;

    @JsonProperty(value = "name_acronym", isRequired = OptBoolean.TRUE)
    private final String name_acronym;

    @JsonProperty(value = "session_key", isRequired = OptBoolean.TRUE)
    private final Integer session_key;

    @JsonProperty(value = "team_colour", isRequired = OptBoolean.TRUE)
    private final String team_colour;

    @JsonProperty(value = "team_name", isRequired = OptBoolean.TRUE)
    private final String team_name;
}
