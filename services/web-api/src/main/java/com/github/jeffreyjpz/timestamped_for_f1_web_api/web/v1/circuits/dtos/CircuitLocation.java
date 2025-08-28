package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.dtos;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class CircuitLocation {

    @JsonAlias({"angle"})
    @JsonProperty("angle")
    private final double angle;

    @JsonAlias({"coordinates"})
    @JsonProperty("coordinates")
    private final CircuitLocationCoordinates coordinates;

    @JsonAlias({"length"})
    @JsonProperty("length")
    private final double length;

    @JsonAlias({"number"})
    @JsonProperty("number")
    private final Integer number;

    @JsonAlias({"type"})
    @JsonProperty("type")
    private final String type;

}
