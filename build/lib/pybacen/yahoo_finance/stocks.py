from pybacen.yahoo_finance.stock_quote import Stock_quote as sq

def read_stock_quote(*args, **kwargs):
    return sq().read_stock_quote(*args, **kwargs)

