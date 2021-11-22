import pandas as pd
from io import StringIO

from pybacen.utils.requests import Request
from pybacen.utils.validators import (date_validator, 
                                      compare_dates,
                                      to_date,
                                      sysdate)

def read_funds_quote(start: str, 
                     end: str,
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

    date_ranges = pd.date_range(start[0:7], end[0:7], freq='MS')

    request = Request()
                           
    full_fq = pd.DataFrame()
     
    for _date in date_ranges:

        url = f'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{_date.year}{_date.month}.csv'
        
        response = request.get(url,
                                headers = headers, 
                                auth = auth, 
                                proxies = proxies, 
                                cert = cert, 
                                cookies = cookies,
                                hooks = hooks, 
                                stream = stream, 
                                verify = verify)

        try:
            fq = pd.read_csv(StringIO(response.content.decode('utf-8')), sep=';')
        except UnicodeDecodeError:
            fq = pd.read_csv(StringIO(response.content.decode('ISO-8859-1')), sep=';')
        
        fq['DT_COMPTC'] = pd.to_datetime(fq['DT_COMPTC'], format=('%Y-%m-%d'))
        full_fq = pd.concat([full_fq, fq], ignore_index=True)
    
    start = start if start is not None else full_fq['DT_COMPTC'].min()
    end = end if end is not None else full_fq['DT_COMPTC'].max()

    full_fq = full_fq[(full_fq['DT_COMPTC']>=start) & (full_fq['DT_COMPTC']<=end)].copy()
         
    return full_fq

def read_registration_funds(headers = None,
                            auth = None,
                            proxies = None, 
                            cert = None, 
                            cookies = None, 
                            hooks = None,
                            stream = None,
                            verify = True) -> pd.core.frame.DataFrame:

    url = f'http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv'

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

    try:
        rf = pd.read_csv(StringIO(response.content.decode('ISO-8859-1')), sep=';')
    except:
        rf = pd.read_csv(StringIO(response.content), sep=';')

    return rf