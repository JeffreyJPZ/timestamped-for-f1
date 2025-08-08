package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1;

import java.util.Map;

/**
 * Response types for the OpenF1 API.
 */
public class OpenF1Response {
    
    public record Driver(
        String broadcast_name,
        String country_code,
        Integer driver_number,
        String first_name,
        String full_name,
        String headshot_url,
        String last_name,
        Integer meeting_key,
        String name_acronym,
        Integer session_key,
        String team_colour,
        String team_name
    ) {}

    public record Event(
        String category,
        String cause,
        String date,
        Map<String, Object> details,
        Integer meeting_key,
        Integer session_key
    ) {}

    public record Meeting(
        Integer circuit_key,
        String circuit_short_name,
        String country_code,
        Integer country_key,
        String country_name,
        String date_start,
        String gmt_offset,
        String location,
        Integer meeting_key,
        String meeting_name,
        String meeting_official_name,
        Integer year
    ) {}

    public record Session(
        Integer circuit_key,
        String circuit_short_name,
        String country_code,
        Integer country_key,
        String country_name,
        String date_end,
        String date_start,
        String gmt_offset,
        String location,
        Integer meeting_key,
        Integer session_key,
        String session_name,
        String session_type,
        Integer year
    ) {}
}
