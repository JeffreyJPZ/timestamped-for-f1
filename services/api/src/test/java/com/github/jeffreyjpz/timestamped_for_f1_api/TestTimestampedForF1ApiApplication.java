package com.github.jeffreyjpz.timestamped_for_f1_api;

import org.springframework.boot.SpringApplication;

public class TestTimestampedForF1ApiApplication {

	public static void main(String[] args) {
		SpringApplication.from(TimestampedForF1ApiApplication::main).with(TestcontainersConfiguration.class).run(args);
	}

}
