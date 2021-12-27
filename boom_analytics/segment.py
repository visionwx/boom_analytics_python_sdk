import analytics


class Segment(object):

    _instance = None
    _write_key = None
    _segment_analytics = analytics

    # def __init__(self):
    #     pass

    def __new__(cls, segment_write_key: str, *args, **kwargs):
        if cls._instance is None:
            if segment_write_key is None:
                raise Exception("segment_write_key is None")
            cls._instance = object.__new__(cls)
            cls._write_key = segment_write_key
        return cls._instance

    @classmethod
    def get_segment_analytics(cls):
        cls._segment_analytics.write_key = cls._write_key
        return cls._segment_analytics
