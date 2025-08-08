package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer;

import java.util.List;

import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.client.WebClient;

import reactor.core.publisher.Mono;

public class F1MultiviewerService {

    private final F1MultiviewerServiceConfigurationProperties properties;

    private final WebClient webClient;

    public F1MultiviewerService(F1MultiviewerServiceConfigurationProperties properties, WebClient.Builder builder) {
        this.properties = properties;

        // Clone builder to avoid affecting other services using the same builder
        WebClient.Builder builderCopy = builder.clone();
        
        // Initialize web client for OpenF1
        this.webClient = builderCopy
            .baseUrl(this.properties.getBaseUrl())
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON.toString())
            .build();
    }

    public Mono<List<F1MultiviewerResponse.Circuit>> getCircuits(final String circuitKey, final String year) {
        return this.webClient
            .get()
            .uri(uriBuilder ->
                uriBuilder.path("/circuits/{circuitKey}/{year}").build(circuitKey, year)
            )
            .retrieve()
            .bodyToMono(new ParameterizedTypeReference<List<F1MultiviewerResponse.Circuit>>(){});
    }

}
