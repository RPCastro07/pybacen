from os import getcwd
from datetime import datetime
from warnings import filterwarnings, warn
import pandas as pd 
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
                    proxies = None, 
                    cert = None, 
                    cookies = None, 
                    hooks = None,
                    stream = None,
                    verify = True) -> pd.core.frame.DataFrame:

    date_format = '%Y-%m-%d'
    convert_format = '%d/%m/%Y'

    if start is not None:
        _start = date_validator(start, format = date_format, format_converter = convert_format)
        _start = f'&dataInicial={_start}'

    else:
        _start = ''

    if end is not None:
        _end = date_validator(end, format = date_format, format_converter = convert_format)
        _end = f'&dataFinal={_end}'
    elif _start != '':
        _end = sysdate(convert_format)
        _end = f'&dataFinal={_end}'
    else:
        _end = ''

    if start is not None and end is not None: 
        compare_dates(start, end, date_format)

    url = f'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{str(bacen_code)}/dados?formato=json{_start}{_end}'

    request = Request()

    response = request.get(url, 
                           headers = headers, 
                           auth = auth, 
                           proxies = proxies, 
                           cert = cert, 
                           cookies = cookies,
                           hooks = hooks, 
                           stream = stream, 
                           verify = verify)

    json_resp = json.loads(response.content)

    ts = pd.DataFrame(json_resp)

    ts = ts.rename(columns={'data': 'date', 'valor': 'value'})

    ts['date'] = pd.to_datetime(ts['date'], dayfirst=True) 

    ts['value'] = ts['value'].astype('float64')

    if as_index == True:
        ts.set_index('date', inplace=True)
        #ts.drop('data', inplace=True, axis=1)
    else:
        pass
        
    return ts


def read_bacen_code(search_text: str, 
                    period: str = None, 
                    unit: str = None,
                    headers = None,
                    auth = None,
                    proxies = None, 
                    cert = None, 
                    cookies = None, 
                    hooks = None,
                    stream = None,
                    verify = True) -> pd.core.frame.DataFrame:

    url = 'https://raw.githubusercontent.com/RPCastro07/Bacen_Time_Series_Codes/main/series_bacen_codes.csv'

    request = Request()

    response = request.get(url, 
                           headers = headers, 
                           auth = auth, 
                           proxies = proxies, 
                           cert = cert, 
                           cookies = cookies,
                           hooks = hooks, 
                           stream = stream, 
                           verify = verify)

    result = pd.read_csv(StringIO(response.content.decode('cp1252')), encoding='cp1252')

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