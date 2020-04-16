import json
import logging.config
from kafka import KafkaConsumer
from datetime import datetime
from influxdb import InfluxDBClient
from settings import KAFKA_SERVER, KAFKA_CLIENT_ID, KAFKA_API_VERSION, KAFKA_VTRANSCODER_SPECTATORS_TOPIC, LOGGING, \
    INFLUX_DATABASES, INFLUX_RETENTION_POLICY, KAFKA_VTRANSCODER_SPECTATORS_GROUP_ID

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def init_kafka_consumer():
    # See more: https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER, client_id=KAFKA_CLIENT_ID, enable_auto_commit=True,
                             api_version=KAFKA_API_VERSION, group_id=KAFKA_VTRANSCODER_SPECTATORS_GROUP_ID)
    return consumer


def init_influx_client():
    # See more: http://influxdb-python.readthedocs.io/en/latest/examples.html
    influx_client = InfluxDBClient(host=INFLUX_DATABASES['default']['HOST'], port=INFLUX_DATABASES['default']['PORT'],
                                   username=INFLUX_DATABASES['default']['USERNAME'],
                                   password=INFLUX_DATABASES['default']['PASSWORD'],
                                   database=INFLUX_DATABASES['default']['NAME'], )
    return influx_client


def get_metric_name(name, mtype):
    """ Rename the metric if needed

    Args:
        name (str): The name of the metric
        mtype (str): The type of the metric

    Returns:
        str: the name of the metric
    """
    if name == "bitrate":
        return "bitrate_on" if mtype == "on" else "bitrate_aggr"
    elif name == "framerate":
        return "framerate_on" if mtype == "on" else "framerate_aggr"
    elif name == "latency":
        return "latency_on" if mtype == "on" else "latency_aggr"
    else:
        return name


def main():
    consumer = init_kafka_consumer()
    consumer.subscribe(pattern=KAFKA_VTRANSCODER_SPECTATORS_TOPIC)

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
            streams = message['incoming_streams']
            tm = "{}".format(message['timestamp']).split('.')
            dt = datetime.utcfromtimestamp(float(tm[0]))
            timestamp = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

            client_id = message.get('client_id', None)
            group_id = message.get('group_id', None)

            if client_id is None or group_id is None:
                continue

            group_id = group_id.replace(' ', '_')

            for i in streams:
                quality = i['quality_id']
                transcoder_id = i['transcoder_id']
                try:
                    if len(transcoder_id) < 2:
                        continue
                except:
                    continue

                metrics = i['metrics']
                metrics.append({"name": "quality", "state": "na", "value": quality, "unit": "number"})
                for metric in metrics:
                    # Skip broker metric names
                    if len(metric['name']) == 0 or metric['name'] == " ":
                        continue

                    metric_name = get_metric_name(metric['name'].lower(), metric['state'])
                    # Filter the value of each metric
                    try:
                        float(metric['value'])
                    except:
                        continue

                    temp = {
                        "measurement": "vtranscoder_spectators_measurements",
                        "time": timestamp,
                        "tags": {
                            "group_id": group_id,
                            "client_id": client_id,
                            "transcoder_id": transcoder_id,
                            "metric": metric_name,
                        },
                        "fields": {
                            "value": float(metric['value']),
                            "unit": "{}".format(metric['unit'])
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
