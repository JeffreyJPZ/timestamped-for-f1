package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuit_locations;

import java.util.ArrayList;
import java.util.List;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.cache.CacheService;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer.F1MultiviewerService;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuit_locations.dtos.CircuitLocation;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@RestController
@RequestMapping(path = "/circuit-locations", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
@Slf4j
public class CircuitLocationController {
    
    private final CacheService cacheService;
    private final F1MultiviewerService f1MultiviewerService;

    private final ObjectMapper objectMapper;

    // Given a circuit key and year, return the rotation needed to display the circuit.
    @GetMapping(path = "/{id}/{year}/rotation")
    public Integer getCircuitRotation() {
        return 0;
    }

    // Given a circuit key and year, return all of the x, y coords needed to draw the circuit.
    @GetMapping(path = "/{id}/{year}/points")
    public List<CircuitLocation> getCircuitPoints() {
        return new ArrayList<CircuitLocation>();
    }

    // Given a circuit key and year, return all of the turn x, y, z coords.
    @GetMapping(path = "/{id}/{year}/turns")
    public List<CircuitLocation> getTurnLocations() {
        return new ArrayList<CircuitLocation>();
    }

    // Given a circuit key, year and turn number, return the turn x, y coords.
    @GetMapping(path = "/{id}/{year}/turns/{number}")
    public List<CircuitLocation> getTurnLocation() {
        return new ArrayList<CircuitLocation>();
    }

    // Given a circuit key and year, return all of the mini sector x, y coords.
    @GetMapping(path = "/{id}/{year}/mini-sectors")
    public List<CircuitLocation> getMiniSectorLocations() {
        return new ArrayList<CircuitLocation>();
    }

    // Given a circuit key, year and mini sector number, return the mini sector x, y coords.
    @GetMapping(path = "/{id}/{year}/mini-sectors/{number}")
    public List<CircuitLocation> getMiniSectorLocation() {
        return new ArrayList<CircuitLocation>();
    }

    // Given a circuit key we return all of the marshal sector x, y coords.
    @GetMapping(path = "/{id}/{year}/marshal-sectors")
    public List<CircuitLocation> getMarshalSectorLocations() {
        return new ArrayList<CircuitLocation>();
    }

    // Given a circuit key, year and marshal sector number, return the marshal sector x, y coords.
    @GetMapping(path = "/{id}/{year}/marshal-ssectors/{number}")
    public List<CircuitLocation> getMarshalSectorLocation() {
        return new ArrayList<CircuitLocation>();
    }

}
