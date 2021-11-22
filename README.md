# boom_analytics_python_sdk

## Sensors Data
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
export logdir=/boom_analysis/sensors/data/
# default value is </boom_analysis/sensors/data/>
```

## Segment
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
pip install git+https://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@github.com/visionwx/boom_analytics_python_sdk@v0.0.1
```
