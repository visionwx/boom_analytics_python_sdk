import json

import flask

from boom_analytics import Sensors, Segment
from urllib import parse


class Analytics(object):

    @classmethod
    def track(cls, user_id=None, event=None, properties=None):
        ajs_anonymous_id = None
        sensors_distinct_id = None
        boom_platform_type = None
        boom_platform_version = None
        if flask.has_request_context():
            ajs_anonymous_id = flask.request.headers.get('ajs_anonymous_id', '')
            sensors_distinct_id = flask.request.headers.get('sensors_distinct_id', '')
            boom_platform_type = flask.request.headers.get('boom_platform_type', '')
            boom_platform_version = flask.request.headers.get('boom_platform_version', '')

        if user_id and user_id != '':
            Segment.get_segment_analytics().track(user_id, event, properties)
            if properties and 'general_attr' in properties:
                properties.pop('general_attr')
            Sensors.get_sensors_analytics().track(user_id, event, properties, is_login_id=True)
        else:
            if ajs_anonymous_id:
                Segment.get_segment_analytics().track(event=event, properties=properties, anonymous_id=ajs_anonymous_id)
            else:
                Segment.get_segment_analytics().track(event=event, properties=properties, anonymous_id='undefined')

            if properties and 'general_attr' in properties:
                properties.pop('general_attr')
            properties['platform_type'] = boom_platform_type
            properties['platform_version'] = boom_platform_version

            if sensors_distinct_id:
                Sensors.get_sensors_analytics().track(sensors_distinct_id, event, properties, is_login_id=False)
            else:
                Sensors.get_sensors_analytics().track('undefined', event, properties, is_login_id=False)

        Sensors.flush()

    @classmethod
    def get_distinct_id(cls, cross):
        try:
            cross_str = parse.unquote(cross)
            cross_dict = json.loads(cross_str)
            return cross_dict.get('distinct_id', None)
        except:
            return None

    @classmethod
    def set_module_name(cls, name, sensorsLogDir):
        Sensors(name, sensorsLogDir)

    @classmethod
    def set_segment_write_key(cls, key):
        Segment(**{'segment_write_key': key})



