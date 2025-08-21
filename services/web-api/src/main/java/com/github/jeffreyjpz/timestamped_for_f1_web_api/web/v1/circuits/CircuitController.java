package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits;

import java.time.Duration;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.jeffreyjpz.timestamped_for_f1_cache.cache_api_grpc_v1.CacheResult;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.cache.CacheService;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.cache.CacheServiceException;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer.F1MultiviewerService;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer.dtos.F1MultiviewerCircuit;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.utils.CacheUtils;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.errors.exceptions.InvalidInstanceException;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.dtos.Circuit;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.dtos.CircuitLocation;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.dtos.CircuitLocationCoordinates;
import com.google.common.collect.Streams;

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

    @GetMapping("/{circuitKey}/{year}")
    public Circuit getCircuit(@PathVariable Integer circuitKey, @PathVariable Integer year) {
        String cacheKey = CacheUtils.buildCacheKey(
            "circuits",
            String.valueOf(circuitKey),
            String.valueOf(year)
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
                return objectMapper.readValue(cacheGetResult.getValue(), new TypeReference<Circuit>(){});
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

        // Otherwise, query F1Multiviewer and transform data.
        F1MultiviewerCircuit f1MultiviewerCircuit = f1MultiviewerService.getCircuit(String.valueOf(circuitKey), String.valueOf(year));
        
        if (f1MultiviewerCircuit == null) throw new InvalidInstanceException();

        List<CircuitLocationCoordinates> coordinates = Streams
            .zip(
                f1MultiviewerCircuit.getX().stream(),
                f1MultiviewerCircuit.getY().stream(),
                (x, y) -> new CircuitLocationCoordinates(
                    x.doubleValue(),
                    y.doubleValue()
                )
            )
            .collect(Collectors.toList());

        List<CircuitLocation> marshalSectors = f1MultiviewerCircuit.getMarshalSectors()
            .stream()
            .map(s -> new CircuitLocation(
                s.getAngle(),
                s.getLength(),
                s.getNumber(),
                new CircuitLocationCoordinates(s.getTrackPosition().getX(), s.getTrackPosition().getY())
            ))
            .collect(Collectors.toList());

        List<CircuitLocationCoordinates> miniSectors = f1MultiviewerCircuit.getMiniSectorsIndexes()
            .stream()
            .map(i -> new CircuitLocationCoordinates(
                f1MultiviewerCircuit.getX().get(i).doubleValue(),
                f1MultiviewerCircuit.getY().get(i).doubleValue()
            ))
            .collect(Collectors.toList());

        List<CircuitLocation> turns = f1MultiviewerCircuit.getCorners()
            .stream()
            .map(t -> new CircuitLocation(
                t.getAngle(),
                t.getLength(),
                t.getNumber(),
                new CircuitLocationCoordinates(t.getTrackPosition().getX(), t.getTrackPosition().getY())
            ))
            .collect(Collectors.toList());
        
        Circuit circuit = new Circuit(
            f1MultiviewerCircuit.getCircuitKey(),
            f1MultiviewerCircuit.getCircuitName(), 
            coordinates,
            f1MultiviewerCircuit.getCountryIocCode(),
            f1MultiviewerCircuit.getCountryKey(),
            f1MultiviewerCircuit.getCountryName(),
            f1MultiviewerCircuit.getLocation(),
            marshalSectors,
            miniSectors,
            f1MultiviewerCircuit.getRotation(),
            turns,
            year // F1Multiviewer currently does not have updated circuits for every year
        );

        // Cache OpenF1 results with a TTL of 5 minutes.
        CacheResult cacheSetResult = null;
        try {
            cacheSetResult = cacheService.set(
                cacheKey,
                objectMapper.writeValueAsString(circuit),
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

        return circuit;
    }
}
