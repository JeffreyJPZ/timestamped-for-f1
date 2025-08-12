package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.events;

import java.time.Duration;
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
import com.github.jeffreyjpz.timestamped_for_f1_cache.cache_api_grpc_v1.CacheResult;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.cache.CacheService;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.cache.CacheServiceException;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.OpenF1Response;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.OpenF1Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@RestController
@RequestMapping(path = "/events", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
@Slf4j
public class EventController {

    private final CacheService cacheService;
    private final OpenF1Service openf1Service;

    private final ObjectMapper objectMapper;

    @GetMapping(path = "")
    public List<OpenF1Response.Event> getEvents(@RequestParam MultiValueMap<String, String> queryParams) {
        CacheResult cacheGetResult = null;

        // Perform a cache lookup.
        try {
            cacheGetResult = cacheService.get("foo");
        } catch (CacheServiceException e) {
            log.error("cache lookup failed to complete", e);
        }

        // If value associated with key derived from query parameters is in cache, return cache result.
        if (
            cacheGetResult != null &&
            cacheGetResult.hasField(cacheGetResult.getDescriptorForType().findFieldByNumber(CacheResult.KEY_FIELD_NUMBER)) &&
            cacheGetResult.hasField(cacheGetResult.getDescriptorForType().findFieldByNumber(CacheResult.VALUE_FIELD_NUMBER))
        ) {
            List<OpenF1Response.Event> value;

            try {
                value = objectMapper.readValue(cacheGetResult.getValue(), new TypeReference<List<OpenF1Response.Event>>(){});
                return value;
            } catch (JsonProcessingException e) {
                log.error("cache value object coercion failed", e);
            } finally {
                if (cacheGetResult != null &&
                    cacheGetResult.hasField(cacheGetResult.getDescriptorForType().findFieldByNumber(CacheResult.CODE_FIELD_NUMBER)) &&
                    cacheGetResult.hasField(cacheGetResult.getDescriptorForType().findFieldByNumber(CacheResult.MESSAGE_FIELD_NUMBER))
                ) {
                    log.info(
                        String.format(
                            "cache get internal failure. code: %s message %s",
                            cacheGetResult.getCode(),
                            cacheGetResult.getMessage()
                        )
                    );
                }
            }
        }

        // Otherwise, query OpenF1.
        List<OpenF1Response.Event> events = openf1Service.getEvents(queryParams);;
        CacheResult cacheSetResult = null;

        // Cache OpenF1 results with a TTL of 5 minutes.
        try {
            String value = objectMapper.writeValueAsString(events);
            cacheService.set("foo", value, Duration.ofMinutes(5).toSeconds());
        } catch (CacheServiceException e) {
            log.error("cache set failed to complete", e);
        } catch (JsonProcessingException e) {
            log.error("cache value string coercion failed", e);
        } finally {
            if (cacheSetResult != null &&
                cacheSetResult.hasField(cacheSetResult.getDescriptorForType().findFieldByNumber(CacheResult.CODE_FIELD_NUMBER)) &&
                cacheSetResult.hasField(cacheSetResult.getDescriptorForType().findFieldByNumber(CacheResult.MESSAGE_FIELD_NUMBER))
            ) {
                log.info(
                    String.format(
                        "cache set internal failure. code: %s message %s",
                        cacheSetResult.getCode(),
                        cacheSetResult.getMessage()
                    )
                );
            }
        }

        return events;
    }
}
