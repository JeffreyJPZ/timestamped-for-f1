package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.cache;

import java.util.concurrent.CancellationException;
import java.util.concurrent.ExecutionException;

import org.springframework.stereotype.Service;

import com.github.jeffreyjpz.timestamped_for_f1_cache.cache_api_grpc_v1.CacheGrpc;
import com.github.jeffreyjpz.timestamped_for_f1_cache.cache_api_grpc_v1.CacheItem;
import com.github.jeffreyjpz.timestamped_for_f1_cache.cache_api_grpc_v1.CacheKey;
import com.github.jeffreyjpz.timestamped_for_f1_cache.cache_api_grpc_v1.CacheResult;

import lombok.RequiredArgsConstructor;
import net.devh.boot.grpc.client.inject.GrpcClient;

@Service
@RequiredArgsConstructor
public class CacheService {

    @GrpcClient("cache-api")
    private final CacheGrpc.CacheFutureStub cacheStub;

    public CacheResult get(String key) throws CacheServiceException {
        CacheKey cacheKey = CacheKey
            .newBuilder()
            .setKey(key)
            .build();
        CacheResult cacheResult;

        try {
            cacheResult = cacheStub.get(cacheKey).get();
        } catch (InterruptedException | ExecutionException | CancellationException e) {
            throw new CacheServiceException(e);
        }
        
        return cacheResult;
    }

    public CacheResult set(String key, String value, double expirationTime) throws CacheServiceException {
        CacheItem cacheItem = CacheItem
            .newBuilder()
            .setKey(key)
            .setValue(value)
            .setExpirationTime(expirationTime)
            .build();
        CacheResult cacheResult;

        try {
            cacheResult = cacheStub.set(cacheItem).get();
        } catch (InterruptedException | ExecutionException | CancellationException e) {
            throw new CacheServiceException(e);
        }
        
        return cacheResult;
    }
}
