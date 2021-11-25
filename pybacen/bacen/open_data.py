import requests
import pandas as pd
from pandas import DataFrame
import json
from pybacen.utils.requests import Request

def read_bacen_complaints(year: int, periodicity: str, period: int) -> DataFrame:
    url = f'https://www3.bcb.gov.br/rdrweb/rest/ext/ranking/arquivo?ano={year}&periodicidade={periodicity.upper()}&periodo={period}&tipo=Bancos+e+financeiras'
    
    bc = pd.read_csv(url, sep = ';', encoding='cp1252')
    return bc
    
# IF Data - Olinda
def read_list_reports() -> DataFrame:
    
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

def read_currency_quote(currency: str = 'USD', 
                        start: str = None, 
                        end: str = None, 
                        filter: str = None, 
                        select: str = None,
                        headers = None,
                        auth = None,
                        proxies = None, 
                        cert = None, 
                        cookies = None, 
                        hooks = None,
                        stream = None,
                        verify = True) -> pd.core.frame.DataFrame:
   
    convert_date = lambda x: f"{x[5:7]}-{x[8:11]}-{x[0:4]}"
    start = convert_date(start)
    end = convert_date(end)
    filter = f"&$filter={filter}'" if filter is not None else ''
    select = f"&$select={select}'" if select is not None else ''
    url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda='{currency}'&@dataInicial='{start}'&@dataFinalCotacao='{end}'&$top=10000{filter}&$format=json{select}"
    
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


    json_list = json.loads(response.content)
    df = DataFrame(json_list['value'])

    df['dataHoraCotacao'] = df['dataHoraCotacao'].apply(lambda x: x[0:19])
    
    df['dataHoraCotacao'] = pd.to_datetime(df['dataHoraCotacao'], format=('%Y-%m-%d %H:%M:%S'))

    return df
