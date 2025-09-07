package com.github.jeffreyjpz.timestamped_for_f1_web_api.services.cache;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.github.jeffreyjpz.timestamped_for_f1_cache.cache_api_grpc_v1.CacheGrpc;

import net.devh.boot.grpc.client.inject.GrpcClient;
import net.devh.boot.grpc.client.inject.GrpcClientBean;

@Configuration
@GrpcClientBean(
    clazz = CacheGrpc.CacheFutureStub.class,
    beanName = "cacheStub",
    client = @GrpcClient("cache-api")
)
public class CacheServiceConfiguration {

    @Bean
    CacheService cacheService(@Autowired CacheGrpc.CacheFutureStub cacheStub) {
        return new CacheService(cacheStub);
    }
}
