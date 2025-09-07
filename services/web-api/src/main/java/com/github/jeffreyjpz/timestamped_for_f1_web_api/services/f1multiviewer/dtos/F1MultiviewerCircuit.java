package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer.dtos;

import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class F1MultiviewerCircuit {

    @JsonAlias(value = "corners")
    @JsonProperty(value = "corners")
    private final List<F1MultiviewerCircuitLocation> corners;

    @JsonAlias(value = "marshalLights")
    @JsonProperty(value = "marshalLights")
    private final List<F1MultiviewerCircuitLocation> marshalLights;

    @JsonAlias(value = "marshalSectors")
    @JsonProperty(value = "marshalSectors")
    private final List<F1MultiviewerCircuitLocation> marshalSectors;

    @JsonAlias(value = "candidateLap")
    @JsonProperty(value = "candidateLap")
    private final Map<String, Object> candidateLap;

    @JsonAlias(value = "circuitKey")
    @JsonProperty(value = "circuitKey")
    private final String circuitKey;

    @JsonAlias(value = "circuitName")
    @JsonProperty(value = "circuitName")
    private final String circuitName;

    @JsonAlias(value = "countryIocCode")
    @JsonProperty(value = "countryIocCode")
    private final String countryIocCode;

    @JsonAlias(value = "countryKey")
    @JsonProperty(value = "countryKey")
    private final Integer countryKey;

    @JsonAlias(value = "countryName")
    @JsonProperty(value = "countryName")
    private final String countryName;

    @JsonAlias(value = "location")
    @JsonProperty(value = "location")
    private final String location;

    @JsonAlias(value = "meetingKey")
    @JsonProperty(value = "meetingKey")
    private final String meetingKey;

    @JsonAlias(value = "meetingName")
    @JsonProperty(value = "meetingName")
    private final String meetingName;

    @JsonAlias(value = "meetingOfficialName")
    @JsonProperty(value = "meetingOfficialName")
    private final String meetingOfficialName;

    @JsonAlias(value = "miniSectorsIndexes")
    @JsonProperty(value = "miniSectorsIndexes")
    private final List<Integer> miniSectorsIndexes;

    @JsonAlias(value = "raceDate")
    @JsonProperty(value = "raceDate")
    private final String raceDate;

    @JsonAlias(value = "rotation")
    @JsonProperty(value = "rotation")
    private final Integer rotation;

    @JsonAlias(value = "round")
    @JsonProperty(value = "round")
    private final Integer round;

    @JsonAlias(value = "x")
    @JsonProperty(value = "x")
    private final List<Integer> x;

    @JsonAlias(value = "y")
    @JsonProperty(value = "y")
    private final List<Integer> y;

    @JsonAlias(value = "year")
    @JsonProperty(value = "year")
    private final Integer year;
}
