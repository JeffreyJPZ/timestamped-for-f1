package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer.dtos;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.OptBoolean;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class F1MultiviewerCircuitLocationCoordinates {
    @JsonProperty(value = "x", isRequired = OptBoolean.TRUE)
    private final double x;

    @JsonProperty(value = "y", isRequired = OptBoolean.TRUE)
    private final double y;
}
