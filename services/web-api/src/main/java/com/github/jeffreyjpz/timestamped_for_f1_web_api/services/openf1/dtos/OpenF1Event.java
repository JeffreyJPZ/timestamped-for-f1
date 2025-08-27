package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import java.util.Map;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class OpenF1Event {
    
    @JsonAlias("category")
    @JsonProperty("category")
    private final String category;

    @JsonAlias("cause")
    @JsonProperty("cause")
    private final String cause;

    @JsonAlias("date")
    @JsonProperty("date")
    private final String date;

    @JsonAlias("details")
    @JsonProperty("details")
    private final Map<String, Object> details;

    @JsonAlias("meeting_key")
    @JsonProperty("meetingKey")
    private final Integer meetingKey;

    @JsonAlias("session_key")
    @JsonProperty("sessionKey")
    private final Integer sessionKey;
}
