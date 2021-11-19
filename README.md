# boom_analytics_python_sdk

## Sensors Data
- _**usage**_
```python
from boom_analytics import Sensors

s = Sensors('<module_name>')

sa = s.get_sensors_analytics()

sa.track('ABCDE12345', 'UserLogin', is_login_id=True)

sa.flush()

sa.close()
```
- _**dependencies**_
```shell
 SensorsAnalyticsSDK 1.10.3
```
- env
```shell
export logdir=/boom_analysis/sensors/data/
# default value is </boom_analysis/sensors/data/>
```

## Segment
- todo