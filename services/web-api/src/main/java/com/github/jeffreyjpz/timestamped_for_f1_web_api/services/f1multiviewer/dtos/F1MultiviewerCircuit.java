package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer.dtos;

import java.util.List;
import java.util.Map;

public record F1MultiviewerCircuit(
    List<Map<String, Object>>       corners,
    List<Map<String, Object>>       marshalLights,
    List<Map<String, Object>>       marshalSectors,
    Map<String, Object>             candidateLap,
    String                          circuitKey,
    String                          circuitName,
    String                          countryIocCode,
    Integer                         countryKey,
    String                          countryName,
    String                          location,
    String                          meetingKey,
    String                          meetingName,
    String                          meetingOfficialName,
    List<Integer>                   miniSectorsIndexes,
    String                          raceDate,
    Integer                         rotation,
    Integer                         round,
    List<Integer>                   x,
    List<Integer>                   y,
    Integer                         year
) {}
