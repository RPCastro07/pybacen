from pybacen.cvm.cvm_investment_funds import Investment_funds as fi

def read_funds_quote(start: str = None, end: str = None):
    return fi().read_funds_quote(start, end)

def read_registration_funds():
    return fi().read_registration_funds()