package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import java.util.Map;

public record OpenF1Event(
    String                  category,
    String                  cause,
    String                  date,
    Map<String, Object>     details,
    Integer                 meeting_key,
    Integer                 session_key
) {}
