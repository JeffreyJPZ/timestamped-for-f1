package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.drivers.dtos;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class Driver {

    @JsonAlias({"broadcastName", "broadcast_name"})
    @JsonProperty("broadcast_name")
    private final String broadcastName;

    @JsonAlias({"countryCode", "country_code"})
    @JsonProperty("country_code")
    private final String countryCode;

    @JsonAlias({"driverNumber", "driver_number"})
    @JsonProperty("driver_number")
    private final Integer driverNumber;

    @JsonAlias({"firstName", "first_name"})
    @JsonProperty("first_name")
    private final String firstName;

    @JsonAlias({"fullName", "full_name"})
    @JsonProperty("full_name")
    private final String fullName;

    @JsonAlias({"headshotUrl", "headshot_url"})
    @JsonProperty("headshot_url")
    private final String headshotUrl;

    @JsonAlias({"lastName", "last_name"})
    @JsonProperty("last_name")
    private final String lastName;

    @JsonAlias({"meetingKey", "meeting_key"})
    @JsonProperty("meeting_key")
    private final Integer meetingKey;

    @JsonAlias({"nameAcronym", "name_acronym"})
    @JsonProperty("name_acronym")
    private final String nameAcronym;

    @JsonAlias({"sessionKey", "session_key"})
    @JsonProperty("session_key")
    private final Integer sessionKey;

    @JsonAlias({"teamColour", "team_colour"})
    @JsonProperty("team_colour")
    private final String teamColour;

    @JsonAlias({"teamName", "team_name"})
    @JsonProperty("team_name")
    private final String teamName;

}
