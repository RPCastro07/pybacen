from os import getcwd
from datetime import datetime
from warnings import filterwarnings, warn
import pandas as pd
from pandas import DataFrame
import json
from plotly.graph_objects import Figure, Scatter
from io import StringIO
from pybacen.utils.requests import Request
from pybacen.utils.validators import (date_validator, 
                                      compare_dates,
                                      to_date,
                                      sysdate)

def read_time_series(bacen_code: int, 
                    start: str = None, 
                    end: str = None, 
                    as_index: bool = True,
                    headers = None, 
                    auth = None, 
                    proxy = None,
                    proxy_auth= None,
                    cookies = None,                                       
                    ssl= None,
                    verify_ssl = None) -> DataFrame:

    _DATE_FORMAT = '%Y-%m-%d'
    _CONVERT_FORMAT = '%d/%m/%Y'

    if start is not None:
        _start = date_validator(start, format = _DATE_FORMAT, format_converter = _CONVERT_FORMAT)
        _start = f'&dataInicial={_start}'

    else:
        _start = ''

    if end is not None:
        _end = date_validator(end, format = _DATE_FORMAT, format_converter = _CONVERT_FORMAT)
        _end = f'&dataFinal={_end}'
    elif _start != '':
        _end = sysdate(_CONVERT_FORMAT)
        _end = f'&dataFinal={_end}'
    else:
        _end = ''

    if start is not None and end is not None: 
        compare_dates(start, end, _DATE_FORMAT)

    url = f'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{str(bacen_code)}/dados?formato=json{_start}{_end}'
    
    request = Request()

    try:                
        _response = request.get(urls = [url],
                                 headers = headers, 
                                 auth = auth, 
                                 proxy = proxy,
                                 proxy_auth=proxy_auth,
                                 cookies = cookies,                                       
                                 ssl= ssl,
                                 verify_ssl = verify_ssl)
    except Exception as exception:
        raise TypeError(exception)

    _content = json.loads(_response[0][1])
    _URL = _response[0][0]
    _STATUS_CODE = _response[0][2]
    _CONTENT_TYPE = _response[0][3]

    if 'application/json' not in _CONTENT_TYPE:
        raise TypeError(f"Invalid content type ('application/json' not in {_CONTENT_TYPE})")
        
    elif 200 >= _STATUS_CODE >= 299:
        raise TypeError(f"Status code ({_STATUS_CODE})")
                
    ts = pd.DataFrame(_content)

    ts = ts.rename(columns={'data': 'date', 'valor': 'value'})

    ts['date'] = pd.to_datetime(ts['date'], dayfirst=True) 

    ts['value'] = ts['value'].astype('float64')

    if as_index == True:
        ts.set_index('date', inplace=True)
    else:
        pass
        
    return ts


def read_bacen_code(search_text: str, 
                    period: str = None, 
                    unit: str = None,
                    headers = None, 
                    auth = None, 
                    proxy = None,
                    proxy_auth= None,
                    cookies = None,                                       
                    ssl= None,
                    verify_ssl = None) -> DataFrame:


    if type(search_text) != str:
        raise AttributeError(f'{search_text} not is str')
    
    if period is not None:
        if type(period) != str:
            raise AttributeError(f'{period} not is str')

    if unit is not None:
        if type(unit) != str:
            raise AttributeError(f'{unit} not is str')

    warn('Check the website: https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries')

    url = 'https://raw.githubusercontent.com/RPCastro07/Bacen_Time_Series_Codes/main/series_bacen_codes.csv'

    request = Request()

    try:                
        _response = request.get([url],
                                 headers = headers, 
                                 auth = auth, 
                                 proxy = proxy,
                                 proxy_auth=proxy_auth,
                                 cookies = cookies,                                       
                                 ssl= ssl,
                                 verify_ssl = verify_ssl)
    except Exception as exception:
        raise TypeError(exception)

    _content = str(_response[0][1], 'ISO-8859-1')
    _URL = _response[0][0]
    _STATUS_CODE = _response[0][2]
    _CONTENT_TYPE = _response[0][3]

    if 'text/plain' not in _CONTENT_TYPE and 'text/csv' not in _CONTENT_TYPE:
        raise TypeError(f"Invalid content type ({_CONTENT_TYPE} not in ['text/csv', 'text/plain'])")
        
    elif 200 >= _STATUS_CODE >= 299:
        raise TypeError(f"Status code ({_STATUS_CODE})")

    result = pd.read_csv(StringIO(_content), encoding='cp1252')

    if search_text is not None:
        if search_text != '':
            for i in list(filter(lambda x: x != '', search_text.split('%'))):
                if search_text != '':
                    result = result[result['nm_serie'].str.upper().str.contains(i.upper())].copy()

    if period != None and period != '':
        result = result[result['periodicity'].str.strip().str.upper()==period.upper().strip()]
        
    if unit != None and unit != '':
        result = result[result['unit'].str.strip().str.upper()==unit.upper().strip()]

    return result[['bacen_code', 'nm_serie', 'unit', 'periodicity', 'source', 'special']]

def line_plot(dfs: list, title: str, xtitle: str = 'Date', ytitle: str = 'Values', template: str = 'plotly_dark'):
    
    filterwarnings("ignore")
        
    dates = dfs[0][0].index
        
    for iteration, i in enumerate(dfs):
            
        df = i[0][i[0].index.isin(dates)].copy()

        df = df.sort_index(ascending=True)
            
        if iteration == 0:
            fig = Figure(Scatter(
                        x=df.index,
                        y=df['value'],
                        line = dict(color = i[2]),
                        name = i[1]
                        ))
                
            fig.update_layout(xaxis_rangeslider_visible=False,
                              template = template,
                              yaxis_title = ytitle, 
                              xaxis_title = xtitle,
                              title = title
                             )
                    
        else:
            fig.add_trace(Scatter(
                                  x=df.index,
                                  y=df['value'],
                                  line = dict(color = i[2]),
                                  name = i[1]
                                )
                        )
    fig.show() 

