package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class OpenF1Meeting {
    
    @JsonAlias("circuit_short_name")
    @JsonProperty("circuit_short_name")
    private final String circuitShortName;

    @JsonAlias("country_code")
    @JsonProperty("country_code")
    private final String countryCode;

    @JsonAlias("country_key")
    @JsonProperty("country_key")
    private final Integer countryKey;

    @JsonAlias("country_name")
    @JsonProperty("country_name")
    private final String countryName;

    @JsonAlias("date_start")
    @JsonProperty("date_start")
    private final String dateStart;

    @JsonAlias("gmt_offset")
    @JsonProperty("gmt_offset")
    private final String gmtOffset;

    @JsonAlias("location")
    @JsonProperty("location")
    private final String location;

    @JsonAlias("meeting_key")
    @JsonProperty("meeting_key")
    private final Integer meetingKey;

    @JsonAlias("meeting_name")
    @JsonProperty("meeting_name")
    private final String meetingName;

    @JsonAlias("meeting_official_name")
    @JsonProperty("meeting_official_name")
    private final String meetingOfficialName;

    @JsonAlias("year")
    @JsonProperty("year")
    private final Integer year;

}
