import os

from boom_analytics import MyLogger

if __name__ == '__main__':

    LOGGER = MyLogger(
        # logTcpHost=os.environ.get('logger_host'),
        # logTcpPort=os.environ.get('logger_tcp'),
        logFilePath='/Users/laniakea/Documents/log/boom_media.log',
        maxBytes=50,
        logToConsole=True,
        loggerName='boom_media',
        extra={
            'applicationName': 'boom_media',
            'version': '<image_version>'
        }
    )

    LOGGER.info("测试一下", __name__)
