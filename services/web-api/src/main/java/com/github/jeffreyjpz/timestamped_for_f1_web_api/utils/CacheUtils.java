package com.github.jeffreyjpz.timestamped_for_f1_web_api.utils;

/**
 * Utilities for the cache service.
 */
public class CacheUtils {

    // Returns a single string where each value is separated by ":".
    public static String buildCacheKey(String... values) {
        return String.join(":", values);
    }
}
