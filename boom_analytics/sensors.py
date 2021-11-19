import os
import sensorsanalytics

from boom_analytics.util import getEnvPara


class Sensors(object):

    _instance = None
    _sensors_analytics = None
    _log_dir = getEnvPara('log_dir', '/boom_analysis/sensors/data/')

    def __init__(self, module_name: str):
        consumer = sensorsanalytics.ConcurrentLoggingConsumer(os.path.join(self._log_dir, module_name))
        self._sensors_analytics = sensorsanalytics.SensorsAnalytics(consumer)

    def __new__(cls, module_name: str, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def get_sensors_analytics(self):
        return self._sensors_analytics

    def flush(self):
        if self._sensors_analytics:
            self._sensors_analytics.flush()

    def close(self):
        if self._sensors_analytics:
            self._sensors_analytics.close()
