package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import java.util.Map;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class OpenF1Event {
    private final String category;
    private final String cause;
    private final String date;
    private final Map<String, Object> details;
    private final Integer meeting_key;
    private final Integer session_key;
}
