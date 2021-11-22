# boom_analytics_python_sdk

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

segment.identify('f4ca124298', {
    'name': 'Michael Bolton',
    'email': 'mbolton@example.com',
    'created_at': datetime.datetime.now()
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

## Download
```shell
pip install git+https://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@github.com/visionwx/boom_analytics_python_sdk.git@v0.0.3
```
