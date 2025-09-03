FROM rabbitmq:4.1-management-alpine

# Enable custom management config
ENV RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS="-rabbitmq_management load_definitions \"/etc/rabbitmq/definitions.json\""

# Install MQTT plugin
RUN rabbitmq-plugins enable --offline rabbitmq_mqtt