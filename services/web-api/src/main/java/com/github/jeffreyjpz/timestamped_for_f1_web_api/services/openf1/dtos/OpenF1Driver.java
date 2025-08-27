package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class OpenF1Driver {
    
    @JsonAlias(value = "broadcast_name")
    @JsonProperty(value = "broadcastName")
    private final String broadcastName;

    @JsonAlias(value = "country_code")
    @JsonProperty(value = "countryCode")
    private final String countryCode;

    @JsonAlias(value = "driver_number")
    @JsonProperty(value = "driverNumber")
    private final Integer driverNumber;

    @JsonAlias(value = "first_name")
    @JsonProperty(value = "firstName")
    private final String firstName;

    @JsonAlias(value = "full_name")
    @JsonProperty(value = "fullName")
    private final String fullName;

    @JsonAlias(value = "headshot_url")
    @JsonProperty(value = "headshotUrl")
    private final String headshotUrl;

    @JsonAlias(value = "last_name")
    @JsonProperty(value = "lastName")
    private final String lastName;

    @JsonAlias("meeting_key")
    @JsonProperty("meetingKey")
    private final Integer meetingKey;

    @JsonAlias("name_acronym")
    @JsonProperty("nameAcronym")
    private final String nameAcronym;

    @JsonAlias("session_key")
    @JsonProperty("sessionKey")
    private final Integer sessionKey;

    @JsonAlias("team_colour")
    @JsonProperty("teamColour")
    private final String teamColour;

    @JsonAlias("team_name")
    @JsonProperty("teamName")
    private final String teamName;
}
