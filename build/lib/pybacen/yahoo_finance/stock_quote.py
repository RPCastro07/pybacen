import json
import requests
import re
import pandas as pd
from pandas import DataFrame, to_datetime
from plotly.graph_objects import Figure, Candlestick, Line, Scatter
from plotly.express import box
import warnings


try:
    pd.options.display.max_rows = 999
    pd.set_option('display.max_colwidth', None)
except:
    pass

class Stock_quote:

    def __init__(self):
        self.user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
        self.quote_pattern_json = r"root\.App\.main = (.*?);\n}\(this\)\);"

    def read_stock_quote(self, stock_code: str or list, start: str = None, end: str = None, as_index: bool = True, pivot_table: bool = False) -> pd.core.frame.DataFrame:
        
        full_quote = pd.DataFrame()

        type_validation = lambda x: [x] if type(x) == str else x if type(x) == list else None

        stock_code = type_validation(stock_code)

        if stock_code is not None:
            for stock in stock_code:
                url = f'https://finance.yahoo.com/quote/{stock}/history'
                    
                response = requests.get(url, headers = self.user_agent)

                response = json.loads(re.search(self.quote_pattern_json, response.text, re.DOTALL).group(1))

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

        print('Error: Verify your stock_code: str or list')

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

    def boxplot(df: pd.core.frame.DataFrame,  x: str = 'stock_code', y: str = 'adjclose', color: str = 'stock_code', template: str = 'plotly_dark'):
        return box(df, x = x, y = y, color = color, template = template)