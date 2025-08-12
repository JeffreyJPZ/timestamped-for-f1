package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class OpenF1Driver {
    private final String broadcast_name;
    private final String country_code;
    private final Integer driver_number;
    private final String first_name;
    private final String full_name;
    private final String headshot_url;
    private final String last_name;
    private final Integer meeting_key;
    private final String name_acronym;
    private final Integer session_key;
    private final String team_colour;
    private final String team_name;
}
