package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits;

import java.time.Duration;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.CrossOrigin;
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
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.errors.exceptions.InvalidInstanceException;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.utils.CacheUtils;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.dtos.Circuit;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.dtos.CircuitLocation;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.dtos.CircuitLocationCoordinates;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.v1.circuits.types.CircuitLocationType;
import com.google.common.collect.Streams;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping(path = "/api/v1/circuits", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
@Slf4j
public class CircuitController {
    
    private final CacheService cacheService;
    private final F1MultiviewerService f1MultiviewerService;

    private final ObjectMapper objectMapper;

    @GetMapping("/{year}/{circuit_key}")
    public Circuit getCircuit(
        @PathVariable("year") Integer year,
        @PathVariable("circuit_key") Integer circuitKey
    ) {
        String cacheKey = CacheUtils.buildCacheKey(
            "circuits",
            String.valueOf(year),
            String.valueOf(circuitKey)
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
        F1MultiviewerCircuit f1MultiviewerCircuit = f1MultiviewerService.getCircuit(String.valueOf(year), String.valueOf(circuitKey));
        
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
                new CircuitLocationCoordinates(s.getTrackPosition().getX(), s.getTrackPosition().getY()),
                s.getLength(),
                s.getNumber(),
                CircuitLocationType.MARSHAL_SECTOR.toString()
                )
            )
            .collect(Collectors.toList());

        List<CircuitLocation> miniSectors = Streams
            .zip(
                IntStream.range(0, f1MultiviewerCircuit.getMiniSectorsIndexes().size()).boxed(),
                f1MultiviewerCircuit.getMiniSectorsIndexes().stream(),
                (n, i) -> new CircuitLocation(
                    0,
                    new CircuitLocationCoordinates(
                        f1MultiviewerCircuit.getX().get(i).doubleValue(),
                        f1MultiviewerCircuit.getY().get(i).doubleValue()
                    ),
                    0,
                    n + 1,
                    CircuitLocationType.MINI_SECTOR.toString()
                )
            )
            .collect(Collectors.toList());

        List<CircuitLocation> turns = f1MultiviewerCircuit.getCorners()
            .stream()
            .map(t ->
                new CircuitLocation(
                    t.getAngle(),
                    new CircuitLocationCoordinates(t.getTrackPosition().getX(), t.getTrackPosition().getY()),
                    t.getLength(),
                    t.getNumber(),
                    CircuitLocationType.TURN.toString()
                )
            )
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

        // Cache results with a TTL of 5 minutes.
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

    @GetMapping("/{year}/{circuit_key}/turns/{number}")
    public CircuitLocation getTurn(
        @PathVariable("year") Integer year,
        @PathVariable("circuit_key") Integer circuitKey,
        @PathVariable("number") Integer number
    ) {
        String cacheKey = CacheUtils.buildCacheKey(
            "turns",
            String.valueOf(year),
            String.valueOf(circuitKey),
            String.valueOf(number)
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
                return objectMapper.readValue(cacheGetResult.getValue(), new TypeReference<CircuitLocation>(){});
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
        F1MultiviewerCircuit f1MultiviewerCircuit = f1MultiviewerService.getCircuit(String.valueOf(year), String.valueOf(circuitKey));
        
        if (f1MultiviewerCircuit == null) throw new InvalidInstanceException();

        CircuitLocation turn = f1MultiviewerCircuit.getCorners()
            .stream()
            .filter(t -> t.getNumber().equals(number))
            .map(t ->
                new CircuitLocation(
                    t.getAngle(),
                    new CircuitLocationCoordinates(t.getTrackPosition().getX(), t.getTrackPosition().getY()),
                    t.getLength(),
                    t.getNumber(),
                    CircuitLocationType.TURN.toString()
                )
            )
            .findFirst()
            .orElse(null);
        
        if (turn == null) throw new InvalidInstanceException();

        // Cache results with a TTL of 5 minutes.
        CacheResult cacheSetResult = null;
        try {
            cacheSetResult = cacheService.set(
                cacheKey,
                objectMapper.writeValueAsString(turn),
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

        return turn;
    }

    @GetMapping("/{year}/{circuit_key}/marshal-sectors/{number}")
    public CircuitLocation getMarshalSector(
        @PathVariable("year") Integer year,
        @PathVariable("circuit_key") Integer circuitKey,
        @PathVariable("number") Integer number
    ) {
        String cacheKey = CacheUtils.buildCacheKey(
            "marshal-sectors",
            String.valueOf(year),
            String.valueOf(circuitKey),
            String.valueOf(number)
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
                return objectMapper.readValue(cacheGetResult.getValue(), new TypeReference<CircuitLocation>(){});
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
        F1MultiviewerCircuit f1MultiviewerCircuit = f1MultiviewerService.getCircuit(String.valueOf(year), String.valueOf(circuitKey));
        
        if (f1MultiviewerCircuit == null) throw new InvalidInstanceException();

        CircuitLocation marshalSector = f1MultiviewerCircuit.getMarshalSectors()
            .stream()
            .filter(t -> t.getNumber().equals(number))
            .map(t ->
                new CircuitLocation(
                    t.getAngle(),
                    new CircuitLocationCoordinates(t.getTrackPosition().getX(), t.getTrackPosition().getY()),
                    t.getLength(),
                    t.getNumber(),
                    CircuitLocationType.MARSHAL_SECTOR.toString()
                )
            )
            .findFirst()
            .orElse(null);
        
        if (marshalSector == null) throw new InvalidInstanceException();

        // Cache results with a TTL of 5 minutes.
        CacheResult cacheSetResult = null;
        try {
            cacheSetResult = cacheService.set(
                cacheKey,
                objectMapper.writeValueAsString(marshalSector),
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

        return marshalSector;
    }

    @GetMapping("/{year}/{circuit_key}/mini-sectors/{number}")
    public CircuitLocation getMiniSector(
        @PathVariable("year") Integer year,
        @PathVariable("circuit_key") Integer circuitKey,
        @PathVariable("number") Integer number
    ) {
        String cacheKey = CacheUtils.buildCacheKey(
            "mini-sectors",
            String.valueOf(year),
            String.valueOf(circuitKey),
            String.valueOf(number)
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
                return objectMapper.readValue(cacheGetResult.getValue(), new TypeReference<CircuitLocation>(){});
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
        F1MultiviewerCircuit f1MultiviewerCircuit = f1MultiviewerService.getCircuit(String.valueOf(year), String.valueOf(circuitKey));
        
        if (f1MultiviewerCircuit == null) throw new InvalidInstanceException();

        CircuitLocation miniSector = Streams
            .zip(
                IntStream.range(0, f1MultiviewerCircuit.getMiniSectorsIndexes().size()).boxed(),
                f1MultiviewerCircuit.getMiniSectorsIndexes().stream(),
                (n, i) -> new CircuitLocation(
                    0,
                    new CircuitLocationCoordinates(
                        f1MultiviewerCircuit.getX().get(i).doubleValue(),
                        f1MultiviewerCircuit.getY().get(i).doubleValue()
                    ),
                    0,
                    n + 1,
                    CircuitLocationType.MINI_SECTOR.toString()
                )
            )
            .filter(s -> s.getNumber().equals(number))
            .findFirst()
            .orElse(null);
        
        if (miniSector == null) throw new InvalidInstanceException();

        // Cache results with a TTL of 5 minutes.
        CacheResult cacheSetResult = null;
        try {
            cacheSetResult = cacheService.set(
                cacheKey,
                objectMapper.writeValueAsString(miniSector),
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

        return miniSector;
    }
}
