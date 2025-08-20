package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits;

import java.util.ArrayList;
import java.util.List;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.cache.CacheService;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer.F1MultiviewerService;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.dtos.Circuit;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@RestController
@RequestMapping(path = "/circuits", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
@Slf4j
public class CircuitController {
    
    private final CacheService cacheService;
    private final F1MultiviewerService f1MultiviewerService;

    private final ObjectMapper objectMapper;

    @GetMapping(path = "")
    public List<Circuit> getCircuits() {
        return null;
    }

    @GetMapping(path = "/{id}")
    public Circuit getCircuit(@PathVariable("id") String id) {
        return null;
    }
}
