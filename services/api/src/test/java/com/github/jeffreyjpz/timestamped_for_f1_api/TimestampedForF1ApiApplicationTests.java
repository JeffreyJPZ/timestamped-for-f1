package com.github.jeffreyjpz.timestamped_for_f1_api;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;

@Import(TestcontainersConfiguration.class)
@SpringBootTest
class TimestampedForF1ApiApplicationTests {

	@Test
	void contextLoads() {
	}

}
