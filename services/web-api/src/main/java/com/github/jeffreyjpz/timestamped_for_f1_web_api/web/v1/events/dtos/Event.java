package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.events.dtos;

import java.util.Map;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.OptBoolean;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class Event {
    @JsonProperty(value = "category", isRequired = OptBoolean.TRUE)
    private final String category;

    @JsonProperty(value = "cause", isRequired = OptBoolean.TRUE)
    private final String cause;

    @JsonProperty(value = "date", isRequired = OptBoolean.TRUE)
    private final String date;

    @JsonProperty(value = "details", isRequired = OptBoolean.TRUE)
    private final Map<String, Object> details;

    @JsonProperty(value = "meetingKey", isRequired = OptBoolean.TRUE)
    private final Integer meetingKey;

    @JsonProperty(value = "sessionKey", isRequired = OptBoolean.TRUE)
    private final Integer sessionKey;
}
