import json
import logging.config
from kafka import KafkaConsumer
from datetime import datetime
from influxdb import InfluxDBClient
from utils import format_str_timestamp
from metric_formatter import format_monitoring_metric_per_source_origin
from exceptions import InvalidStrTimestamp, NotValidDatetimeTimestamp, MetricNameNotFound, \
    MetricValueNotFound, \
    VimUuidTypeNotSupported, VimTypeNotFound, NsUuidNotFound, NsdUuidNotFound, VnfUuidNotFound, \
    VnfdUuidNotFound, \
    VduUuidNotFound
from settings import KAFKA_SERVER, KAFKA_CLIENT_ID, KAFKA_API_VERSION, KAFKA_VCE_TOPIC, LOGGING, \
    INFLUX_DATABASES, INFLUX_RETENTION_POLICY, KAFKA_VCE_GROUP_ID

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def init_kafka_consumer():
    # See more: https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER, client_id=KAFKA_CLIENT_ID,
                             enable_auto_commit=True,
                             api_version=KAFKA_API_VERSION, group_id=KAFKA_VCE_GROUP_ID)
    return consumer


def init_influx_client():
    # See more: http://influxdb-python.readthedocs.io/en/latest/examples.html
    influx_client = InfluxDBClient(host=INFLUX_DATABASES['default']['HOST'],
                                   port=INFLUX_DATABASES['default']['PORT'],
                                   username=INFLUX_DATABASES['default']['USERNAME'],
                                   password=INFLUX_DATABASES['default']['PASSWORD'],
                                   database=INFLUX_DATABASES['default']['NAME'], )
    return influx_client


def main():
    consumer = init_kafka_consumer()
    consumer.subscribe(pattern=KAFKA_VCE_TOPIC)

    influx_client = init_influx_client()
    # Set retention policy in db
    influx_client.create_retention_policy(name=INFLUX_RETENTION_POLICY['NAME'],
                                          duration=INFLUX_RETENTION_POLICY['DURATION'],
                                          replication=INFLUX_RETENTION_POLICY['REPLICATION'],
                                          default=True)

    # metric_x stands for the min bitrate of the selected Profile while the metric_y for the
    # max bitrate of the seclected Profile
    allowed_metrics = ['enc_speed', 'enc_dbl_time', 'gop_size', 'max_bitrate', 'num_frame',
                       'num_fps', 'enc_quality', 'act_bitrate', 'avg_bitrate', 'metric_x',
                       'metric_y', 'metric_z']

    for msg in consumer:
        try:
            monitoring_metrics = list()

            # Get & decode the message
            message = json.loads(msg.value.decode('utf-8', 'ignore'))
            # Format the given timestamp properly
            unix_time = message['utc_time']
            unix_ts = str(unix_time)[:10]
            dt = datetime.utcfromtimestamp(float(unix_ts))
            timestamp = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

            for metric in message:
                if metric not in allowed_metrics:
                    continue
                try:
                    float(message[metric])
                except:
                    continue

                vdu_mac = message.get('id', None)
                if vdu_mac is None:
                    continue
                vdu_name = get_instance(vdu_mac)
                if vdu_name is None:
                    continue

                temp = {
                    "measurement": "vce_vnf_measurements",
                    "time": timestamp,
                    "tags": {
                        "metric": metric,
                        "vdu_mac": vdu_mac,
                    },
                    "fields": {
                        "value": float(message[metric]),
                        "vdu_name": vdu_name
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


def get_instance(index):
    instances = {
        '06:00:cc:74:72:95': 'vCE-1',
        '06:00:cc:74:72:99': 'vCE-2'
    }
    if index in instances.keys():
        return instances[index]
    return None


if __name__ == '__main__':
    main()
