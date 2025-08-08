package com.github.jeffreyjpz.timestamped_for_f1_web_api.utils;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;

import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;

import com.google.common.base.Function;
import com.google.common.collect.Lists;

/**
 * Utility for converting a mapping of multi-valued query parameters to a collection of single-valued query parameters.
 */
public class OpenF1ServiceQueryParameterZipper {
    
    public static Collection<MultiValueMap<String, String>> zip(MultiValueMap<String, String> queryParams) {
        // The index of each param in queryParamNames should match the index in each corresponding entry in queryParamCombinations.
        List<String> queryParamNames = new ArrayList<String>();
        List<List<String>> allQueryParamValues = new ArrayList<List<String>>();

        for (Map.Entry<String, List<String>> queryParam : queryParams.entrySet()) {
            queryParamNames.add(new String(queryParam.getKey()));
            allQueryParamValues.add(new ArrayList<String>(queryParam.getValue()));
        };

        // Generate all query parameter combinations.
        List<List<String>> queryParamCombinations = Lists.cartesianProduct(allQueryParamValues);

        // Zip query parameter names and their corresponding value in each mapping of query parameters.
        Function<List<String>, MultiValueMap<String, String>> zipQueryParamNamesAndValues = new Function<List<String>, MultiValueMap<String, String>>() {
            @Override
            public MultiValueMap<String, String> apply(List<String> queryParamValues) {
                MultiValueMap<String, String> queryParamNamesToSingleValues = new LinkedMultiValueMap<String, String>(queryParamNames.size());

                for (int i = 0; i < queryParamValues.size(); i++) {
                    queryParamNamesToSingleValues.add(queryParamNames.get(i), queryParamValues.get(i));
                }

                return queryParamNamesToSingleValues;
            }
        };

        return queryParamCombinations.stream().map(zipQueryParamNamesAndValues).toList();
    }
}
