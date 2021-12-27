import os
import sensorsanalytics


class Sensors(object):

    _instance = None
    _sensors_analytics = None
    _log_dir = None

    # def __init__(self, module_name: str):
    #     pass

    def __new__(cls, module_name: str, sensors_log_dir: str, *args, **kwargs):
        if cls._instance is None:
            if sensors_log_dir is None:
                raise Exception("sensors_log_dir is None")
            cls._instance = object.__new__(cls)
            cls._log_dir = sensors_log_dir
            consumer = sensorsanalytics.ConcurrentLoggingConsumer(os.path.join(cls._log_dir, module_name))
            Sensors._sensors_analytics = sensorsanalytics.SensorsAnalytics(consumer)
        return cls._instance

    @classmethod
    def get_sensors_analytics(cls):
        return cls._sensors_analytics

    @classmethod
    def flush(cls):
        if cls._sensors_analytics:
            cls._sensors_analytics.flush()

    @classmethod
    def close(cls):
        if cls._sensors_analytics:
            cls._sensors_analytics.close()
