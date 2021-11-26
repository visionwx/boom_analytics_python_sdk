import os
import uuid


def getEnvPara(parameter_name, default=None,
               raise_exception_if_none=True):
    parameter_value = os.environ.get(parameter_name, default)
    if parameter_value is None and raise_exception_if_none:
        raise Exception(parameter_name + " not defined")
    return parameter_value


def trace_id():
    return str(uuid.uuid1()).replace('-', '')
