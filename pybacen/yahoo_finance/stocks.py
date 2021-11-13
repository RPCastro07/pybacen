from pybacen.yahoo_finance.stock_quote import Stock_quote as sq
import pandas as pd

def read_stock_quote(stock_code: str or list, start: str = None, end: str = None, as_index: bool = True, pivot_table: bool = True):
    return sq().read_stock_quote(stock_code, start, end, as_index, pivot_table)

def describe(df: pd.core.frame.DataFrame, column_stats: str):
    return sq().describe(df, column_stats)

def candlestick(df: pd.core.frame.DataFrame, mov_avg: dict = None, template: str='plotly_dark'):
    return sq().candlestick(df, mov_avg, template)

def boxplot(df: pd.core.frame.DataFrame,  x: str = 'stock_code', y: str = 'adjclose', color: str = 'stock_code', template: str = 'plotly_dark'):
    return sq().boxplot(df, x, y, color, template)

