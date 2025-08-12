package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

public record OpenF1Driver(
    String                  broadcast_name,
    String                  country_code,
    Integer                 driver_number,
    String                  first_name,
    String                  full_name,
    String                  headshot_url,
    String                  last_name,
    Integer                 meeting_key,
    String                  name_acronym,
    Integer                 session_key,
    String                  team_colour,
    String                  team_name
) {}
