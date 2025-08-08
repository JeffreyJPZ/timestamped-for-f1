package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer;

import java.util.List;
import java.util.Map;

/**
 * Response types for the F1 Multiviewer API.
 */
public class F1MultiviewerResponse {

    public record Circuit(
        List<Map<String, Object>> corners,
        List<Map<String, Object>> marshalLights,
        List<Map<String, Object>> marshalSectors,
        Map<String, Object> candidateLap,
        String circuitKey,
        String circuitName,
        String countryIocCode,
        Integer countryKey,
        String countryName,
        String location,
        String meetingKey,
        String meetingName,
        String meetingOfficialName,
        List<Integer> miniSectorsIndexes,
        String raceDate,
        Integer rotation,
        Integer round,
        List<Integer> x,
        List<Integer> y,
        Integer year
    ) {}
}
