package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer.dtos;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class F1MultiviewerCircuitLocationCoordinates {

    @JsonAlias(value = "x")
    @JsonProperty(value = "x")
    private final double x;

    @JsonAlias(value = "y")
    @JsonProperty(value = "y")
    private final double y;
}
