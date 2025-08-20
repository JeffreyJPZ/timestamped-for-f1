package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.meetings.dtos;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.OptBoolean;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class Meeting {
    @JsonProperty(value = "circuitKey", isRequired = OptBoolean.TRUE)
    private final Integer circuitKey;

    @JsonProperty(value = "circuitShortName", isRequired = OptBoolean.TRUE)
    private final String circuitShortName;

    @JsonProperty(value = "countryCode", isRequired = OptBoolean.TRUE)
    private final String countryCode;

    @JsonProperty(value = "countryKey", isRequired = OptBoolean.TRUE)
    private final Integer countryKey;

    @JsonProperty(value = "countryName", isRequired = OptBoolean.TRUE)
    private final String countryName;

    @JsonProperty(value = "dateStart", isRequired = OptBoolean.TRUE)
    private final String dateStart;

    @JsonProperty(value = "gmtOffset", isRequired = OptBoolean.TRUE)
    private final String gmtOffset;

    @JsonProperty(value = "location", isRequired = OptBoolean.TRUE)
    private final String location;

    @JsonProperty(value = "meetingKey", isRequired = OptBoolean.TRUE)
    private final Integer meetingKey;

    @JsonProperty(value = "meetingName", isRequired = OptBoolean.TRUE)
    private final String meetingName;

    @JsonProperty(value = "meetingOfficialName", isRequired = OptBoolean.TRUE)
    private final String meetingOfficialName;

    @JsonProperty(value = "year", isRequired = OptBoolean.TRUE)
    private final Integer year;
}