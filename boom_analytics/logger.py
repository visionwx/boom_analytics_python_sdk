# -*- coding: utf-8 -*-
import os
import re
import sys
import logging
import logging.handlers
import flask
from logging.handlers import SocketHandler, TimedRotatingFileHandler
from . import formatter


class TCPLogstashHandler(SocketHandler):
    """Python logging handler for Logstash. Sends events over TCP.
    :param host: The host of the logstash server.
    :param port: The port of the logstash server (default 5959).
    :param message_type: The type of the message (default logstash).
    :param fqdn; Indicates whether to show fully qualified domain name or not (default False).
    :param version: version of logstash event schema (default is 0).
    :param tags: list of tags for a logger (default is None).
    """

    def __init__(self, host, port=5959, message_type='logstash', tags=None, fqdn=False, version=0):
        super(TCPLogstashHandler, self).__init__(host, port)
        if version == 1:
            self.formatter = formatter.LogstashFormatterVersion1(message_type, tags, fqdn)
        else:
            self.formatter = formatter.LogstashFormatterVersion0(message_type, tags, fqdn)

    def makePickle(self, record):
        return str.encode(self.formatter.format(record)) + b'\n'


def catch_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            print("Logger error")
    return wrapper


class MyLogger:
    def __init__(self, logToConsole=True, logFilePath=None,
                 logTcpHost=None, logTcpPort=None, extra={},
                 loggerName="LOGGER", maxBytes=1024 * 1024 * 200, backupCount=30):
        self.logToConsole = logToConsole
        self.logFilePath = logFilePath
        self.logCounter = 0
        self.loggerName = loggerName
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        self.logTcpHost = logTcpHost
        self.logTcpPort = logTcpPort
        self.logger = self.initLogger()
        self.extra = extra

    def initLogFolder(self):
        if self.logFilePath is None:
            return
        logFolder = os.path.dirname(self.logFilePath)
        if not (os.path.exists(logFolder)):
            os.makedirs(logFolder)
        return True

    def initLogger(self):
        # ??????logger????????????????????????????????????root logger
        logger = logging.getLogger(self.loggerName)

        # ??????logger????????????
        json_formatter = formatter.LogstashFormatterVersion1()

        # ????????????, ????????????RotatingFileHandler???
        # ????????????30?????????????????????????????????????????????200M
        if self.logFilePath is not None:
            # ??????log folder
            self.initLogFolder()
            
            # interval ???????????????
            # when="MIDNIGHT", interval=1 ????????????0??????????????????????????????????????????
            # backupCount  ????????????????????????
            fileHandler = logging.handlers.TimedRotatingFileHandler(
                filename=self.logFilePath,
                when='MIDNIGHT',
                interval=1,
                backupCount=self.backupCount
            )

            # filename="mylog" suffix??????????????????????????????mylog.2020-02-25.log
            # fileHandler.suffix = "%Y-%m-%d.log"
            fileHandler.suffix = "%Y-%m-%d"
            # extMatch???????????????????????????????????????????????????????????????
            # ??????????????????suffix???extMatch????????????????????????????????????????????????????????????????????????
            fileHandler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}$")
            fileHandler.setFormatter(json_formatter)
            logger.addHandler(fileHandler)

        # ???????????????
        if self.logToConsole:
            consoleHandler = logging.StreamHandler(sys.stdout)
            # consoleHandler.formatter = json_formatter
            logger.addHandler(consoleHandler)

        # tcp???????????????
        if self.logTcpHost is not None and self.logTcpPort is not None:
            logger.addHandler(TCPLogstashHandler(
                host=self.logTcpHost,
                port=self.logTcpPort,
                version=1,
            ))

        # ?????????????????????????????????????????????WARN??????
        logger.setLevel(logging.INFO)

        return logger

    @catch_exception
    def info(self, logContent, tag, extra=None):
        if extra is None:
            extra = {}
        content = "[" + tag + "] " + logContent
        extra.update(self.extra)
        extra.update({'logger_name': tag})

        trace_id = None
        if flask.has_request_context():
            try:
                trace_id = flask.g.trace_id
            except:
                pass
        extra.update({'trace_id': trace_id})

        self.logger.info(content, extra=extra)
        self.logCounter += 1
        return True

    @catch_exception
    def warning(self, logContent, tag, extra=None):
        if extra is None:
            extra = {}
        content = "[" + tag + "] " + logContent
        extra.update(self.extra)
        extra.update({'logger_name': tag})

        trace_id = None
        if flask.has_request_context():
            try:
                trace_id = flask.g.trace_id
            except:
                pass
        extra.update({'trace_id': trace_id})
        
        self.logger.warning(content, extra=extra)
        self.logCounter += 1
        return True

    @catch_exception
    def error(self, logContent, tag, extra=None):
        if extra is None:
            extra = {}
        content = "[" + tag + "] " + logContent
        extra.update(self.extra)
        extra.update({'logger_name': tag})

        trace_id = None
        if flask.has_request_context():
            try:
                trace_id = flask.g.trace_id
            except:
                pass
        extra.update({'trace_id': trace_id})
        
        self.logger.error(content, extra=extra)
        self.logCounter += 1
        return True
