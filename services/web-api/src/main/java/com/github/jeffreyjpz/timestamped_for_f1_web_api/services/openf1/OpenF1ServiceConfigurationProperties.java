package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@ConfigurationProperties(prefix = "openf1.service")
@ConfigurationPropertiesScan
@RequiredArgsConstructor
@Getter
public class OpenF1ServiceConfigurationProperties { 

    private final String baseUrl;
    
}
