package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.dtos;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.OptBoolean;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class CircuitLocation {
    @JsonProperty(value = "angle", isRequired = OptBoolean.TRUE)
    private final double angle;

    @JsonProperty(value = "length", isRequired = OptBoolean.TRUE)
    private final double length;

    @JsonProperty(value = "number", isRequired = OptBoolean.TRUE)
    private final Integer number;

    @JsonProperty(value = "coordinates", isRequired = OptBoolean.TRUE)
    private final CircuitLocationCoordinates coordinates;
}
