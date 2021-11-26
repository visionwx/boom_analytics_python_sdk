# -*- coding: utf-8 -*-
import os
import sys
import logging
import logging.handlers

from logging.handlers import SocketHandler
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


class MyLogger:
    def __init__(self, logToConsole=True, logFilePath=None,
                 logTcpHost=None, logTcpPort=None, extra={},
                 loggerName="LOGGER", maxBytes=1024 * 1024, backupCount=5):
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
        # 获取logger实例，如果参数为空则返回root logger
        logger = logging.getLogger(self.loggerName)

        # 指定logger输出格式
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)-8s: %(message)s')

        # 文件日志, 定义一个RotatingFileHandler，
        # 最多备份5个日志文件，每个日志文件最大10M
        if self.logFilePath is not None:
            # 检查log folder
            self.initLogFolder()
            fileHandler = logging.handlers.RotatingFileHandler(
                self.logFilePath,
                maxBytes=self.maxBytes,
                backupCount=self.backupCount)
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)

        # 控制台日志
        if self.logToConsole:
            consoleHandler = logging.StreamHandler(sys.stdout)
            consoleHandler.formatter = formatter
            logger.addHandler(consoleHandler)

        # tcp日志服务器
        if self.logTcpHost is not None and self.logTcpPort is not None:
            logger.addHandler(TCPLogstashHandler(
                host=self.logTcpHost,
                port=self.logTcpPort,
                version=1,
            ))

        # 指定日志的最低输出级别，默认为WARN级别
        logger.setLevel(logging.INFO)

        return logger

    def info(self, logContent, tag, trace_id=None, extra=None):
        if extra is None:
            extra = {}
        content = "[" + tag + "] " + logContent
        extra.update(self.extra)
        extra.update({'logger_name': tag})
        extra.update({'trace_id': trace_id})
        self.logger.info(content, extra=extra)
        self.logCounter += 1
        return True

    def warning(self, logContent, tag, trace_id=None, extra=None):
        if extra is None:
            extra = {}
        content = "[" + tag + "] " + logContent
        extra.update(self.extra)
        extra.update({'logger_name': tag})
        extra.update({'trace_id': trace_id})
        self.logger.warning(content, extra=extra)
        self.logCounter += 1
        return True

    def error(self, logContent, tag, trace_id=None, extra=None):
        if extra is None:
            extra = {}
        content = "[" + tag + "] " + logContent
        extra.update(self.extra)
        extra.update({'logger_name': tag})
        extra.update({'trace_id': trace_id})
        self.logger.error(content, extra=extra)
        self.logCounter += 1
        return True
