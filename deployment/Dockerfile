FROM ubuntu:16.04
MAINTAINER Athanasoulis Panagiotis
LABEL version="0.3"

ENV PUBLIC_IP=$PUBLIC_IP
ENV KAFKA_PORT=$KAFKA_PORT
ENV KAFKA_TRANSLATION_TOPIC=$KAFKA_TRANSLATION_TOPIC
ENV INFLUXDB_DB_NAME=$INFLUXDB_DB_NAME
ENV INFLUXDB_USER=$INFLUXDB_USER
ENV INFLUXDB_PWD=$INFLUXDB_PWD
ENV INFLUXDB_PORT=$INFLUXDB_PORT
ENV INFLUXDB_RETENTION_POLICY_NAME=$INFLUXDB_RETENTION_POLICY_NAME
ENV INFLUXDB_RETENTION_POLICY_DURATION=$INFLUXDB_RETENTION_POLICY_DURATION
ENV INFLUXDB_RETENTION_POLICY_REPLICATION=$INFLUXDB_RETENTION_POLICY_REPLICATION


RUN pwd
RUN apt-get update

# Install required packages
RUN apt-get -y install build-essential apt-utils acl cron libxml2-dev python3-pip vim supervisor htop wget
RUN apt-get -y install python3-dev python3-lxml python3-cffi

# Copy source code
RUN mkdir /opt/kafka-influx
COPY kafka-influx /opt/kafka-influx
RUN ls -la /opt/kafka-influx
ADD kafka-influx/deployment/kafka-influx.conf /etc/supervisor/conf.d/kafka-influx.conf

RUN pip3 install -r /opt/kafka-influx/requirements.txt

# Configure Supervisor
RUN rm -rf /etc/supervisor/supervisord.conf && \
 cp /opt/kafka-influx/deployment/supervisor/supervisord.conf /etc/supervisor/supervisord.conf

EXPOSE 3333

# Run script
#CMD ["supervisord", "-n"]
CMD bash /opt/kafka-influx/deployment/run.sh
