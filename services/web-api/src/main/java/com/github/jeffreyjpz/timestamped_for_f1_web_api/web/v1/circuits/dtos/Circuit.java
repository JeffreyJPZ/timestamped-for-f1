package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.dtos;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class Circuit {

    @JsonAlias({"circuitKey", "circuit_key"})
    @JsonProperty("circuit_key")
    private final String circuitKey;

    @JsonAlias({"circuitName", "circuit_name"})
    @JsonProperty("circuit_name")
    private final String circuitName;

    @JsonAlias({"coordinates"})
    @JsonProperty("coordinates")
    private final List<CircuitLocationCoordinates> coordinates;

    @JsonAlias({"countryCode", "country_code"})
    @JsonProperty("country_code")
    private final String countryCode;

    @JsonAlias({"countryKey", "country_key"})
    @JsonProperty("country_key")
    private final Integer countryKey;

    @JsonAlias({"countryName", "country_name"})
    @JsonProperty("country_name")
    private final String countryName;

    @JsonAlias({"location"})
    @JsonProperty("location")
    private final String location;

    @JsonAlias({"marshalSectors", "marshal_sectors"})
    @JsonProperty("marshal_sectors")
    private final List<CircuitLocation> marshalSectors;

    @JsonAlias({"miniSectors", "mini_sectors"})
    @JsonProperty("mini_sectors")
    private final List<CircuitLocation> miniSectors;

    @JsonAlias({"rotation"})
    @JsonProperty("rotation")
    private final Integer rotation;

    @JsonAlias({"turns"})
    @JsonProperty("turns")
    private final List<CircuitLocation> turns;

    @JsonAlias({"year"})
    @JsonProperty("year")
    private final Integer year;

}
