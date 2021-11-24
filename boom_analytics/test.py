import os

from boom_analytics import MyLogger

if __name__ == '__main__':

    LOGGER = MyLogger(
        # logTcpHost=os.environ.get('logger_host'),
        # logTcpPort=os.environ.get('logger_tcp'),
        logToConsole=True,
        loggerName='boom_authentication',
        extra={
            'applicationName': 'boom_authentication',
            'version': '<image_version>'
        }
    )

    LOGGER.info("测试一下", __name__)