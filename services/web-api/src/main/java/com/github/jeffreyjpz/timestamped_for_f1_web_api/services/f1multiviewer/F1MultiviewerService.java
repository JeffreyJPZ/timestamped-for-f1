package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer;

import java.util.List;

import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.client.RestClient;

import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.f1multiviewer.dtos.F1MultiviewerCircuit;

public class F1MultiviewerService {

    private final F1MultiviewerServiceConfigurationProperties properties;

    private final RestClient client;

    public F1MultiviewerService(F1MultiviewerServiceConfigurationProperties properties, RestClient.Builder builder) {
        // Clone builder to avoid affecting other services using the same builder.
        RestClient.Builder builderCopy = builder.clone();
        
        this.properties = properties;
        this.client = builderCopy
            .baseUrl(this.properties.getBaseUrl())
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON.toString())
            .build();
    }

    public List<F1MultiviewerCircuit> getCircuits(final String circuitKey, final String year) {
        return this.client
            .get()
            .uri(uriBuilder ->
                uriBuilder.path("/circuits/{circuitKey}/{year}").build(circuitKey, year)
            )
            .retrieve()
            .body(new ParameterizedTypeReference<List<F1MultiviewerCircuit>>(){});
    }

}
