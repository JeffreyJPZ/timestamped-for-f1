package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.dtos;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class CircuitLocationCoordinates {

    @JsonAlias({"x"})
    @JsonProperty("x")
    private final double x;

    @JsonAlias({"y"})
    @JsonProperty("y")
    private final double y;

}
