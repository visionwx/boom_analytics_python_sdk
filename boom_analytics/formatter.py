import logging
import socket
import traceback
from datetime import datetime
import json


class LogstashFormatterBase(logging.Formatter):
    # The list contains all the attributes listed in
    # http://docs.python.org/library/logging.html#logrecord-attributes
    skip_list = (
        'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
        'funcName', 'id', 'levelname', 'levelno', 'lineno', 'module',
        'msecs', 'msecs', 'message', 'msg', 'name', 'pathname', 'process',
        'processName', 'relativeCreated', 'thread', 'threadName', 'extra'
    )

    easy_types = (str, bool, dict, float, int, list, type(None))

    def __init__(self, message_type='Logstash', tags=None, fqdn=False):
        self.message_type = message_type
        self.tags = tags if tags is not None else []

        if fqdn:
            self.host = socket.getfqdn()
        else:
            self.host = socket.gethostname()

    def get_extra_fields(self, record):
        fields = {}

        for key, value in record.__dict__.items():
            if key not in self.skip_list:
                if isinstance(value, self.easy_types):
                    fields[key] = value
                else:
                    fields[key] = repr(value)

        return fields

    def get_debug_fields(self, record):
        fields = {
            'stack_trace': self.format_exception(record.exc_info),
            'lineno': record.lineno,
            'process': record.process,
            'thread_name': record.threadName,
        }

        # funcName was added in 2.5
        if not getattr(record, 'funcName', None):
            fields['funcName'] = record.funcName

        # processName was added in 2.6
        if not getattr(record, 'processName', None):
            fields['processName'] = record.processName

        return fields

    @classmethod
    def format_source(cls, message_type, host, path):
        return "%s://%s/%s" % (message_type, host, path)

    @classmethod
    def format_timestamp(cls, time):
        tstamp = datetime.utcfromtimestamp(time)
        return tstamp.strftime("%Y-%m-%dT%H:%M:%S") + ".%03dZ" % (tstamp.microsecond / 1000)

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    @classmethod
    def serialize(cls, message):
        return json.dumps(message)


class LogstashFormatterVersion0(LogstashFormatterBase):
    version = 0

    def format(self, record):
        # Create message dict
        message = {
            '@timestamp': self.format_timestamp(record.created),
            '@message': record.getMessage(),
            '@source': self.format_source(
                self.message_type, self.host, record.pathname
            ),
            '@source_host': self.host,
            '@source_path': record.pathname,
            '@tags': self.tags,
            '@type': self.message_type,
            '@fields': {
                'levelname': record.levelname,
                'logger': record.name,
            },
        }

        # Add extra fields
        message['@fields'].update(self.get_extra_fields(record))

        # If exception, add debug info
        if record.exc_info:
            message['@fields'].update(self.get_debug_fields(record))

        return self.serialize(message)


class LogstashFormatterVersion1(LogstashFormatterBase):

    def format(self, record):
        # Create message dict
        message = {
            '@timestamp': self.format_timestamp(record.created),
            '@version': '1',
            'message': record.getMessage(),
            'host': self.host,
            'path': record.pathname,
            'tags': self.tags,
            'type': self.message_type,

            # Extra Fields
            'level': record.levelname,
            'logger_name': record.name,
        }

        # Add extra fields
        message.update(self.get_extra_fields(record))

        # If exception, add debug info
        if record.exc_info:
            message.update(self.get_debug_fields(record))

        return self.serialize(message)








# class JsonFormatter(logging.Formatter):
#     """
#     Formatter that outputs JSON strings after parsing the LogRecord.

#     @param dict fmt_dict: Key: logging format attribute pairs. Defaults to {"message": "message"}.
#     @param str time_format: time.strftime() format string. Default: "%Y-%m-%dT%H:%M:%S"
#     @param str msec_format: Microsecond formatting. Appended at the end. Default: "%s.%03dZ"
#     """
#     def __init__(self, fmt_dict: dict = None, time_format: str = "%Y-%m-%dT%H:%M:%S", msec_format: str = "%s.%03dZ"):
#         self.fmt_dict = fmt_dict if fmt_dict is not None else {"message": "message"}
#         self.default_time_format = time_format
#         self.default_msec_format = msec_format
#         self.datefmt = None

#     def usesTime(self) -> bool:
#         """
#         Overwritten to look for the attribute in the format dict values instead of the fmt string.
#         """
#         return "asctime" in self.fmt_dict.values()

#     def formatMessage(self, record) -> dict:
#         """
#         Overwritten to return a dictionary of the relevant LogRecord attributes instead of a string. 
#         KeyError is raised if an unknown attribute is provided in the fmt_dict. 
#         """
#         return {fmt_key: record.__dict__[fmt_val] for fmt_key, fmt_val in self.fmt_dict.items()}

#     def format(self, record) -> str:
#         """
#         Mostly the same as the parent's class method, the difference being that a dict is manipulated and dumped as JSON
#         instead of a string.
#         """
#         record.message = record.getMessage()
        
#         if self.usesTime():
#             record.asctime = self.formatTime(record, self.datefmt)

#         message_dict = self.formatMessage(record)

#         if record.exc_info:
#             # Cache the traceback text to avoid converting it multiple times
#             # (it's constant anyway)
#             if not record.exc_text:
#                 record.exc_text = self.formatException(record.exc_info)

#         if record.exc_text:
#             message_dict["exc_info"] = record.exc_text

#         if record.stack_info:
#             message_dict["stack_info"] = self.formatStack(record.stack_info)

#         return json.dumps(message_dict)

# usage
# json_formatter = JsonFormatter({
#     "level": "levelname", 
#     "message": "message", 
#     "applicationName": "applicationName",
#     "fileName": "filename",
#     "funcName": "funcName",
#     "logger_name": "logger_name",
#     "module": "module",
#     "pathName": "pathname",
#     "trace_id": "trace_id",
#     "userId": "userId",
#     "version": "version",
#     "datetime": "asctime"
# })