package com.github.jeffreyjpz.timestamped_for_f1_web_api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

@SpringBootApplication
@ConfigurationPropertiesScan("com.github.jeffreyjpz.timestamped_for_f1_web_api.services.cache")
public class TimestampedForF1WebApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(TimestampedForF1WebApiApplication.class, args);
	}

}
