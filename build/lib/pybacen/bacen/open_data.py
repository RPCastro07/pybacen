import requests
import pandas as pd
from pandas import DataFrame
import json
from io import StringIO
from pybacen.utils.requests import Request
from pybacen.utils.validators import (date_validator, 
                                      compare_dates,
                                      to_date,
                                      sysdate)

def read_bacen_complaints(year: int, 
                          periodicity: str,
                          period: int,
                          headers = None, 
                          auth = None, 
                          proxy = None,
                          proxy_auth= None,
                          cookies = None,                                       
                          ssl= None,
                          verify_ssl = None) -> DataFrame:
                          
    url = f'https://www3.bcb.gov.br/rdrweb/rest/ext/ranking/arquivo?ano={year}&periodicidade={periodicity.upper()}&periodo={period}&tipo=Bancos+e+financeiras'
    
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

    _content = str(_response[0][1], 'ISO-8859-1')
    _URL = _response[0][0]
    _STATUS_CODE = _response[0][2]
    _CONTENT_TYPE = _response[0][3]

    if 'application/octet-stream' not in _CONTENT_TYPE and 'text/csv' not in _CONTENT_TYPE:
        raise TypeError(f"Invalid content type ({_CONTENT_TYPE} not in ['text/csv', 'text/plain'])")
        
    elif 200 >= _STATUS_CODE >= 299:
        raise TypeError(f"Status code ({_STATUS_CODE})")

    result = pd.read_csv(StringIO(_content), sep=';', encoding='cp1252')

    result = result.rename(columns={'Ano': 'ANO', 
                                    'Trimestre': 'TRIMESTRE', 
                                    'Categoria': 'CATEGORIA', 
                                    'Tipo': 'TIPO', 
                                    'CNPJ IF': 'CNPJ_IF',
                                    'Instituição financeira': 'INST_FINAN', 
                                    'Índice': 'INDICE',
                                    'Quantidade de reclamações reguladas procedentes': 'QTD_RECL_REG_PROCEDENTES',
                                    'Quantidade de reclamações reguladas - outras': 'QTD_RECL_REG_OUTRAS',
                                    'Quantidade de reclamações não reguladas': 'QTD_RECL_NAO_REG',
                                    'Quantidade total de reclamações': 'QTD_TOTAL_RECL',
                                    'Quantidade total de clientes  CCS e SCR': 'QTD_TOTAL_CLI_CCS_SCR',
                                    'Quantidade de clientes  CCS': 'QTD_CLI_CCS', 
                                    'Quantidade de clientes  SCR': 'QTD_CLI_SCR'})

    try:
        del result['Unnamed: 14']
    except:
        pass
    
    return result
    
# IF Data - Olinda
"""def read_list_reports() -> DataFrame:
    
    url = 'https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/ListaDeRelatorio()?%24format=json'
    
    response = requests.get(url)
    response = json.loads(response.content)
    lr = DataFrame(response['value'])
    return lr

def important_link_olinda() -> any:
    print('Documentation: https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/documentacao')
    print('Filters: https://olinda.bcb.gov.br/olinda/servico/ajuda')
    print('Site IF.data: https://www3.bcb.gov.br/ifdata/')

def read_registration_inst(limit: int = 100, filter: str = None, select: str = None) -> DataFrame:
    filter = f"&$filter={filter}'" if filter is not None else ''
    select = f"&$select={select}'" if select is not None else ''
    url = f"https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/IfDataCadastro(AnoMes=@AnoMes)?@AnoMes=202106&$top={limit}{filter}&$orderby=NomeInstituicao%20asc&$format=json{select}"
    response = requests.get(url, headers={'Cache-Control': 'no-cache'})
    json_list = json.loads(response.content)
    ri = DataFrame(json_list['value'])
    return ri

def read_report_inst(year_month: str, type_inst: int, num_report: str, limit: int = 100, filter: str = None, select: str = None) -> pd.core.frame.DataFrame:
   
    filter = f"&$filter={filter}'" if filter is not None else ''
    select = f"&$select={select}'" if select is not None else ''
    url = f"https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/IfDataValores(AnoMes=@AnoMes,TipoInstituicao=@TipoInstituicao,Relatorio=@Relatorio)?@AnoMes={year_month}&@TipoInstituicao={type_inst}&@Relatorio='{num_report}'&$top={limit}{filter}&$format=json{select}"
    resp = requests.get(url, headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
    json_list = json.loads(resp.content)
    rep = DataFrame(json_list['value'])
    return rep
"""
def read_currency_quote(currency: str = 'USD', 
                        start: str = None, 
                        end: str = None,
                        type: str = None,
                        filter: str = None, 
                        select: str = None,
                        headers = None, 
                        auth = None, 
                        proxy = None,
                        proxy_auth= None,
                        cookies = None,                                       
                        ssl= None,
                        verify_ssl = None) -> DataFrame:
   
    convert_date = lambda x: f"{x[5:7]}-{x[8:11]}-{x[0:4]}"

    _DATE_FORMAT = '%Y-%m-%d'
    _CONVERT_FORMAT = '%d/%m/%Y'

    if start is not None:
        _start = date_validator(start, format = _DATE_FORMAT, format_converter = _CONVERT_FORMAT)
    else:
        raise AttributeError("Attribute 'start' not declared")
    
    if end is not None:
        _end = date_validator(end, format = _DATE_FORMAT, format_converter = _CONVERT_FORMAT)
    else:
        raise AttributeError("Attribute 'end' not declared")
    
    filter = f"&$filter={filter}'" if filter is not None else ''
    select = f"&$select={select}'" if select is not None else ''

    url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda='{currency}'&@dataInicial='{_start}'&@dataFinalCotacao='{_end}'&$top=10000{filter}&$format=json{select}"
    
    request = Request()

    try:                
        _responses = request.get([url],
                                 headers = headers, 
                                 auth = auth, 
                                 proxy = proxy,
                                 proxy_auth=proxy_auth,
                                 cookies = cookies,                                       
                                 ssl= ssl,
                                 verify_ssl = verify_ssl)
    except Exception as exception:
        raise TypeError(exception)

    _content = json.loads(_responses[0][1])['value']
    
    _URL = _responses[0][0]
    _STATUS_CODE = _responses[0][2]
    _CONTENT_TYPE = _responses[0][3]

    if 'application/json' not in _CONTENT_TYPE:
        raise TypeError(f"Invalid content type ({_CONTENT_TYPE} not equals 'application/json')")
        
    elif 200 >= _STATUS_CODE >= 299:
        raise TypeError(f"Status code ({_STATUS_CODE})")

    ct = pd.DataFrame(_content)

    ct['dataHoraCotacao'] = ct['dataHoraCotacao'].apply(lambda x: x[0:19])
    
    ct['dataHoraCotacao'] = pd.to_datetime(ct['dataHoraCotacao'], format=('%Y-%m-%d %H:%M:%S'))

    if type is not None:
        if type == 'intermediary':
            ct = ct[ct['tipoBoletim']=='Intermediário']
        elif type == 'open':
            ct = ct[ct['tipoBoletim']=='Abertura']
        elif type == 'close':
            ct = ct[ct['tipoBoletim']=='Fechamento']
        else:
            raise AttributeError("type not in ('intermediary', 'open', 'close')")

    ct = ct.rename(columns={
                    'paridadeCompra': 'paridade_compra',
                    'paridadeVenda': 'paridade_venda',
                    'cotacaoCompra': 'cotacao_compra',
                    'cotacaoVenda': 'cotacao_venda',
                    'dataHoraCotacao': 'data_hora_cotacao',
                    'tipoBoletim': 'tipo_boletim'
                    })

    return ct


reclamacoes = read_bacen_complaints(year=2021, periodicity='TRIMESTRAL', period=2)

reclamacoes

reclamacoes.columns




