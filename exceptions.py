class InvalidStrTimestamp(Exception):
    """Raised when the type of the timestamp is not str"""
    pass


class NotValidDatetimeTimestamp(Exception):
    """Raised when the type of the timestamp is not datetime.datetime"""
    pass


class MetricNameNotFound(Exception):
    """Raised when the name of the metric is not provided"""
    pass


class MetricValueNotFound(Exception):
    """Raised when the value of the metric is not provided"""
    pass


class VimUuidTypeNotSupported(Exception):
    """Raised when the type of the Vim UUID is not supported"""
    pass


class VimTypeNotFound(Exception):
    """Raised when the type of the Vim UUID is not provided"""
    pass


class NsUuidNotFound(Exception):
    """Raised when the type of the NS UUID is not provided"""
    pass


class NsdUuidNotFound(Exception):
    """Raised when the type of the NSd UUID is not provided"""
    pass


class VnfUuidNotFound(Exception):
    """Raised when the type of the VNF UUID is not provided"""
    pass


class VnfdUuidNotFound(Exception):
    """Raised when the type of the VNFd UUID is not provided"""
    pass


class VduUuidNotFound(Exception):
    """Raised when the type of the VDU UUID is not provided"""
    pass
