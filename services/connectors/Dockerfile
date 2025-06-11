FROM confluentinc/cp-kafka-connect:latest

RUN confluent-hub install --no-prompt --verbose mongodb/kafka-connect-mongodb:latest

# Copy OpenF1 source connectors and config
COPY ./openf1/config /openf1/config
COPY ./openf1/config.properties /openf1