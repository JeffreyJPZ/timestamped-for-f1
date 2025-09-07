package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer.dtos;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class F1MultiviewerCircuitLocation {

    @JsonAlias(value = "angle")
    @JsonProperty(value = "angle")
    private final double angle;

    @JsonAlias(value = "length")
    @JsonProperty(value = "length")
    private final double length;

    @JsonAlias(value = "number")
    @JsonProperty(value = "number")
    private final Integer number;

    @JsonAlias(value = "trackPosition")
    @JsonProperty(value = "trackPosition")
    private final F1MultiviewerCircuitLocationCoordinates trackPosition;
}
