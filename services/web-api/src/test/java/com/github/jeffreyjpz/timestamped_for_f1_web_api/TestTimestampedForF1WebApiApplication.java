package com.github.jeffreyjpz.timestamped_for_f1_web_api;

import org.springframework.boot.SpringApplication;

public class TestTimestampedForF1WebApiApplication {

	public static void main(String[] args) {
		SpringApplication.from(TimestampedForF1WebApiApplication::main).with(TestcontainersConfiguration.class).run(args);
	}

}
