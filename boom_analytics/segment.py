import analytics

from boom_analytics.util import getEnvPara


class Segment(object):

    _instance = None
    _segment_analytics = analytics
    _write_key = getEnvPara('segment_write_key')

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def get_segment_analytics(cls):
        cls._segment_analytics.write_key = cls._write_key
        return cls._segment_analytics
