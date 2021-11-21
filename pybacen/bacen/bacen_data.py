from warnings import filterwarnings
import pandas as pd 
import requests
import json
from plotly.graph_objects import Figure, Scatter

#Ajustes
#Endereço padrão:http://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json&dataInicial={dataInicial}&dataFinal={dataFinal}

try:
    pd.options.display.max_rows = 999
    pd.set_option('display.max_colwidth', None)
except:
    pass



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
    
def line_plot(self, dfs: list, title: str, xtitle: str = 'Date', ytitle: str = 'Values', template: str = 'plotly_dark'):
    
    filterwarnings("ignore")
        
    dates = dfs[0][0].index
        
        
    for iteration, i in enumerate(dfs):
            
        df = i[0][i[0].index.isin(dates)].copy()
            
        if iteration == 0:
            fig = Figure(Scatter(
                        x=df.index,
                        y=df['valor'],
                        line = dict(color = i[2]),
                        name = i[1]
                        ))
                
            fig.update_layout(xaxis_rangeslider_visible=False,
                              template = template,
                              yaxis_title = ytitle, 
                              xaxis_title = xtitle,
                              title = title
                             )
                    
        else:
            fig.add_trace(Scatter(
                                  x=df.index,
                                  y=df['valor'],
                                  line = dict(color = i[2]),
                                  name = i[1]
                                )
                        )
        fig.show() 
            

class BacenData:

    def read_bacen_complaints(self, year: int, periodicity: str, period: int) -> pd.core.frame.DataFrame:
        url = f'https://www3.bcb.gov.br/rdrweb/rest/ext/ranking/arquivo?ano={year}&periodicidade={periodicity.upper()}&periodo={period}&tipo=Bancos+e+financeiras'
        
        bc = pd.read_csv(url, sep = ';', encoding='cp1252')
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
        select = f"&$select={select}'" if select is not None else ''
        url = f"https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/IfDataCadastro(AnoMes=@AnoMes)?@AnoMes=202106&$top={limit}{filter}&$orderby=NomeInstituicao%20asc&$format=json{select}"
        response = requests.get(url, headers={'Cache-Control': 'no-cache'})
        json_list = json.loads(response.content)
        ri = pd.DataFrame(json_list['value'])
        return ri
    def read_report_inst(self, year_month: str, type_inst: int, num_report: str, limit: int = 100, filter: str = None, select: str = None) -> pd.core.frame.DataFrame:
    
        filter = f"&$filter={filter}'" if filter is not None else ''
        select = f"&$select={select}'" if select is not None else ''
        url = f"https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/IfDataValores(AnoMes=@AnoMes,TipoInstituicao=@TipoInstituicao,Relatorio=@Relatorio)?@AnoMes={year_month}&@TipoInstituicao={type_inst}&@Relatorio='{num_report}'&$top={limit}{filter}&$format=json{select}"
        resp = requests.get(url, headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
        json_list = json.loads(resp.content)
        rep = pd.DataFrame(json_list['value'])
        return rep
    def read_currency_quote(self, currency: str = 'USD', start: str = None, end: str = None, filter: str = None, select: str = None) -> pd.core.frame.DataFrame:
    
        convert_date = lambda x: f"{x[5:7]}-{x[8:11]}-{x[0:4]}"
        start = convert_date(start)
        end = convert_date(end)
        filter = f"&$filter={filter}'" if filter is not None else ''
        select = f"&$select={select}'" if select is not None else ''
        url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda='{currency}'&@dataInicial='{start}'&@dataFinalCotacao='{end}'&$top=10000{filter}&$format=json{select}"
        resp = requests.get(url)
        resp
        json_list = json.loads(resp.content)
        df = pd.DataFrame(json_list['value'])
        return df
