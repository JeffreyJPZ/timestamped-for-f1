package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class OpenF1Meeting {
    
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

    @JsonAlias("meeting_name")
    @JsonProperty("meetingName")
    private final String meetingName;

    @JsonAlias("meeting_official_name")
    @JsonProperty("meetingOfficialName")
    private final String meetingOfficialName;

    @JsonAlias("year")
    @JsonProperty("year")
    private final Integer year;
}
