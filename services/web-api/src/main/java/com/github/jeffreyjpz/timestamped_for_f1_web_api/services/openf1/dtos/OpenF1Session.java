package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.OptBoolean;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class OpenF1Session {
    @JsonProperty(value = "circuitKey", isRequired = OptBoolean.TRUE)
    private final Integer circuit_key;

    @JsonProperty(value = "circuitShortName", isRequired = OptBoolean.TRUE)
    private final String circuit_short_name;

    @JsonProperty(value = "countryCode", isRequired = OptBoolean.TRUE)
    private final String country_code;

    @JsonProperty(value = "countryKey", isRequired = OptBoolean.TRUE)
    private final Integer country_key;

    @JsonProperty(value = "countryName", isRequired = OptBoolean.TRUE)
    private final String country_name;

    @JsonProperty(value = "dateEnd", isRequired = OptBoolean.TRUE)
    private final String date_end;

    @JsonProperty(value = "dateStart", isRequired = OptBoolean.TRUE)
    private final String date_start;

    @JsonProperty(value = "gmtOffset", isRequired = OptBoolean.TRUE)
    private final String gmt_offset;

    @JsonProperty(value = "location", isRequired = OptBoolean.TRUE)
    private final String location;

    @JsonProperty(value = "meetingKey", isRequired = OptBoolean.TRUE)
    private final Integer meeting_key;

    @JsonProperty(value = "sessionKey", isRequired = OptBoolean.TRUE)
    private final Integer session_key;

    @JsonProperty(value = "sessionName", isRequired = OptBoolean.TRUE)
    private final String session_name;

    @JsonProperty(value = "sessionType", isRequired = OptBoolean.TRUE)
    private final String session_type;

    @JsonProperty(value = "year", isRequired = OptBoolean.TRUE)
    private final Integer year;
}
