package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.dtos;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.OptBoolean;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class Circuit {
    @JsonProperty(value = "rotation", isRequired = OptBoolean.TRUE)
    private final Integer rotation;

    @JsonProperty(value = "marshalSectors", isRequired = OptBoolean.TRUE)
    private final List<CircuitLocation> marshalSectors;

    @JsonProperty(value = "miniSectors", isRequired = OptBoolean.TRUE)
    private final List<CircuitLocation> miniSectors;

    @JsonProperty(value = "coordinates", isRequired = OptBoolean.TRUE)
    private final List<CircuitLocationCoordinates> coordinates;

    @JsonProperty(value = "turns", isRequired = OptBoolean.TRUE)
    private final List<CircuitLocation> turns;
}
