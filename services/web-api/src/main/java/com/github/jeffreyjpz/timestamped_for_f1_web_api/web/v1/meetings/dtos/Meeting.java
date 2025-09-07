package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.meetings.dtos;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class Meeting {

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

    @JsonAlias({"meetingName", "meeting_name"})
    @JsonProperty("meeting_name")
    private final String meetingName;

    @JsonAlias({"meetingOfficialName", "meeting_official_name"})
    @JsonProperty("meeting_official_name")
    private final String meetingOfficialName;

    @JsonAlias({"year"})
    @JsonProperty("year")
    private final Integer year;

}
