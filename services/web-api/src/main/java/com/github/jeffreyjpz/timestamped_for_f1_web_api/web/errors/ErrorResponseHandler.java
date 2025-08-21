package com.github.jeffreyjpz.timestamped_for_f1_web_api.web.errors;

import java.time.Instant;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import com.github.jeffreyjpz.timestamped_for_f1_web_api.web.errors.exceptions.InvalidInstanceException;

import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;

/**
 * Logs and renders HTTP status codes for web API responses.
 */
@RestControllerAdvice
@Slf4j
public class ErrorResponseHandler {
    
    @ExceptionHandler(InvalidInstanceException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ResponseEntity<ErrorDetails> handleInvalidInstance(InvalidInstanceException e, HttpServletRequest request) {
        log.error(
            String.format("invalid instance %s", getRequestInstance(request)),
            e
        );

        ErrorDetails error = new ErrorDetails(
            "The given instance does not exist.",
            getRequestInstance(request),
            Instant.now().toString(),
            "INVALID_INSTANCE"
        );

        return new ResponseEntity<ErrorDetails>(error, HttpStatus.NOT_FOUND);
    }

    private String getRequestInstance(HttpServletRequest request) {
        String uri = request.getRequestURI();
        if (request.getQueryString() != null) {
            uri = uri + "?" + request.getQueryString();
        }

        return uri;
    }
}
