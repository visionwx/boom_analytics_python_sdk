# boom_analytics_python_sdk

## Analytics
```python
from boom_analytics import Analytics

# 在项目启动时设置
Analytics.set_module_name('<module_name>')

Analytics.track('<user_id>', '<event_name>', {...})

#无法获取userid的情况
Analytics.track(event='<event>', properties={
    'key1': 'value1',
    'key2': 'value2',
    'general_attr': { # 事件参数中，只有general_attr可以是字典，其他的必须是一维数据
        ...
    }
})
```
#### env
- `export sensors_log_dir=/boom_analysis/sensors/data/`
- `export segment_write_key="Q5Ya2TEmuHDDIiutffY2qBtCgHBqZprm"` # test env


## Sensors Data
[https://manual.sensorsdata.cn/sa/latest/tech_sdk_server_python-1573931.html](https://manual.sensorsdata.cn/sa/latest/tech_sdk_server_python-1573931.html)
- _**usage**_
```python
from boom_analytics import Sensors

s = Sensors('<module_name>')

sa = Sensors.get_sensors_analytics()

sa.track('ABCDE12345', 'UserLogin', is_login_id=True)

sa.flush()

sa.close()
```
- _**dependencies**_
```text
 SensorsAnalyticsSDK==1.10.3
```
- **_env_**
```shell
export sensors_log_dir=/boom_analysis/sensors/data/
# default value is </boom_analysis/sensors/data/>
```

## Segment
[https://segment.com/docs/connections/sources/catalog/libraries/server/python/](https://segment.com/docs/connections/sources/catalog/libraries/server/python/)
- **_usage_**
```python
from boom_analytics import Segment
import datetime

segment = Segment.get_segment_analytics()

def general_attr(user_id=None, user_name=None, phone=None):
    return {
        'platform': {
            'name': 'server',
            'version': '<image_version>'
        },
        'user_info': {
            'name': user_name,
            'id': user_id,
            'phone': phone
        }
    }

segment.identify('f4ca124298', {
    'name': 'Michael Bolton',
    'email': 'mbolton@example.com',
    'created_at': datetime.datetime.now(),
    # 通用属性
    'general_attr': general_attr(user_name="xx", user_id="xx", phone="xx")
})
```
- **_dependencies_**
```text
analytics-python==1.4.0
```
- **_env_**
```shell
export segment_write_key="Q5Ya2TEmuHDDIiutffY2qBtCgHBqZprm"  # test
export segment_write_key="4miViANb06lgSGwlBGdoZBvCd0tNtgj0"  # prod
```

## Logger
- **_usage_**
```python
from boom_analytics import MyLogger
from flask import g
import os

LOGGER = MyLogger(
    logTcpHost=os.environ.get('logger_host'),
    logTcpPort=os.environ.get('logger_tcp'),
    loggerName='boom_authentication',
    extra={
        'applicationName': 'boom_authentication',
        'version': '<image_version>'
    }
)

LOGGER.info("测试日志", __name__, extra={})
```
- **_trace_**
```python
from boom_analytics import trace_id

from flask import Flask, request, g

app = Flask(__name__)

@app.before_request
def before_req():
    g.trace_id = request.headers.get('trace_id', trace_id())
    
@app.after_request
def after_req(response):
    response.headers["trace_id"] = g.trace_id
    return response

##add trace_id before request 
import requests
url = "..."
headers = {'trace_id': g.trace_id}
requests.get(url, headers=headers)
```

## Download
```shell
pip install git+https://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@github.com/visionwx/boom_analytics_python_sdk.git@v0.1.2
```
