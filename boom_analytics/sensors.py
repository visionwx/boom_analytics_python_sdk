import os
import sensorsanalytics

from boom_analytics.util import getEnvPara


class Sensors(object):

    _instance = None
    _sensors_analytics = None
    _log_dir = getEnvPara('sensors_log_dir', '/boom_analysis/sensors/data/')

    def __init__(self, module_name: str):
        consumer = sensorsanalytics.ConcurrentLoggingConsumer(os.path.join(self._log_dir, module_name))
        Sensors._sensors_analytics = sensorsanalytics.SensorsAnalytics(consumer)

    def __new__(cls, module_name: str, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
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
