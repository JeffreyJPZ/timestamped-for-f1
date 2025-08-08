package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1;

import java.util.List;

import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.util.MultiValueMap;
import org.springframework.web.reactive.function.client.WebClient;

import reactor.core.publisher.Mono;

@Service
public class OpenF1Service {
    
    private final OpenF1ServiceConfigurationProperties properties;
    
    private final WebClient webClient;

    public OpenF1Service(OpenF1ServiceConfigurationProperties properties, WebClient.Builder builder) {
        this.properties = properties;

        // Clone builder to avoid affecting other services using the same builder
        WebClient.Builder builderCopy = builder.clone();
        
        // Initialize web client for OpenF1
        this.webClient = builderCopy
            .baseUrl(this.properties.getBaseUrl())
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON.toString())
            .build();
    }

    public Mono<List<OpenF1Response.Driver>> getDrivers(final MultiValueMap<String, String> queryParams) {
        return this.webClient
            .get()
            .uri(uriBuilder ->
                uriBuilder.path("/drivers").queryParams(queryParams).build()
            )
            .retrieve()
            .bodyToMono(new ParameterizedTypeReference<List<OpenF1Response.Driver>>(){});
    }

    public Mono<List<OpenF1Response.Event>> getEvents(final MultiValueMap<String, String> queryParams) {
        return this.webClient
            .get()
            .uri(uriBuilder ->
                uriBuilder.path("/events").queryParams(queryParams).build()
            )
            .retrieve()
            .bodyToMono(new ParameterizedTypeReference<List<OpenF1Response.Event>>(){});
    }

    public Mono<List<OpenF1Response.Meeting>> getMeetings(final MultiValueMap<String, String> queryParams) {
        return this.webClient
            .get()
            .uri(uriBuilder ->
                uriBuilder.path("/meetings").queryParams(queryParams).build()
            )
            .retrieve()
            .bodyToMono(new ParameterizedTypeReference<List<OpenF1Response.Meeting>>(){});
    }

    public Mono<List<OpenF1Response.Session>> getSessions(final MultiValueMap<String, String> queryParams) {
        return this.webClient
            .get()
            .uri(uriBuilder ->
                uriBuilder.path("/sessions").queryParams(queryParams).build()
            )
            .retrieve()
            .bodyToMono(new ParameterizedTypeReference<List<OpenF1Response.Session>>(){});
    }
}
