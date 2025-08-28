package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.sessions.dtos;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class Session {
    
    @JsonAlias({"circuitKey", "circuit_key"})
    @JsonProperty("circuit_key")
    private final Integer circuitKey;

    @JsonAlias({"circuitShortName", "circuit_short_name"})
    @JsonProperty("circuit_short_name")
    private final String circuitShortName;

    @JsonAlias({"countryCode", "country_code"})
    @JsonProperty("country_code")
    private final String countryCode;

    @JsonAlias({"countryKey", "country_key"})
    @JsonProperty("country_key")
    private final Integer countryKey;

    @JsonAlias({"countryName", "country_name"})
    @JsonProperty("country_name")
    private final String countryName;

    @JsonAlias({"dateEnd", "date_end"})
    @JsonProperty("date_end")
    private final String dateEnd;

    @JsonAlias({"dateStart", "date_start"})
    @JsonProperty("date_start")
    private final String dateStart;

    @JsonAlias({"gmtOffset", "gmt_offset"})
    @JsonProperty("gmt_offset")
    private final String gmtOffset;

    @JsonAlias({"location"})
    @JsonProperty("location")
    private final String location;

    @JsonAlias({"meetingKey", "meeting_key"})
    @JsonProperty("meeting_key")
    private final Integer meetingKey;

    @JsonAlias({"sessionKey", "session_key"})
    @JsonProperty("session_key")
    private final Integer sessionKey;

    @JsonAlias({"sessionName", "session_name"})
    @JsonProperty("session_name")
    private final String sessionName;

    @JsonAlias({"sessionType", "session_type"})
    @JsonProperty("session_type")
    private final String sessionType;

    @JsonAlias({"year"})
    @JsonProperty("year")
    private final Integer year;

}
