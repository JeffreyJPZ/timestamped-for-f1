package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class OpenF1Driver {
    
    @JsonAlias("broadcast_name")
    @JsonProperty("broadcast_name")
    private final String broadcastName;

    @JsonAlias("country_code")
    @JsonProperty("country_code")
    private final String countryCode;

    @JsonAlias("driver_number")
    @JsonProperty("driver_number")
    private final Integer driverNumber;

    @JsonAlias("first_name")
    @JsonProperty("first_name")
    private final String firstName;

    @JsonAlias("full_name")
    @JsonProperty("full_name")
    private final String fullName;

    @JsonAlias("headshot_url")
    @JsonProperty("headshot_url")
    private final String headshotUrl;

    @JsonAlias("last_name")
    @JsonProperty("last_name")
    private final String lastName;

    @JsonAlias("meeting_key")
    @JsonProperty("meeting_key")
    private final Integer meetingKey;

    @JsonAlias("name_acronym")
    @JsonProperty("name_acronym")
    private final String nameAcronym;

    @JsonAlias("session_key")
    @JsonProperty("session_key")
    private final Integer sessionKey;

    @JsonAlias("team_colour")
    @JsonProperty("team_colour")
    private final String teamColour;

    @JsonAlias("team_name")
    @JsonProperty("team_name")
    private final String teamName;

}
