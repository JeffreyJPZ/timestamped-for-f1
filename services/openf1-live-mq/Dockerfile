FROM rabbitmq:4.1.2-management

# Install MQTT plugin
RUN rabbitmq-plugins enable --offline rabbitmq_mqtt

# Code credit to https://stackoverflow.com/a/62026712
# Create admin and guest user using management plugin
COPY --chown=rabbitmq ./config/definitions.json /etc/rabbitmq/definitions.json
ENV RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS="-rabbitmq_management load_definitions \"/etc/rabbitmq/definitions.json\""