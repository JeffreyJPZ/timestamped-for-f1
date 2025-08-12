package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.dtos;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class CircuitLocation {
    private final double angle;
    private final double length;
    private final Integer number;
    private final CircuitLocationCoordinates trackPosition;
}
