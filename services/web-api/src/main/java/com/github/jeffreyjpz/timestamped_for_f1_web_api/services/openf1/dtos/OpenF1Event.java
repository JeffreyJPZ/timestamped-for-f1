package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import java.util.Map;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.OptBoolean;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class OpenF1Event {
    
    @JsonProperty(value = "category", isRequired = OptBoolean.TRUE)
    private final String category;

    @JsonProperty(value = "cause", isRequired = OptBoolean.TRUE)
    private final String cause;

    @JsonProperty(value = "date", isRequired = OptBoolean.TRUE)
    private final String date;

    @JsonProperty(value = "details", isRequired = OptBoolean.TRUE)
    private final Map<String, Object> details;

    @JsonProperty(value = "meeting_key", isRequired = OptBoolean.TRUE)
    private final Integer meeting_key;

    @JsonProperty(value = "session_key", isRequired = OptBoolean.TRUE)
    private final Integer session_key;
}
