# MAPE data-importer component

This component is part of the 5G-MEDIA MAPE service. Take a look in the [mape](https://github.com/5g-media/mape) repository.

## Introduction

The `data-importer` component:
- consumes the monitoring data in the publish/subscribe (Apache Kafka) broker,
- adjusts the format of the monitoring data in the one that InfluxDB supports,
- inserts the monitoring data in a dedicated database in the InfluxDB.

This service operates as a mediator between the publish/subscribe (Apache Kafka) broker and the database (InfluxDB).


## Requirements
- Python 3.5+ 
  + a set of python packages are used (see `requirements.txt`).
- The Apache Kafka broker must be running and accessible from the component
- The InfluxDB must be running and accessible (mainly the API) from the component

## Configuration

A set of environmental variables are used in the docker image:
 - *PUBLIC_IP*: defines the IPv4 of the kafka bus. The default IP is `192.168.1.107`.
 - *KAFKA_PORT*: defines the port of the kafka bus. The default port is `9092`.
 - *INFLUXDB_DB_NAME*: defines the name of the InfluxDB. The default topic name is `monitoring`.
 - *INFLUXDB_USER*: defines the user of the InfluxDB. The default value is `root`.
 - *INFLUXDB_PWD*: defines the user's password in InfluxDB. The default port is `password`.
 - *INFLUXDB_PORT*: defines the port in which the InfluxDB listens to. The default value is `8086`.
 - *INFLUXDB_RETENTION_POLICY_NAME*: defines the name of the retention policy in InfluxDB.
 - *INFLUXDB_RETENTION_POLICY_DURATION*: defines the duration of the retention policy in InfluxDB.
 - *INFLUXDB_RETENTION_POLICY_REPLICATION*: defines the replication factor of the retention policy in InfluxDB.


## Installation/Deployment

To build the docker image, copy the bash script included in the `bash_scripts/` folder in the parent folder of the project and then, run:
```bash
   chmod +x build_docker_image.sh
   ./build_docker_image.sh
```

Given the docker image availability, there are 2 ways to deploy it:
 - using the MAPE docker-compose project
 - manual deployment as standalone container

For manual deployment in a linux VM, download the code from the repo in the user home (e.g. `/home/ubuntu`) and follow the below steps:
```bash
# Set the values of the environmental variables
$ sudo docker run -p 3336:3333 --name kafka_influx --restart always \
    -e PUBLIC_IP="kafka_ivp4" \
    -e KAFKA_PORT="9092" \
    -e INFLUXDB_DB_NAME="monitoring" \
    -e INFLUXDB_USER="root" \
    -e INFLUXDB_PWD="password" \
    -e INFLUXDB_PORT="8086" \
    -e INFLUXDB_RETENTION_POLICY_NAME="one_week" \
    -e INFLUXDB_RETENTION_POLICY_DURATION="1w" \
    -e INFLUXDB_RETENTION_POLICY_REPLICATION="1" \
    -dit kafka-influx
```

## Usage

Access the docker container:
```bash
$ sudo docker exec -it kafka_influx bash
```

Start the translator service through the supervisor:
```bash
$ service supervisor start && supervisorctl start kafka-influx
```

Stop the service through the supervisor:
```bash
$ supervisorctl stop kafka-influx
```

Stop the supervisor service:
```bash
$ service supervisor stop 
```


## Authors
- Singular Logic <pathanasoulis@ep.singularlogic.eu>
- 

## Contributors
 - Contact with Authors
 

## Acknowledgements
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement *No 761699*. The dissemination of results herein reflects only the author’s view and the European Commission is not responsible for any use that may be made 
of the information it contains.


## License
[Apache 2.0](LICENSE.md)