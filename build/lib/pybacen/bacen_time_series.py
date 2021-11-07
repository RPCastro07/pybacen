import pandas as pd 

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
    
    def read_bacen_code(self, search_text: str) -> pd.core.frame.DataFrame:
        result = pd.read_csv('https://raw.githubusercontent.com/RPCastro07/Bacen_Time_Series_Codes/main/series_bacen_codes.csv', encoding='cp1252')
        
        if search_text is not None:
            if search_text != '':
                for i in list(filter(lambda x: x != '', search_text.split('%'))):
                    if search_text != '':
                        result = result[result['NM_SERIE'].str.upper().str.contains(i.upper())].copy()
                    
        return result
        

