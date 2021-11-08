from pybacen.yahoo_finance.stock_quote import Stock_quote as sq

def read_stock_quote(stock_code, start: str = None, end: str = None, as_index: bool = True):
    return sq().read_stock_quote(stock_code, start, end, as_index)

