package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos;

public record OpenF1Session(
    Integer                 circuit_key,
    String                  circuit_short_name,
    String                  country_code,
    Integer                 country_key,
    String                  country_name,
    String                  date_end,
    String                  date_start,
    String                  gmt_offset,
    String                  location,
    Integer                 meeting_key,
    Integer                 session_key,
    String                  session_name,
    String                  session_type,
    Integer                 year
) {}
