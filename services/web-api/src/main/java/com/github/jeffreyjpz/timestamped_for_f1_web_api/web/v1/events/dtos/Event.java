package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.events.dtos;

import java.util.Map;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class Event {
    
    @JsonAlias("category")
    @JsonProperty("category")
    private final String category;

    @JsonAlias("cause")
    @JsonProperty("cause")
    private final String cause;

    @JsonAlias("date")
    @JsonProperty("date")
    private final String date;

    @JsonAlias({"elapsedTime", "elapsed_time"})
    @JsonProperty("elapsed_time")
    private final String elapsedTime;

    @JsonAlias("details")
    @JsonProperty("details")
    private final Map<String, Object> details;

    @JsonAlias({"meetingKey", "meeting_key"})
    @JsonProperty("meeting_key")
    private final Integer meetingKey;

    @JsonAlias({"sessionKey", "session_key"})
    @JsonProperty("session_key")
    private final Integer sessionKey;

}
