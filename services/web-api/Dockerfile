# Must use non-alpine image for protoc compatibility
FROM maven:3.9-eclipse-temurin-21 AS build

COPY pom.xml /app/
COPY src /app/src/

WORKDIR /app

RUN mvn clean package -DskipTests

ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} timestamped-for-f1-web-api.jar

# Copy jar file to production image
FROM eclipse-temurin:21-alpine

RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

COPY --from=build /app/target/*.jar /app/timestamped-for-f1-web-api.jar

ENTRYPOINT ["java","-jar","/app/timestamped-for-f1-web-api.jar"]
