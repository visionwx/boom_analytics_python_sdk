from boom_analytics import MyLogger


if __name__ == '__main__':

    LOGGER = MyLogger(
        logFilePath='/Users/laniakea/Documents/log/boom_media.log',
        logToConsole=True,
        loggerName='boom_media',
        extra={
            'applicationName': 'boom_media',
            'version': '<image_version>'
        }
    )

    LOGGER.info("测试中文", __name__, extra={"userId": "123123123"})
