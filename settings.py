import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

# =================================
# KAFKA SETTINGS
# =================================
KAFKA_SERVER = "{}:{}".format(os.environ.get("PUBLIC_IP", "192.168.1.175"),
                              os.environ.get("KAFKA_PORT", "9092"))
KAFKA_CLIENT_ID = 'influxdb'
KAFKA_API_VERSION = (1, 1, 0)
KAFKA_TRANSLATION_TOPIC = os.environ.get("KAFKA_TRANSLATION_TOPIC", "ns.instances.trans")
KAFKA_VCE_TOPIC = "app.vce.metrics"  
KAFKA_PLEX_SERVER_TOPIC = "app.originserver.metrics"
KAFKA_VTRANSCODER_SPECTATORS_TOPIC = "spectators.vtranscoder3d.metrics"
KAFKA_TRAFFIC_MANAGER_TOPIC = "trafficmanager.uc2.metrics"
KAFKA_UC2_QOE_TOPIC = "app.uc2.qoe" 
KAFKA_UC1_QOE_TOPIC = "app.vtranscoder3d_spectators.qoe" 

KAFKA_GROUP_ID = "STORE_MON_VALUES"
KAFKA_VCE_GROUP_ID = "STORE_VCE_METRICS_CG"
KAFKA_PLEX_SERVER_GROUP_ID = "STORE_PLEX_SERVER_METRICS_CG"
KAFKA_VTRANSCODER_SPECTATORS_GROUP_ID = "STORE_VTRANSCODER_SPECTATORS_METRICS_CG"
KAFKA_TRAFFIC_MANAGER_GROUP_ID = "STORE_TRAFFIC_MANAGER_METRICS_CG"
KAFKA_UC2_QOE_GROUP_ID = "STORE_UC2_QOE_METRICS_CG"
KAFKA_UC1_QOE_GROUP_ID = "STORE_UC1_QOE_METRICS_CG"

# =================================
# INFLUXDB SETTINGS
# =================================
# See InfluxDBClient class
INFLUX_DATABASES = {
    'default': {
        'ENGINE': 'influxdb',
        'NAME': os.environ.get("INFLUXDB_DB_NAME", 'monitoring'),
        'USERNAME': os.environ.get("INFLUXDB_USER", 'root'),
        'PASSWORD': os.environ.get("INFLUXDB_PWD", 'password'),
        'HOST': os.environ.get("PUBLIC_IP", "192.168.1.175"),
        'PORT': os.environ.get("INFLUXDB_PORT", 8086)
    }
}

INFLUX_RETENTION_POLICY = {
    "NAME": os.environ.get("INFLUXDB_RETENTION_POLICY_NAME", 'two_weeks_policy'),
    "DURATION": os.environ.get("INFLUXDB_RETENTION_POLICY_DURATION", '2w'),
    "REPLICATION": os.environ.get("INFLUXDB_RETENTION_POLICY_REPLICATION", '1')
}

# ==================================
# LOGGING SETTINGS
# ==================================
# See more: https://docs.python.org/3.5/library/logging.config.html
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': "[%(asctime)s] - [%(name)s:%(lineno)s] - [%(levelname)s] %(message)s",
        },
        'simple': {
            'class': 'logging.Formatter',
            'format': '%(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
        },
        'daemon': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "{}/logs/access.log".format(PROJECT_ROOT),
            'mode': 'w',
            'formatter': 'detailed',
            'level': 'DEBUG',
            'maxBytes': 2024 * 2024,
            'backupCount': 5,
        },
    },
    'loggers': {
        'daemon': {
            'handlers': ['daemon']
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'daemon']
    },
}
