import json
import requests
import os
import re
import pandas as pd
from pandas import DataFrame, to_datetime

try:
    pd.options.display.max_rows = 999
    pd.set_option('display.max_colwidth', None)
except:
    pass

class Stock_quote:

    def __init__(self):
        self.user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
        self.quote_pattern_json = r"root\.App\.main = (.*?);\n}\(this\)\);"

    def read_stock_quote(self, stock_code, start: str = None, end: str = None, as_index: bool = True) -> pd.core.frame.DataFrame:
        url = f'https://finance.yahoo.com/quote/{stock_code}/history'
        
        response = requests.get(url,
                                headers = self.user_agent
                                )

        response = json.loads(re.search(self.quote_pattern_json, response.text, re.DOTALL).group(1))

        reponse = response["context"]["dispatcher"]["stores"]["HistoricalPriceStore"]

        quote = DataFrame(reponse['prices'])

        quote['date'] = to_datetime(to_datetime(quote["date"], unit="s").dt.date)

        start = start if start is not None else quote['date'].min()
        end = end if end is not None else quote['date'].max()

        quote = quote[(quote['date']>=start) & (quote['date']<=end)].copy()

        if as_index == True:
            quote.set_index('date', inplace=True)
        else:
            pass

        quote = quote[['open', 'high', 'low', 'close', 'volume', 'adjclose']]

        return quote
