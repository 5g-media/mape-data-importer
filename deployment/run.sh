#!/bin/bash

# set the variables in the supervisor environment
sed -i "s/ENV_PUBLIC_IP/$PUBLIC_IP/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_KAFKA_PORT/$KAFKA_PORT/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_KAFKA_TRANSLATION_TOPIC/$KAFKA_TRANSLATION_TOPIC/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_INFLUXDB_DB_NAME/$INFLUXDB_DB_NAME/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_INFLUXDB_USER/$INFLUXDB_USER/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_INFLUXDB_PWD/$INFLUXDB_PWD/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_INFLUXDB_PORT/$INFLUXDB_PORT/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_INFLUXDB_RETENTION_POLICY_NAME/$INFLUXDB_RETENTION_POLICY_NAME/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_INFLUXDB_RETENTION_POLICY_DURATION/$INFLUXDB_RETENTION_POLICY_DURATION/g" /etc/supervisor/supervisord.conf
sed -i "s/ENV_INFLUXDB_RETENTION_POLICY_REPLICATION/$INFLUXDB_RETENTION_POLICY_REPLICATION/g" /etc/supervisor/supervisord.conf

# Restart services
service supervisor start && service supervisor status

# Makes services start on system start
update-rc.d supervisor defaults

echo "Initialization completed."
tail -f /dev/null  # Necessary in order for the container to not stop
