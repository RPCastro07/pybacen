import pandas as pd 
import requests
import json

try:
    pd.options.display.max_rows = 999
    pd.set_option('display.max_colwidth', None)
except:
    pass

class Bacen_time_series:

    def read_time_series(self, bacen_code: int, start: str = None, end: str = None, as_index: bool = True) -> pd.core.frame.DataFrame:
        url = f'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{str(bacen_code)}/dados?formato=json'
        ts = pd.read_json(url)
        ts['date'] = pd.to_datetime(ts['data'], dayfirst=True)
        
        start = start if start is not None else ts['date'].min()
        end = end if end is not None else ts['date'].max()

        ts = ts[(ts['date']>=start) & (ts['date']<=end)].copy()
         
        if as_index == True:
            ts.set_index('date', inplace=True)
            ts.drop('data', inplace=True, axis=1)
        else:
            pass
        
        return ts
    
    def read_bacen_code(self, search_text: str, period: str = None, unit: str = None) -> pd.core.frame.DataFrame:
        result = pd.read_csv('https://raw.githubusercontent.com/RPCastro07/Bacen_Time_Series_Codes/main/series_bacen_codes.csv', encoding='cp1252')
        
        if search_text is not None:
            if search_text != '':
                for i in list(filter(lambda x: x != '', search_text.split('%'))):
                    if search_text != '':
                        result = result[result['NM_SERIE'].str.upper().str.contains(i.upper())].copy()

        if period != None and period != '':
            result = result[result['PERIODICIDADE'].str.strip().str.upper()==period.upper().strip()]
        
        if unit != None and unit != '':
            result = result[result['UNIDADE'].str.strip().str.upper()==unit.upper().strip()]

        return result
        

class Bacen_data:

    def read_bacen_complaints(self, year: int, periodicity: str, period: int) -> pd.core.frame.DataFrame:
        url = f'https://www3.bcb.gov.br/rdrweb/rest/ext/ranking/arquivo?ano={year}&periodicidade={periodicity.upper()}&periodo={period}&tipo=Bancos+e+financeiras'
        
        bc = pd.read_csv(url, sep=';', encoding='cp1252')

        return bc

    # IF Data - Olinda
    def read_list_reports(self) -> pd.core.frame.DataFrame:
        
        url = 'https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/ListaDeRelatorio()?%24format=json'
        
        response = requests.get(url)

        response = json.loads(response.content)

        lr = pd.DataFrame(response['value'])

        return lr

    def important_link_olinda(self):
        print('Documentation: https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/documentacao')
        print('Filters: https://olinda.bcb.gov.br/olinda/servico/ajuda')
        print('Site IF.data: https://www3.bcb.gov.br/ifdata/')

    def read_registration_inst(self, limit: int = 100, filter: str = None, select: str = None) -> pd.core.frame.DataFrame:

        
        filter = f"&$filter={filter}'" if filter is not None else ''
        select = f"&$select={select}'" if filter is not None else ''

        url = f"https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/IfDataCadastro(AnoMes=@AnoMes)?@AnoMes=202106&$top={limit}{filter}&$orderby=NomeInstituicao%20asc&$format=json{select}"
        response = requests.get(url, headers={'Cache-Control': 'no-cache'})

        json_list = json.loads(response.content)

        ri = pd.DataFrame(json_list['value'])

        return ri

    def read_report_inst(self, year_month: str, type_inst: int, num_report: str, limit: int = 100, filter: str = None, select: str = None) -> pd.core.frame.DataFrame:
       

        filter = f"&$filter={filter}'" if filter is not None else ''
        select = f"&$select={select}'" if filter is not None else ''

        url = f"https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/IfDataValores(AnoMes=@AnoMes,TipoInstituicao=@TipoInstituicao,Relatorio=@Relatorio)?@AnoMes={year_month}&@TipoInstituicao={type_inst}&@Relatorio='{num_report}'&$top={limit}{filter}&$format=json{select}"

        resp = requests.get(url, headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})

        json_list = json.loads(resp.content)

        rep = pd.DataFrame(json_list['value'])

        return rep

