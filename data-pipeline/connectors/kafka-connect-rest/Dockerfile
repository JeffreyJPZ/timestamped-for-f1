FROM maven:3.8.6-openjdk-11-slim
RUN apt-get update && \
    apt-get install ca-certificates curl && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
WORKDIR connectors/kafka-connect-rest
COPY . .
RUN mvn clean install && \
    cd rest && \
    mkdir jars && \
    cp ../kafka-connect-rest-plugin/target/kafka-connect-rest-plugin-*-shaded.jar jars/ && \
    cp ../kafka-connect-transform-from-json/kafka-connect-transform-from-json-plugin/target/kafka-connect-transform-from-json-plugin-*-shaded.jar jars/ && \
    cp ../kafka-connect-transform-add-headers/target/kafka-connect-transform-add-headers-*-shaded.jar jars/ && \
    cp ../kafka-connect-transform-velocity-eval/target/kafka-connect-transform-velocity-eval-*-shaded.jar jars/
