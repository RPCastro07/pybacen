from pybacen.bacen.bacen_data import Bacen_time_series as bc_ts

def read_time_series(bacen_code: int, start: str = None, end: str = None, as_index: bool = True):
    return bc_ts().read_time_series(bacen_code, start, end, as_index)

def read_bacen_code(search_text: str, period: str = None, unit: str = None):
    return bc_ts().read_bacen_code(search_text, period, unit)

def line_plot(dfs: list, title: str, xtitle: str= 'Date', ytitle: str= 'Values', template: str='plotly_dark'):
   return bc_ts().line_plot(dfs, title, xtitle, ytitle, template)