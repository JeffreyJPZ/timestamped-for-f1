package com.github.jeffreyjpz.timestamped_for_f1_web_api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer.F1MultiviewerServiceConfigurationProperties;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.OpenF1ServiceConfigurationProperties;

@SpringBootApplication
@ConfigurationPropertiesScan(
	basePackageClasses = {
		F1MultiviewerServiceConfigurationProperties.class,
		OpenF1ServiceConfigurationProperties.class
	}
)
public class TimestampedForF1WebApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(TimestampedForF1WebApiApplication.class, args);
	}

}
