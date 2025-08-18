package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.OptBoolean;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class OpenF1Driver {
    @JsonProperty(value = "broadcastName", isRequired = OptBoolean.TRUE)
    private final String broadcast_name;

    @JsonProperty(value = "countryCode", isRequired = OptBoolean.TRUE)
    private final String country_code;

    @JsonProperty(value = "driverNumber", isRequired = OptBoolean.TRUE)
    private final Integer driver_number;

    @JsonProperty(value = "firstName", isRequired = OptBoolean.TRUE)
    private final String first_name;

    @JsonProperty(value = "full_name", isRequired = OptBoolean.TRUE)
    private final String full_name;

    @JsonProperty(value = "headshotUrl", isRequired = OptBoolean.TRUE)
    private final String headshot_url;

    @JsonProperty(value = "lastName", isRequired = OptBoolean.TRUE)
    private final String last_name;

    @JsonProperty(value = "meetingKey", isRequired = OptBoolean.TRUE)
    private final Integer meeting_key;

    @JsonProperty(value = "nameAcronym", isRequired = OptBoolean.TRUE)
    private final String name_acronym;

    @JsonProperty(value = "sessionKey", isRequired = OptBoolean.TRUE)
    private final Integer session_key;

    @JsonProperty(value = "teamColour", isRequired = OptBoolean.TRUE)
    private final String team_colour;

    @JsonProperty(value = "teamName", isRequired = OptBoolean.TRUE)
    private final String team_name;
}
