FROM confluentinc/cp-kafka-connect:latest

RUN confluent-hub install --no-prompt --verbose mongodb/kafka-connect-mongodb:latest

# Copy OpenF1 source connectors and config
COPY ./data-pipeline/connectors/openf1/config /connectors/openf1/config
COPY ./data-pipeline/connectors/openf1/config.properties /connectors/openf1