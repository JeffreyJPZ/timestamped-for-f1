package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@ConfigurationProperties(prefix = "f1multiviewer.service") 
@ConfigurationPropertiesScan
@RequiredArgsConstructor
@Getter
public class F1MultiviewerServiceConfigurationProperties { 

    private final String baseUrl;
    
}
