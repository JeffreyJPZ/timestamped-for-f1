package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.drivers.dtos;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.OptBoolean;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class Driver {
    @JsonProperty(value = "broadcastName", isRequired = OptBoolean.TRUE)
    private final String broadcastName;

    @JsonProperty(value = "countryCode", isRequired = OptBoolean.TRUE)
    private final String countryCode;

    @JsonProperty(value = "driverNumber", isRequired = OptBoolean.TRUE)
    private final Integer driverNumber;

    @JsonProperty(value = "firstName", isRequired = OptBoolean.TRUE)
    private final String firstName;

    @JsonProperty(value = "fullName", isRequired = OptBoolean.TRUE)
    private final String fullName;

    @JsonProperty(value = "headshotUrl", isRequired = OptBoolean.TRUE)
    private final String headshotUrl;

    @JsonProperty(value = "lastName", isRequired = OptBoolean.TRUE)
    private final String lastName;

    @JsonProperty(value = "meetingKey", isRequired = OptBoolean.TRUE)
    private final Integer meetingKey;

    @JsonProperty(value = "nameAcronym", isRequired = OptBoolean.TRUE)
    private final String nameAcronym;

    @JsonProperty(value = "sessionKey", isRequired = OptBoolean.TRUE)
    private final Integer sessionKey;

    @JsonProperty(value = "teamColour", isRequired = OptBoolean.TRUE)
    private final String teamColour;

    @JsonProperty(value = "teamName", isRequired = OptBoolean.TRUE)
    private final String teamName;
}
