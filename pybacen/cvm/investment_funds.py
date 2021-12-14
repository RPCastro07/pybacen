from io import StringIO
from pandas import DataFrame
import pandas as pd
from pybacen.utils.requests import Request
from pybacen.utils.validators import (date_validator, 
                                      compare_dates,
                                      to_date,
                                      sysdate)

def read_funds_quote(start: str, 
                     end: str,
                     headers = None, 
                     auth = None, 
                     proxy = None,
                     proxy_auth= None,
                     cookies = None,                                       
                     ssl= None,
                     verify_ssl = None) -> DataFrame:

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
                           
    full_fq = DataFrame()
     
    _URL_BASE = 'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_'
        
    url = [f'{_URL_BASE}{_date.year}{_date.month}.csv' for _date in date_ranges]
        
    try:                
        _responses = request.get(url,
                                 headers = headers, 
                                 auth = auth, 
                                 proxy = proxy,
                                 proxy_auth=proxy_auth,
                                 cookies = cookies,                                       
                                 ssl= ssl,
                                 verify_ssl = verify_ssl)
    except Exception as exception:
        raise TypeError(exception)

    for _response in _responses:

        _URL = _response[0]
        _STATUS_CODE = _response[2]
        _CONTENT_TYPE = _response[3]

        if 'text/plain' not in _CONTENT_TYPE and 'text/csv' not in _CONTENT_TYPE:
            raise TypeError(f"Invalid content type ({_CONTENT_TYPE} not in ['text/csv', 'text/plain'])")
            
        elif _STATUS_CODE < 200 or _STATUS_CODE > 299:
            raise TypeError(f"Status code ({_STATUS_CODE})")

        _content = str(_response[1], 'ISO-8859-1')

        result = pd.read_csv(StringIO(_content), sep=';', encoding='ISO-8859-1')

        result['DT_COMPTC'] = pd.to_datetime(result['DT_COMPTC'], format=('%Y-%m-%d'))
        
        full_fq = full_fq.append(result, ignore_index=True)

    start = start if start is not None else full_fq['DT_COMPTC'].min()
    end = end if end is not None else full_fq['DT_COMPTC'].max()

    full_fq = full_fq[(full_fq['DT_COMPTC']>=start) & (full_fq['DT_COMPTC']<=end)].copy()
         
    return result

def read_registration_funds(active_funds = True,
                            headers = None, 
                            auth = None, 
                            proxy = None,
                            proxy_auth= None,
                            cookies = None,                                       
                            ssl= None,
                            verify_ssl = None) -> DataFrame:

    url = f'http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv'

    request = Request()

    try:                
        _response = request.get([url],
                                 headers = headers, 
                                 auth = auth, 
                                 proxy = proxy,
                                 proxy_auth=proxy_auth,
                                 cookies = cookies,                                       
                                 ssl= ssl,
                                 verify_ssl = verify_ssl)
    except Exception as exception:
        raise TypeError(exception)

    _URL = _response[0][0]
    _STATUS_CODE = _response[0][2]
    _CONTENT_TYPE = _response[0][3]

    if 'text/plain' not in _CONTENT_TYPE and 'text/csv' not in _CONTENT_TYPE:
        raise TypeError(f"Invalid content type ({_CONTENT_TYPE} not in ['text/csv', 'text/plain'])")
        
    elif _STATUS_CODE < 200 or _STATUS_CODE > 299:
        raise TypeError(f"Status code ({_STATUS_CODE})")

    _content = str(_response[0][1], 'ISO-8859-1')

    result = pd.read_csv(StringIO(_content), sep=';', encoding='cp1252')

    if active_funds == True:
        result = result[result['SIT']=='EM FUNCIONAMENTO NORMAL'].copy()

    return result

