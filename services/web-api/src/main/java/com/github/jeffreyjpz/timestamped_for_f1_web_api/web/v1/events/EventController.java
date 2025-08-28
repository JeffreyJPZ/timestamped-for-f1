package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.events;

import java.util.List;

import org.springframework.http.MediaType;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.OpenF1Service;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.events.dtos.Event;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@RestController
@RequestMapping(path = "/api/v1/events", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
@Slf4j
public class EventController {
    private final OpenF1Service openf1Service;

    private final ObjectMapper objectMapper;

    @GetMapping("")
    public List<Event> getEvents(@RequestParam MultiValueMap<String, String> queryParams) {
        List<Event> events = null;

        try {
            events = objectMapper.readValue(
                objectMapper.writeValueAsString(
                    openf1Service.getEvents(queryParams)
                ),
                new TypeReference<List<Event>>(){}
            );
        } catch (JsonProcessingException e) {
            log.error("data transformation failed", e);
        }

        return events;
    }
}
