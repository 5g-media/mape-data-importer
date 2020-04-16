import json
import logging.config
from kafka import KafkaConsumer
from influxdb import InfluxDBClient
from utils import format_str_timestamp
from metric_formatter import format_monitoring_metric_per_source_origin
from exceptions import InvalidStrTimestamp, NotValidDatetimeTimestamp, MetricNameNotFound, MetricValueNotFound, \
    VimUuidTypeNotSupported, VimTypeNotFound, NsUuidNotFound, NsdUuidNotFound, VnfUuidNotFound, VnfdUuidNotFound, \
    VduUuidNotFound
from settings import KAFKA_SERVER, KAFKA_CLIENT_ID, KAFKA_API_VERSION, KAFKA_TRANSLATION_TOPIC, LOGGING, \
    INFLUX_DATABASES, INFLUX_RETENTION_POLICY, KAFKA_GROUP_ID

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def main():
    # See more: https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER, client_id=KAFKA_CLIENT_ID, enable_auto_commit=True,
                             api_version=KAFKA_API_VERSION, group_id=KAFKA_GROUP_ID)
    consumer.subscribe(pattern=KAFKA_TRANSLATION_TOPIC)

    # See more: http://influxdb-python.readthedocs.io/en/latest/examples.html
    influx_client = InfluxDBClient(host=INFLUX_DATABASES['default']['HOST'], port=INFLUX_DATABASES['default']['PORT'],
                                   username=INFLUX_DATABASES['default']['USERNAME'],
                                   password=INFLUX_DATABASES['default']['PASSWORD'],
                                   database=INFLUX_DATABASES['default']['NAME'], )

    # Set retention policy in db
    influx_client.create_retention_policy(name=INFLUX_RETENTION_POLICY['NAME'],
                                          duration=INFLUX_RETENTION_POLICY['DURATION'],
                                          replication=INFLUX_RETENTION_POLICY['REPLICATION'],
                                          default=True)
    for msg in consumer:
        try:
            # Get the message
            # message = msg.value
            message = json.loads(msg.value.decode('utf-8', 'ignore'))
            ns_uuid = message.get("mano", {}).get('ns', {}).get('id', None)
            if ns_uuid is None:
                continue

            original_timestamp = message.get('metric', {}).get('timestamp')
            expected_timestamp = format_str_timestamp(original_timestamp)

            # Skip non numeric values
            try:
                float(message.get('metric', {}).get('value', None))
            except (TypeError, ValueError):
                # skip the message
                logger.warning('Skip non numeric value: {}'.format(message.get('metric', {}).get('value')))
                continue

            # Prepare the record to be inserted
            monitoring_metric = format_monitoring_metric_per_source_origin(message, expected_timestamp)
            # Insert the record in the db
            influx_client.write_points(monitoring_metric)

        except (MetricNameNotFound, MetricValueNotFound, VimUuidTypeNotSupported, VimTypeNotFound, NsUuidNotFound,
                NsdUuidNotFound, VnfUuidNotFound, VnfdUuidNotFound, VduUuidNotFound) as we:
            logger.warning(we)
            continue
        except (InvalidStrTimestamp, NotValidDatetimeTimestamp) as ex:
            logger.error(ex)
            continue
        except Exception as e:
            logger.exception(e)
            continue


if __name__ == '__main__':
    main()
