package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.OptBoolean;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class OpenF1Session {
    
    @JsonProperty(value = "circuit_key", isRequired = OptBoolean.TRUE)
    private final Integer circuit_key;

    @JsonProperty(value = "circuit_short_name", isRequired = OptBoolean.TRUE)
    private final String circuit_short_name;

    @JsonProperty(value = "country_code", isRequired = OptBoolean.TRUE)
    private final String country_code;

    @JsonProperty(value = "country_key", isRequired = OptBoolean.TRUE)
    private final Integer country_key;

    @JsonProperty(value = "country_name", isRequired = OptBoolean.TRUE)
    private final String country_name;

    @JsonProperty(value = "date_end", isRequired = OptBoolean.TRUE)
    private final String date_end;

    @JsonProperty(value = "date_start", isRequired = OptBoolean.TRUE)
    private final String date_start;

    @JsonProperty(value = "gmt_offset", isRequired = OptBoolean.TRUE)
    private final String gmt_offset;

    @JsonProperty(value = "location", isRequired = OptBoolean.TRUE)
    private final String location;

    @JsonProperty(value = "meeting_key", isRequired = OptBoolean.TRUE)
    private final Integer meeting_key;

    @JsonProperty(value = "session_key", isRequired = OptBoolean.TRUE)
    private final Integer session_key;

    @JsonProperty(value = "session_name", isRequired = OptBoolean.TRUE)
    private final String session_name;

    @JsonProperty(value = "session_type", isRequired = OptBoolean.TRUE)
    private final String session_type;

    @JsonProperty(value = "year", isRequired = OptBoolean.TRUE)
    private final Integer year;
}
