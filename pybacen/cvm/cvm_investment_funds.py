
import pandas as pd 

try:
    pd.options.display.max_rows = 999
    pd.set_option('display.max_colwidth', None)
except:
    pass

class Investment_funds:

    def read_funds_quote(self, start: str = None, end: str = None) -> pd.core.frame.DataFrame:

        date_ranges = pd.date_range(start[0:7], end[0:7], freq='MS')

        full_fq = pd.DataFrame()

        for _date in date_ranges:
            url = f'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{_date.year}{_date.month}.csv'
            fq = pd.read_csv(url, sep=';')
            fq['DT_COMPTC'] = pd.to_datetime(fq['DT_COMPTC'], format=('%Y-%m-%d'))

            full_fq = pd.concat([full_fq, fq], ignore_index=True)
        
        start = start if start is not None else full_fq['DT_COMPTC'].min()
        end = end if end is not None else full_fq['DT_COMPTC'].max()

        full_fq = full_fq[(full_fq['DT_COMPTC']>=start) & (full_fq['DT_COMPTC']<=end)].copy()
         
        #if as_index == True:
        #    full_fq.set_index('DT_COMPTC', inplace=True)
        #else:
        #    pass
        
        return full_fq