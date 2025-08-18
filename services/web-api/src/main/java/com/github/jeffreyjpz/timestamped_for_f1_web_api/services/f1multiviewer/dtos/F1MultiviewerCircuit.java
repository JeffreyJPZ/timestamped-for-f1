package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer.dtos;

import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.OptBoolean;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class F1MultiviewerCircuit {
    @JsonProperty(value = "corners", isRequired = OptBoolean.TRUE)
    private final List<F1MultiviewerCircuitLocation> corners;

    @JsonProperty(value = "marshalLights", isRequired = OptBoolean.TRUE)
    private final List<F1MultiviewerCircuitLocation> marshalLights;

    @JsonProperty(value = "marshalSectors", isRequired = OptBoolean.TRUE)
    private final List<F1MultiviewerCircuitLocation> marshalSectors;

    @JsonProperty(value = "candidateLap", isRequired = OptBoolean.TRUE)
    private final Map<String, Object> candidateLap;

    @JsonProperty(value = "circuitKey", isRequired = OptBoolean.TRUE)
    private final String circuitKey;

    @JsonProperty(value = "circuitName", isRequired = OptBoolean.TRUE)
    private final String circuitName;

    @JsonProperty(value = "countryIocCode", isRequired = OptBoolean.TRUE)
    private final String countryIocCode;

    @JsonProperty(value = "countryKey", isRequired = OptBoolean.TRUE)
    private final Integer countryKey;

    @JsonProperty(value = "countryName", isRequired = OptBoolean.TRUE)
    private final String countryName;

    @JsonProperty(value = "location", isRequired = OptBoolean.TRUE)
    private final String location;

    @JsonProperty(value = "meetingKey", isRequired = OptBoolean.TRUE)
    private final String meetingKey;

    @JsonProperty(value = "meetingName", isRequired = OptBoolean.TRUE)
    private final String meetingName;

    @JsonProperty(value = "meetingOfficialName", isRequired = OptBoolean.TRUE)
    private final String meetingOfficialName;

    @JsonProperty(value = "miniSectorsIndexes", isRequired = OptBoolean.TRUE)
    private final List<Integer> miniSectorsIndexes;

    @JsonProperty(value = "raceDate", isRequired = OptBoolean.TRUE)
    private final String raceDate;

    @JsonProperty(value = "rotation", isRequired = OptBoolean.TRUE)
    private final Integer rotation;

    @JsonProperty(value = "round", isRequired = OptBoolean.TRUE)
    private final Integer round;

    @JsonProperty(value = "x", isRequired = OptBoolean.TRUE)
    private final List<Integer> x;

    @JsonProperty(value = "y", isRequired = OptBoolean.TRUE)
    private final List<Integer> y;

    @JsonProperty(value = "year", isRequired = OptBoolean.TRUE)
    private final Integer year;
}
