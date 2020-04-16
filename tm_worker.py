import json
import logging.config
from kafka import KafkaConsumer
from datetime import datetime
from influxdb import InfluxDBClient
from settings import KAFKA_SERVER, KAFKA_CLIENT_ID, KAFKA_API_VERSION, KAFKA_TRAFFIC_MANAGER_TOPIC, LOGGING, \
    INFLUX_DATABASES, INFLUX_RETENTION_POLICY, KAFKA_TRAFFIC_MANAGER_GROUP_ID

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def init_kafka_consumer():
    # See more: https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER, client_id=KAFKA_CLIENT_ID, enable_auto_commit=True,
                             api_version=KAFKA_API_VERSION, group_id=KAFKA_TRAFFIC_MANAGER_GROUP_ID)
    return consumer


def init_influx_client():
    # See more: http://influxdb-python.readthedocs.io/en/latest/examples.html
    influx_client = InfluxDBClient(host=INFLUX_DATABASES['default']['HOST'], port=INFLUX_DATABASES['default']['PORT'],
                                   username=INFLUX_DATABASES['default']['USERNAME'],
                                   password=INFLUX_DATABASES['default']['PASSWORD'],
                                   database=INFLUX_DATABASES['default']['NAME'], )
    return influx_client


def main():
    consumer = init_kafka_consumer()
    consumer.subscribe(pattern=KAFKA_TRAFFIC_MANAGER_TOPIC)

    influx_client = init_influx_client()
    # Set retention policy in db
    influx_client.create_retention_policy(name=INFLUX_RETENTION_POLICY['NAME'],
                                          duration=INFLUX_RETENTION_POLICY['DURATION'],
                                          replication=INFLUX_RETENTION_POLICY['REPLICATION'],
                                          default=True)

    for msg in consumer:
        try:
            monitoring_metrics = list()
            # Get & decode the message
            message = json.loads(msg.value.decode('utf-8', 'ignore'))
            metric = message['type']
            value = message['value']
            unit = message['unit']
            timestamp = message['timestamp']

            try:
                float(value)
            except:
                continue

            temp = {
                "measurement": "traffic_manager_measurements",
                "time": timestamp,
                "tags": {
                    "metric": metric,
                },
                "fields": {
                    "value": float(value),
                    "unit": "{}".format(unit)
                }
            }
            monitoring_metrics.append(temp)

            # Insert the record in the db
            influx_client.write_points(monitoring_metrics)

        except json.decoder.JSONDecodeError as je:
            logger.warning("JSONDecodeError: {}".format(je))
        except Exception as e:
            logger.exception(e)
            continue


if __name__ == '__main__':
    main()
