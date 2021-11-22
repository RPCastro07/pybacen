import json
import re
import pandas as pd
from pandas import DataFrame, to_datetime
from plotly.graph_objects import Figure, Candlestick, Line, Scatter
from plotly.express import box
import warnings

from pybacen.utils.requests import Request
from pybacen.utils.validators import (date_validator, 
                                      compare_dates,
                                      to_date,
                                      sysdate)

from pybacen.yahoo_finance import (request_param, regular_expressions)

def read_stock_quote(self, 
                     stock_code: str or list, 
                     start: str = None, 
                     end: str = None, 
                     as_index: bool = True, 
                     pivot_table: bool = False,
                     headers = None,
                     auth = None,
                     proxies = None, 
                     cert = None, 
                     cookies = None, 
                     hooks = None,
                     stream = None,
                     verify = True) -> pd.core.frame.DataFrame:
                     
    date_format = '%Y-%m-%d'
    convert_format = '%Y-%m-%d'

    if start is not None:
        _start = date_validator(start, format = date_format, format_converter = convert_format)

    if end is not None:
        _end = date_validator(end, format = date_format, format_converter = convert_format)

    elif _start != '':
        _end = sysdate(convert_format)

    if start is not None and end is not None: 
        compare_dates(start, end, date_format)

    full_quote = pd.DataFrame()

    type_validation = lambda x: [x] if type(x) == str else x if type(x) == list else None

    stock_code = type_validation(stock_code)

    request = Request()

    headers = request_param.USER_AGENT if headers is None else headers

    if stock_code is not None:
        for stock in stock_code:
            try:
                
                url = f'https://finance.yahoo.com/quote/{stock}/history'

                response = request.get(url,
                                       headers = headers, 
                                       auth = auth, 
                                       proxies = proxies, 
                                       cert = cert, 
                                       cookies = cookies,
                                       hooks = hooks, 
                                       stream = stream, 
                                       verify = verify)
            except Exception as exception:
                warnings.warn(f"Invalid stock code '{stock}': {exception}")
                continue

            response = json.loads(re.search(regular_expressions.QUOTE_PATTERN_JSON, response.text, re.DOTALL).group(1))

            reponse = response["context"]["dispatcher"]["stores"]["HistoricalPriceStore"]

            quote = DataFrame(reponse['prices'])

            quote['date'] = to_datetime(to_datetime(quote["date"], unit="s").dt.date)

            quote = quote[quote['adjclose'].isnull() == False]

            start = start if start is not None else quote['date'].min()

            end = end if end is not None else quote['date'].max()

            quote = quote[(quote['date']>=start) & (quote['date']<=end)].copy()

            quote['stock_code'] = stock

            quote = quote[['date', 'stock_code', 'open', 'high', 'low', 'close', 'volume', 'adjclose']]

            full_quote = full_quote.append(quote, ignore_index=True)
        
        full_quote = full_quote.sort_values(by=['date', 'stock_code'])

        if pivot_table == True:
            full_quote = pd.pivot_table(full_quote, values=['open', 'high', 'low', 'close', 'adjclose'], index=['date'],
                    columns=['stock_code'], aggfunc= lambda x: x)

        else:
            if as_index == True:
                full_quote.set_index('date', inplace=True)
                
        return full_quote

    else:
        raise AttributeError('Verify your stock_code: str or list')

def candlestick(self, df: pd.core.frame.DataFrame, mov_avg: dict = None, template: str='plotly_dark'):
    warnings.filterwarnings("ignore")
    
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

def describe(self, df: pd.core.frame.DataFrame, column_stats: str):

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
    
def boxplot(self, df: pd.core.frame.DataFrame,  x: str = 'stock_code', y: str = 'adjclose', color: str = 'stock_code', template: str = 'plotly_dark'):
    return box(df, x = x, y = y, color = color, template = template)