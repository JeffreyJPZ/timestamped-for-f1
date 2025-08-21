package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.errors;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

/**
 * Structure of error response body for the web API.
 */
@Getter
@RequiredArgsConstructor
public class ErrorDetails {

    private final String message;
    private final String instance;
    private final String timestamp;
    private final String type;
    
}
