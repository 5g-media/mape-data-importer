from exceptions import MetricNameNotFound, MetricValueNotFound, VimUuidTypeNotSupported, VimTypeNotFound, \
    NsUuidNotFound, NsdUuidNotFound, VnfUuidNotFound, VnfdUuidNotFound, VduUuidNotFound


def format_monitoring_metric_per_metric_type(input, proper_timestamp):
    """Convert the Monitoring metric as provided from Translator component in format suitable for the InfluxDB.

    The metric name is used for the InfluxDB measurement name, e.g.: cpu, memory
    while its value, type and unit are defined as values.

    The source origin (see `tag`) is defined as tag for search.

    See the format of the monitoring metric coming from the Translator component: samples/input.json

    Args:
        input (dict): The metric as it was set by the translator component
        proper_timestamp (str): The timestamp of the metric as provided from NVFI or app

    Returns:
        list: The monitoring metric in a format that the InfluxDB requires so as to be inserted.
    """
    vim = input.get('mano', {}).get('vim', {})
    ns = input.get('mano', {}).get('ns', {})
    vnf = input.get('mano', {}).get('vnf', {})
    vdu = input.get('mano', {}).get('vdu', {})
    metric = input.get('metric', {})

    monitoring_metric = [
        {
            "measurement": metric.get('name'),
            "tags": {
                "vim_uuid": vim.get('uuid'),
                "vim_type": vim.get('type'),
                "vim_name": vim.get('name'),
                "vim_host": vim.get('url', "http://localhost"),
                "origin": vim.get('tag', ""),
                "ns_uuid": ns.get('id', None),
                "ns_name": ns.get('nsd_name', None),
                "nsd_id": ns.get('nsd_id', None),
                "nsd_name": ns.get('nsd_name', None),
                "vnf_uuid": vnf.get('id', None),
                "vnf_name": vnf.get('name', None),
                "vnf_short_name": vnf.get('short_name', None),
                "vnfd_id": vnf.get('vnfd_id', None),
                "vnfd_name": vnf.get('vnfd_name', None),
                "vdu_uuid": vdu.get('id', None),
                "vdu_image_uuid": vdu.get('image_id', None),
                "vdu_flavor_vcpus": vdu.get('flavor', {}).get('vcpus', None),
                "vdu_flavor_ram": vdu.get('flavor', {}).get('ram', None),
                "vdu_flavor_disk": vdu.get('flavor', {}).get('disk', None),
                "vdu_state": vdu.get('status', None),  # new
                "ip_address": vdu.get('ip_address', None),  # new
                # "mgmt-interface": vdu.get('mgmt-interface', None),  # new
            },
            "time": proper_timestamp,
            "fields": {
                "value": metric.get('value', None),
                "unit": metric.get('unit', None),
                "type": metric.get('type', None)
            }
        }
    ]
    return monitoring_metric


def format_monitoring_metric_per_source_origin(input, timestamp):
    """Convert the Monitoring metric as provided from Translator component in format suitable for the InfluxDB.

    The source origin (see `tag`) is used for the measurement name, e.g.: openstack, kubernetes, ...
    The metric is defined as tag while its value, type and unit are defined as values.

    See the format of the monitoring metric coming from the Translator component: samples/input.json

    Args:
        input (dict): The metric as it was set by the translator component
        timestamp (str): The timestamp of the metric as provided from NVFI or app

    Returns:
        list: The monitoring metric in a format that the InfluxDB requires so as to be inserted.
    """
    vim = input.get('mano', {}).get('vim', {})
    ns = input.get('mano', {}).get('ns', {})
    vnf = input.get('mano', {}).get('vnf', {})
    vdu = input.get('mano', {}).get('vdu', {})
    metric = input.get('metric', {})

    # Validate the value of the metric
    if metric.get('value', None) is None:
        raise MetricValueNotFound("Invalid metric value in record: {}".format(input))

    # Filter the value of each tag
    if metric.get('name', None) is None:
        raise MetricNameNotFound("Invalid metric name in record: {}".format(input))
    if not isinstance(vim.get('uuid'), str):
        raise VimUuidTypeNotSupported("Invalid VIM uuid in record: {}".format(input))
    if vim.get('type') is None:
        raise VimTypeNotFound("Invalid VIM type in record: {}".format(input))
    if ns.get('id', None) is None:
        raise NsUuidNotFound("Invalid NS uuid in record: {}".format(input))
    if ns.get('nsd_id', None) is None:
        raise NsdUuidNotFound("Invalid NSd uuid in record: {}".format(input))
    if vnf.get('id', None) is None:
        raise VnfUuidNotFound("Invalid VNF uuid in record: {}".format(input))
    if vnf.get('vnfd_id', None) is None:
        raise VnfdUuidNotFound("Invalid VNFd uuid in record: {}".format(input))
    if vdu.get('id', None) is None:
        raise VduUuidNotFound("Invalid VDU uuid in record: {}".format(input))

    monitoring_metric = [
        {
            "measurement": vim.get('name'),
            "time": timestamp,
            "tags": {
                "metric_name": metric['name'],
                "vim_uuid": vim['uuid'],
                "vim_type": vim['type'],
                "ns_uuid": ns['id'],
                "nsd_id": ns['nsd_id'],
                "vnf_uuid": vnf['id'],
                "vnfd_id": vnf['vnfd_id'],
                "vdu_uuid": vdu['id'],
            },
            "fields": {
                "value": float(metric['value']),
                "metric_unit": metric.get('unit', ""),
                "metric_type": metric.get('type', ""),
                "source_origin": vim.get('tag', ""),
                "vim_host": vim.get('url', "http://localhost"),
                "ns_name": ns.get('nsd_name', ""),
                "nsd_name": ns.get('nsd_name', ""),
                "vnfd_name": vnf.get('vnfd_name', ""),
                "vdu_image_uuid": vdu.get('image_id', "unknown"),
                # "vnf_name": vnf.get('name', ""),
                # "vnf_short_name": vnf.get('short_name', ""),
                # "vdu_flavor_vcpus": vdu.get('flavor', {}).get('vcpus', None),
                # "vdu_flavor_ram": vdu.get('flavor', {}).get('ram', None),
                # "vdu_flavor_disk": vdu.get('flavor', {}).get('disk', None),
                # "vdu_state": vdu.get('status', ""),
                "ip_address": vdu.get('ip_address', "127.0.0.1")
                # "mgmt-interface": vdu.get('mgmt-interface', None)
            }
        }
    ]
    return monitoring_metric
