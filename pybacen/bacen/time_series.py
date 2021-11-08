from pybacen.bacen.bacen_time_series import Bacen_time_series as bc_ts

def read_time_series(*args, **kwargs):
    return bc_ts().read_time_series(*args, **kwargs)

def read_bacen_code(*args, **kwargs):
    return bc_ts().read_bacen_code(*args, **kwargs)

