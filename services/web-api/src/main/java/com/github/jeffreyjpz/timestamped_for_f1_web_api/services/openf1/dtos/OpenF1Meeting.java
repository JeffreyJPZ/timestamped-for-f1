package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class OpenF1Meeting {
    private final Integer circuit_key;
    private final String circuit_short_name;
    private final String country_code;
    private final Integer country_key;
    private final String country_name;
    private final String date_start;
    private final String gmt_offset;
    private final String location;
    private final Integer meeting_key;
    private final String meeting_name;
    private final String meeting_official_name;
    private final Integer year;
}
