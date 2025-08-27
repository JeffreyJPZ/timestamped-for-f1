package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class OpenF1Session {
    
    @JsonAlias(value = "circuit_key")
    @JsonProperty(value = "circuitKey")
    private final Integer circuitKey;

    @JsonAlias("circuit_short_name")
    @JsonProperty("circuitShortName")
    private final String circuitShortName;

    @JsonAlias("country_code")
    @JsonProperty("countryCode")
    private final String countryCode;

    @JsonAlias("country_key")
    @JsonProperty("countryKey")
    private final Integer countryKey;

    @JsonAlias("country_name")
    @JsonProperty("countryName")
    private final String countryName;

    @JsonAlias("date_end")
    @JsonProperty("dateEnd")
    private final String dateEnd;

    @JsonAlias("date_start")
    @JsonProperty("dateStart")
    private final String dateStart;

    @JsonAlias("gmt_offset")
    @JsonProperty("gmtOffset")
    private final String gmtOffset;

    @JsonAlias("location")
    @JsonProperty("location")
    private final String location;

    @JsonAlias("meeting_key")
    @JsonProperty("meetingKey")
    private final Integer meetingKey;

    @JsonAlias("session_key")
    @JsonProperty("sessionKey")
    private final Integer sessionKey;

    @JsonAlias("session_name")
    @JsonProperty("sessionName")
    private final String sessionName;

    @JsonAlias("session_type")
    @JsonProperty("sessionType")
    private final String sessionType;

    @JsonAlias("year")
    @JsonProperty("year")
    private final Integer year;
}
