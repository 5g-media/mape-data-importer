from datetime import datetime
from exceptions import *


def convert_str_to_datetime_timestamp(timestamp_str):
    """Convert a timestamp from str type to datetime object.

    Args:
        timestamp_str (str): The timestamp of the monitoring metric

    Returns:
        Object: The timestamp as datetime object
    """
    formatter = '%Y-%m-%dT%H:%M:%S.%f'
    if not isinstance(timestamp_str, str):
        raise InvalidStrTimestamp("The type of the timestamp `{}` is not str".format(timestamp_str))

    return datetime.strptime(timestamp_str, formatter)


def convert_utc_timestamp_to_unixtime_ms(timestamp_obj):
    """Convert a timestamp from datetime object to unix-time.

    Args:
        timestamp_obj (Object): The timestamp as datetime object

    Returns:
         int: The timestamp as unix-time (in microseconds)
    """
    if not isinstance(timestamp_obj, datetime):
        raise NotValidDatetimeTimestamp("The type of the timestamp `{}` is not datetime object".format(timestamp_obj))

    unixtime_ms = timestamp_obj.timestamp() * pow(10, 6)
    return unixtime_ms


def format_str_timestamp(timestamp_str):
    """Format a str timestamp adding teh char `Z` in the end of it, if needed

    For instance: the '2014-12-10T12:00:00.123123' is converted to '2014-12-10T12:00:00.123123Z'.

    Args:
        timestamp_str (str): The timestamp of the monitoring metric

    Returns:
        str: The timestamp as datetime object
    """
    if not timestamp_str.endswith('Z'):
        return "{}Z".format(timestamp_str)
    return timestamp_str
