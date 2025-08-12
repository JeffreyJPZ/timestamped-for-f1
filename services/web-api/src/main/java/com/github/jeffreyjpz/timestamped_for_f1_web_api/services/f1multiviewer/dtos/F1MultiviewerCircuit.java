package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer.dtos;

import java.util.List;
import java.util.Map;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class F1MultiviewerCircuit {
    private final List<Map<String, Object>> corners;
    private final List<Map<String, Object>> marshalLights;
    private final List<Map<String, Object>> marshalSectors;
    private final Map<String, Object> candidateLap;
    private final String circuitKey;
    private final String circuitName;
    private final String countryIocCode;
    private final Integer countryKey;
    private final String countryName;
    private final String location;
    private final String meetingKey;
    private final String meetingName;
    private final String meetingOfficialName;
    private final List<Integer> miniSectorsIndexes;
    private final String raceDate;
    private final Integer rotation;
    private final Integer round;
    private final List<Integer> x;
    private final List<Integer> y;
    private final Integer year;
}
