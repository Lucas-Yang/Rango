import logging
import json
import re
import datetime
import traceback
import socket
import time

from inspect import istraceback

# Support order in python 2.7 and 3
try:
    from collections import OrderedDict
except ImportError:
    pass

# skip natural LogRecord attributes
# http://docs.python.org/library/logging.html#logrecord-attributes
RESERVED_ATTRS = (
    'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
    'funcName', 'levelname', 'levelno', 'lineno', 'module',
    'msecs', 'message', 'msg', 'name', 'pathname', 'process',
    'processName', 'relativeCreated', 'stack_info', 'thread', 'threadName',
    'level', 'log')

RESERVED_ATTR_HASH = dict(zip(RESERVED_ATTRS, RESERVED_ATTRS))


def merge_record_extra(record, target, reserved=RESERVED_ATTR_HASH):
    """
    Merges extra attributes from LogRecord object into target dictionary

    :param record: logging.LogRecord
    :param target: dict to update
    :param reserved: dict or list with reserved keys to skip
    """
    for key, value in record.items():
        # this allows to have numeric keys
        if (key not in reserved and not (hasattr(key, "startswith") and key.startswith('_'))):
            target[key] = value
    return target


class JsonFormatter(logging.Formatter):
    """
    A custom formatter to format logging records as json strings.
    extra values will be formatted as str() if nor supported by
    json default encoder
    """

    def __init__(self, *args, **kwargs):
        """
        :param json_default: a function for encoding non-standard objects
            as outlined in http://docs.python.org/2/library/json.html
        :param json_encoder: optional custom encoder
        :param json_serializer: a :meth:`json.dumps`-compatible callable
            that will be used to serialize the log record.
        :param prefix: an optional string prefix added at the beginning of
            the formatted string
        """
        self.json_default = kwargs.pop("json_default", None)
        self.json_encoder = kwargs.pop("json_encoder", None)
        self.json_serializer = kwargs.pop("json_serializer", json.dumps)
        self.json_indent = kwargs.pop("json_indent", None)
        self.additional_fields = kwargs.pop("additional_fields", None)
        self.prefix = kwargs.pop("prefix", "")
        # super(JsonFormatter, self).__init__(*args, **kwargs)
        logging.Formatter.__init__(self, *args, **kwargs)
        if not self.json_encoder and not self.json_default:
            def _default_json_handler(obj):
                '''Prints dates in ISO format'''
                if isinstance(obj, (datetime.date, datetime.time)):
                    return obj.isoformat()
                elif istraceback(obj):
                    tb = ''.join(traceback.format_tb(obj))
                    return tb.strip()
                elif isinstance(obj, Exception):
                    return "Exception: %s" % str(obj)
                return str(obj)

            self.json_default = _default_json_handler
        self._required_fields = self.parse()
        # asctime levelname instance_id must be in json body
        for field in ['asctime', 'levelname', 'instance_id', 'message']:
            if field not in self._required_fields:
                self._required_fields.append(field)
        self._skip_fields = RESERVED_ATTR_HASH

    def parse(self):
        """
        Parses format string looking for substitutions

        This method is responsible for returning a list of fields (as strings)
        to include in all log messages.
        """
        standard_formatters = re.compile(r'\((.+?)\)', re.IGNORECASE)
        return standard_formatters.findall(self._fmt)

    def add_fields(self, log_record, record, message_dict):
        """
        Override this method to implement custom logic for adding fields.
        """
        for field in self._required_fields:
            log_record[field] = record.__dict__.get(field)
        log_record.update(message_dict)
        merge_record_extra(record.__dict__, log_record, reserved=self._skip_fields)
        merge_record_extra(self.additional_fields, log_record, reserved=self._skip_fields)

    def process_log_record(self, log_record):
        """
        Override this method to implement custom logic
        on the possibly ordered dictionary.
        """
        if "asctime" in log_record and "time" not in log_record:
            log_record["time"] = log_record["asctime"]
            log_record.pop("asctime")

        if "levelname" in log_record and "level" not in log_record:
            log_record["level"] = log_record["levelname"]
            log_record.pop("levelname")

        if "message" in log_record and "log" not in log_record:
            log_record["log"] = log_record["message"]
            log_record.pop("message")

        if "instance_id" in log_record and not log_record['instance_id']:
            log_record['instance_id'] = socket.gethostname()
        return log_record

    def jsonify_log_record(self, log_record):
        """Returns a json string of the log record."""
        return self.json_serializer(log_record,
                                    default=self.json_default,
                                    cls=self.json_encoder,
                                    indent=self.json_indent)

    def formatTime(self, record, datefmt=None):
        """
        Return the creation time of the specified LogRecord as formatted text.

        This method should be called from format() by a formatter which
        wants to make use of a formatted time. This method can be overridden
        in formatters to provide for any specific requirement, but the
        basic behaviour is as follows: if datefmt (a string) is specified,
        it is used with time.strftime() to format the creation time of the
        record. Otherwise, the ISO8601 format is used. The resulting
        string is returned. This function uses a user-configurable function
        to convert the creation time to a tuple. By default, time.localtime()
        is used; to change this for a particular formatter instance, set the
        'converter' attribute to a function with the same signature as
        time.localtime() or time.gmtime(). To change it for all formatters,
        for example if you want all logging times to be shown in GMT,
        set the 'converter' attribute in the Formatter class.
        """
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            t = time.strftime("%Y-%m-%dT%H:%M:%S", ct)
            s = "%s.%03d" % (t, record.msecs)
        return s

    def format(self, record):
        """Formats a log record and serializes to json"""
        message_dict = {}
        if isinstance(record.msg, dict):
            message_dict = record.msg
            record.message = None
        else:
            record.message = record.getMessage()
        # only format time if needed
        if "asctime" in self._required_fields:
            record.asctime = self.formatTime(record, self.datefmt)

        # Display formatted exception, but allow overriding it in the
        # user-supplied dict.
        if record.exc_info and not message_dict.get('exc_info'):
            message_dict['exc_info'] = self.formatException(record.exc_info)
        if not message_dict.get('exc_info') and record.exc_text:
            message_dict['exc_info'] = record.exc_text

        try:
            log_record = OrderedDict()
        except NameError:
            log_record = {}

        self.add_fields(log_record, record, message_dict)
        log_record = self.process_log_record(log_record)

        return "%s%s" % (self.prefix, self.jsonify_log_record(log_record))
