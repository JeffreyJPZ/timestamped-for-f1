package com.github.jeffreyjpz.timestamped_for_f1_api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.reactive.config.EnableWebFlux;

@SpringBootApplication
@EnableWebFlux
public class TimestampedForF1ApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(TimestampedForF1ApiApplication.class, args);
	}

}
