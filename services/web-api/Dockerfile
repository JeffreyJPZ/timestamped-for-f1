FROM eclipse-temurin:21-alpine

RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} timestamped-for-f1-web-api.jar

ENTRYPOINT ["java","-jar","/timestamped-for-f1-web-api.jar"]
