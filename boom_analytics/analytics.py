import json

import flask

from boom_analytics import Sensors, Segment
from urllib import parse


class Analytics(object):

    @classmethod
    def track(cls, user_id=None, event=None, properties=None):
        ajs_anonymous_id = None
        sensor_distinct_id = None
        if flask.has_request_context():
            ajs_anonymous_id = flask.request.cookies.get('ajs_anonymous_id')
            sensorsdata2015jssdkcross = flask.request.cookies.get('sensorsdata2015jssdkcross', '')
            sensor_distinct_id = cls._get_distinct_id(sensorsdata2015jssdkcross)

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

            if sensor_distinct_id:
                Sensors.get_sensors_analytics().track(sensor_distinct_id, event, properties, is_login_id=False)
            else:
                Sensors.get_sensors_analytics().track('undefined', event, properties, is_login_id=False)

        Sensors.flush()

    @classmethod
    def _get_distinct_id(cls, cross):
        try:
            cross_str = parse.unquote(cross)
            cross_dict = json.dumps(cross_str)
            return cross_dict.get('distinct_id', None)
        except:
            return None

    @classmethod
    def set_module_name(cls, name):
        Sensors(name)



