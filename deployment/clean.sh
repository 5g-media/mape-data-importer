#!/bin/bash

if sudo docker ps | grep -q 'kafka_influx'; then
    sudo docker exec -i kafka_influx service supervisor stop && \
    sudo docker stop kafka_influx && \
    sudo docker rm -f kafka_influx
fi