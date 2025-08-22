package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.drivers;

import java.time.Duration;
import java.util.List;
import java.util.Map;

import org.springframework.http.MediaType;
import org.springframework.util.CollectionUtils;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.jeffreyjpz.timestamped_for_f1_cache.cache_api_grpc_v1.CacheResult;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.cache.CacheService;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.cache.CacheServiceException;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.OpenF1Service;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.utils.CacheUtils;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.errors.exceptions.InvalidInstanceException;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.drivers.dtos.Driver;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@RestController
@RequestMapping(path = "/drivers", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
@Slf4j
public class DriverController {

    private final CacheService cacheService;
    private final OpenF1Service openf1Service;

    private final ObjectMapper objectMapper;

    @GetMapping("")
    public List<Driver> getDrivers(@RequestParam MultiValueMap<String, String> queryParams) {
        List<Driver> drivers = null;

        try {
            drivers = objectMapper.readValue(
                objectMapper.writeValueAsString(openf1Service.getDrivers(queryParams)),
                new TypeReference<List<Driver>>(){}
            );
        } catch (JsonProcessingException e) {
            log.error("data transformation failed", e);
        }

        return drivers;
    }

    @GetMapping("/{meetingKey}/{sessionKey}/{driverNumber}")
    public Driver getDriver(@PathVariable Integer meetingKey, @PathVariable Integer sessionKey, @PathVariable Integer driverNumber) {
        String cacheKey = CacheUtils.buildCacheKey(
            "drivers",
            String.valueOf(meetingKey),
            String.valueOf(sessionKey),
            String.valueOf(driverNumber)
        );

        // Perform a cache lookup.
        CacheResult cacheGetResult = null;
        try {
            cacheGetResult = cacheService.get(cacheKey);
        } catch (CacheServiceException e) {
            log.error("cache lookup failed to complete", e);
        }

        // If value associated with key derived from query parameters is in cache, return cache result.
        if (
            cacheGetResult != null &&
            cacheGetResult.hasField(cacheGetResult.getDescriptorForType().findFieldByNumber(CacheResult.KEY_FIELD_NUMBER)) &&
            cacheGetResult.hasField(cacheGetResult.getDescriptorForType().findFieldByNumber(CacheResult.VALUE_FIELD_NUMBER))
        ) {
            try {
                return objectMapper.readValue(cacheGetResult.getValue(), new TypeReference<Driver>(){});
            } catch (JsonProcessingException e) {
                log.error("cache value object coercion failed", e);
            }
        } else if (
            cacheGetResult != null &&
            cacheGetResult.hasField(cacheGetResult.getDescriptorForType().findFieldByNumber(CacheResult.CODE_FIELD_NUMBER)) &&
            cacheGetResult.hasField(cacheGetResult.getDescriptorForType().findFieldByNumber(CacheResult.MESSAGE_FIELD_NUMBER))
        ) {
            log.info(
                String.format(
                    "cache get internal failure with code: %s and message %s",
                    cacheGetResult.getCode(),
                    cacheGetResult.getMessage()
                )
            );
        }

        // Otherwise, query OpenF1 and transform data.
        List<Driver> drivers = null;
        MultiValueMap<String, String> queryParams = CollectionUtils.toMultiValueMap(
            Map.ofEntries(
                Map.entry("meeting_key", List.of(String.valueOf(meetingKey))),
                Map.entry("session_key", List.of(String.valueOf(sessionKey))),
                Map.entry("driver_number", List.of(String.valueOf(driverNumber))
            ))
        );

        try {
            drivers = objectMapper.readValue(
                objectMapper.writeValueAsString(openf1Service.getDrivers(queryParams)),
                new TypeReference<List<Driver>>(){}
            );
        } catch (JsonProcessingException e) {
            log.error("data transformation failed", e);
        }
        
        if (drivers == null) throw new InvalidInstanceException();

        Driver driver = drivers
            .stream()
            .filter(
                d -> d.getMeetingKey().equals(meetingKey) &&
                    d.getSessionKey().equals(sessionKey) &&
                    d.getDriverNumber().equals(driverNumber)
            )
            .findFirst()
            .orElse(null);

        if (driver == null) throw new InvalidInstanceException();

        // Cache OpenF1 results with a TTL of 5 minutes.
        CacheResult cacheSetResult = null;
        try {
            cacheSetResult = cacheService.set(
                cacheKey,
                objectMapper.writeValueAsString(driver),
                Duration.ofMinutes(5).toSeconds()
            );
        } catch (CacheServiceException e) {
            log.error("cache set failed to complete", e);
        } catch (JsonProcessingException e) {
            log.error("cache value string coercion failed", e);
        }

        if (
            cacheSetResult != null &&
            cacheSetResult.hasField(cacheSetResult.getDescriptorForType().findFieldByNumber(CacheResult.CODE_FIELD_NUMBER)) &&
            cacheSetResult.hasField(cacheSetResult.getDescriptorForType().findFieldByNumber(CacheResult.MESSAGE_FIELD_NUMBER))
        ) {
            log.info(
                String.format(
                    "cache set internal failure with code: %s and message %s",
                    cacheSetResult.getCode(),
                    cacheSetResult.getMessage()
                )
            );
        }

        return driver;
    }
}
