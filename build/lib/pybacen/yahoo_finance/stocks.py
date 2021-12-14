from warnings import filterwarnings, warn
import json
import pandas as pd
from pandas import DataFrame, to_datetime
from plotly.graph_objects import Figure, Candlestick, Line, Scatter
from plotly.express import box
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    FrozenSet,
    Generator,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)


from pybacen.utils.requests import Request
from pybacen.utils.validators import (date_validator, 
                                      compare_dates,
                                      to_date,
                                      to_timestamp,
                                      sysdate)

from pybacen.yahoo_finance import (request_param, regular_expressions)

def read_stock_quote(stock_code: Union[list, str], 
                     start: str = None, 
                     end: str = None,
                     interval: str = '1d',
                     as_index: bool = True, 
                     pivot_table: bool = False,
                     content_type: str = 'application/json;charset=utf-8',
                     headers = request_param.USER_AGENT, 
                     auth = None, 
                     proxy = None,
                     proxy_auth= None,
                     cookies = None,                                       
                     ssl= None,
                     verify_ssl = None) -> pd.core.frame.DataFrame:
                     
    date_format = '%Y-%m-%d'
    convert_format = '%Y-%m-%d'

    if start is not None:
        _start = date_validator(start, format = date_format, format_converter = convert_format)
        
    if end is not None:
        _end = date_validator(end, format = date_format, format_converter = convert_format)
        
    if start is not None and end is not None:
        start_ts = int(to_timestamp(start, date_format))
        end_ts = int(to_timestamp(end, date_format))
        period = f'period1={start_ts}&period2={end_ts}'

    elif start is not None and end is None:
        start_ts = int(to_timestamp(start, date_format))
        end_ts = int(to_timestamp(sysdate(date_format), date_format))        
        period = f'period1={start_ts}&period2={end_ts}'

    elif start is None and end is not None:
        end_ts = int(to_timestamp(end, date_format))
        period = f'period2={end_ts}'

    type_validation = lambda x: [x] if type(x) == str else x if type(x) == list else None

    stock_code = type_validation(stock_code)

    if stock_code is not None:
        _BASE_URL = 'https://query2.finance.yahoo.com/v8/finance/chart/'

        urls = [f'{_BASE_URL}{stocks}?{period}&interval={interval}&events=history&includeAdjustedClose=true' for stocks in stock_code]

        headers = request_param.USER_AGENT if headers is None else headers
    else:
        raise AttributeError('Verify your stock_code: str or list')

    if stock_code is not None:
        
        request = Request()

        full_quote = pd.DataFrame()

        try:                
            _responses = request.get(urls,
                                     headers = headers, 
                                     auth = auth, 
                                     proxy = proxy,
                                     proxy_auth=proxy_auth,
                                     cookies = cookies,                                       
                                     ssl= ssl,
                                     verify_ssl = verify_ssl)
            
            #_responses = DataFrame(_responses)

        except Exception as exception:
            raise TypeError(exception)

        for _iterator, _response in enumerate(_responses):

            _URL = _response[0]
            _STATUS_CODE = _response[2]
            _CONTENT_TYPE = _response[3]

            if 'application/json' not in _CONTENT_TYPE:
                warn(f"{stock_code[int(_iterator)]}: Invalid content type ('application/json' not in {_CONTENT_TYPE})")
                continue
    
            elif _STATUS_CODE < 200 or _STATUS_CODE > 299:
                warn(f"{stock_code[_iterator]}: Status code ({_STATUS_CODE})")
                continue
            
            _content = json.loads(_response[1])
            
            if _content['chart']['error'] is None:

                results = {}

                results['stock_code'] = _content['chart']['result'][0]['meta']['symbol']

                results['timestamp'] = _content['chart']['result'][0]['timestamp']

                results.update(_content['chart']['result'][0]['indicators']['adjclose'][0])

                #OHLC
                results.update(_content['chart']['result'][0]['indicators']['quote'][0])

                quote = pd.DataFrame(results)

                quote['date'] = pd.to_datetime(pd.to_datetime(quote['timestamp'], unit="s").dt.date)

                quote = quote[['date', 
                               'stock_code', 
                               'open', 
                               'high', 
                               'low', 
                               'close', 
                               'volume', 
                               'adjclose']]

                full_quote = full_quote.append(quote, ignore_index=True)
            else:
                warn(_content['chart']['error'])

        full_quote = full_quote.sort_values(by=['date', 'stock_code'])

        if pivot_table == True:
            full_quote = pd.pivot_table(full_quote, values=['open', 'high', 'low', 'close', 'adjclose', 'volume'], index=['date'],
                    columns=['stock_code'], aggfunc= lambda x: x)

        else:
            if as_index == True:
                full_quote.set_index('date', inplace=True)
                
        return full_quote

    else:
        raise AttributeError('Verify your stock_code: str or list')


def candlestick(df: pd.core.frame.DataFrame, mov_avg: dict = None, template: str='plotly_dark'):
    filterwarnings("ignore")
    
    def get_candlestick(df, mov_avg):
        
        fig = Figure(Candlestick(x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close']))
        fig.update_layout(xaxis_rangeslider_visible=False, 
                        template=template,
                        yaxis_title = 'Price', xaxis_title = 'Date', title= ''.join(df['stock_code'].unique())
                        )

        if mov_avg is not None:
            for i in mov_avg:
                df[f'mov_avg_{i}'] = df['close'].rolling(window=i).mean()
                fig.add_trace(
                    Scatter(
                    x=df.index,
                    y=df[f'mov_avg_{i}'],
                    line = dict(color = mov_avg[i]),
                    name = f'mov_avg_{i}'
                    )
                )
        fig.show()
    
    for i in df['stock_code'].unique():
        get_candlestick(df[df['stock_code']== i], mov_avg)

def describe(df: pd.core.frame.DataFrame, column_stats: str):

    df = df.groupby(['stock_code'], as_index=False).agg(
        min = pd.NamedAgg(column= column_stats, aggfunc=min),
        max = pd.NamedAgg(column= column_stats, aggfunc=max),
        avg = pd.NamedAgg(column= column_stats, aggfunc='mean'),
        count = pd.NamedAgg(column= column_stats, aggfunc='count'),
        q25 = pd.NamedAgg(column= column_stats, aggfunc= lambda x: x.quantile(0.25)),
        q50 = pd.NamedAgg(column= column_stats, aggfunc='median'),
        q75 = pd.NamedAgg(column= column_stats, aggfunc= lambda x: x.quantile(0.75)),
        std = pd.NamedAgg(column= column_stats, aggfunc= 'std'),
        return_ = pd.NamedAgg(column= column_stats, aggfunc= lambda x: x[-1] / x[0] - 1)
    )
    df['std/avg'] = df['std'] / df['avg']
    return df
    
def boxplot(df: pd.core.frame.DataFrame,  x: str = 'stock_code', y: str = 'adjclose', color: str = 'stock_code', template: str = 'plotly_dark'):
    return box(df, x = x, y = y, color = color, template = template)