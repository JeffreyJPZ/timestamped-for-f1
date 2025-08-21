package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.StringJoiner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClient;

import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos.OpenF1Driver;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos.OpenF1Event;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos.OpenF1Meeting;
import com.github.jeffreyjpz.timestamped_for_f1_web_api.services.openf1.dtos.OpenF1Session;

@Service
public class OpenF1Service {

    private final Map<String, String> operatorMap = Map.ofEntries(
        Map.entry("~eq~", "="),
        Map.entry("~gt~", ">"),
        Map.entry("~gte~", ">="),
        Map.entry("~lt~", "<"),
        Map.entry("~lte~", "<=")
    );
    private final Pattern operatorPattern = Pattern.compile("~\\w+~");
    
    private final OpenF1ServiceConfigurationProperties properties;

    private final RestClient client;

    public OpenF1Service(OpenF1ServiceConfigurationProperties properties, RestClient.Builder builder) {
        // Clone builder to avoid affecting other services using the same builder.
        RestClient.Builder builderCopy = builder.clone();
        
        this.properties = properties;
        this.client = builderCopy
            .baseUrl(this.properties.getBaseUrl())
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON.toString())
            .build();
    }

    public List<OpenF1Driver> getDrivers(MultiValueMap<String, String> queryParams) {
        return getResults(
            new ParameterizedTypeReference<List<OpenF1Driver>>() {},
            "drivers",
            queryParams
        );
    }

    public List<OpenF1Event> getEvents(MultiValueMap<String, String> queryParams) {
        return getResults(
            new ParameterizedTypeReference<List<OpenF1Event>>() {},
            "events",
            queryParams
        );
    }

    public List<OpenF1Meeting> getMeetings(MultiValueMap<String, String> queryParams) {
        return getResults(
            new ParameterizedTypeReference<List<OpenF1Meeting>>() {},
            "meetings",
            queryParams
        );
    }

    public List<OpenF1Session> getSessions(MultiValueMap<String, String> queryParams) {
        return getResults(
            new ParameterizedTypeReference<List<OpenF1Session>>() {},
            "sessions",
            queryParams
        );
    }

    private <T> T getResults(ParameterizedTypeReference<T> type, String endpoint, MultiValueMap<String, String> queryParams) {
        return this.client
            .get()
            .uri((uriBuilder) ->
                // Builds a URI in the form "/{endpoint}?{queryString}".
                uriBuilder.pathSegment(endpoint).replaceQuery(buildQueryString(queryParams)).build()
            )
            .retrieve()
            .body(type);
    }

    private String buildQueryString(MultiValueMap<String, String> queryParams) {
        // Attempt to extract an operator "~eq~, ~gt~, ~gte~, ~lt~, ~lte~" and map it to the appropriate
        // OpenF1 operator "=, >, >=, <, <=" respectively. If no operator is found, "=" is used.
        List<String> stringParams = new ArrayList<String>();

        queryParams.forEach((key, values) -> {
            values.forEach((value) -> {
                Matcher matcher = operatorPattern.matcher(value);
                String operator;

                if (matcher.find()) {
                    operator = operatorMap.get(matcher.group());
                } else {
                    operator = operatorMap.get("~eq~");
                }

                // Build the query string in the form {key}{operator}{value} for each entry.
                stringParams.add(String.format("%s%s%s", key, operator, value));
            });
        });
 
        return String.join("&", stringParams);
    }
}
