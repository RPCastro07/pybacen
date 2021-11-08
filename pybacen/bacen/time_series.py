from pybacen.bacen.bacen_time_series import Bacen_time_series as bc_ts

def read_time_series(bacen_code: int, start: str = None, end: str = None, as_index: bool = True):
    return bc_ts().read_time_series(bacen_code, start, end, as_index)

def read_bacen_code(search_text: str, period: str = None, unit: str = None):
    return bc_ts().read_bacen_code(search_text, period, unit)

