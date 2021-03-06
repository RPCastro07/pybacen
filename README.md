<h1>Pybacen</h1>

<h3>This library was developed for economic analysis in the Brazilian scenario (Investments, micro and macroeconomic indicators)</h3>


## Installation

Install using `pip`

``` shell
pip install pybacen
```

## Usage

#### Time Series Bacen
``` python
from pybacen.bacen import time_series # Source: SGS - Sistema Gerenciador de Séries Temporais - v2.1 (Bacen - Banco Central)

# To consult the Bacen code, use it as a parameter when consulting the time series
list_code_bacen = time_series.read_bacen_code(search_text='%CDI%ANUALIZADA%252%', period= 'D', unit= '% a.a.')

list_code_bacen
```
<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>COD_BACEN</th>      <th>NM_SERIE</th>      <th>UNIDADE</th>      <th>PERIODICIDADE</th>      <th>FONTE</th>      <th>ESPECIAL</th>    </tr>  </thead>  <tbody>    <tr>      <th>4015</th>      <td>4389</td>      <td>Taxa de juros - CDI anualizada base 252</td>      <td>% a.a.</td>      <td>D</td>      <td>BCB-Demab</td>      <td>N</td>    </tr>  </tbody></table>

``` python
ts = time_series.read_time_series(bacen_code= 4389, start='2021-11-04', end='2021-11-04', as_index=True)

ts
```
<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>valor</th>    </tr>    <tr>      <th>date</th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th>2021-11-04</th>      <td>7.65</td>    </tr>  </tbody></table>

#### Stock Quote - Yahoo Finance

``` python
from pybacen.yahoo_finance import stocks # Source: Yahoo Finance - Stock Quote

# Ibovespa - 2021-11-05
sq = stocks.read_stock_quote(stock_code='^BVSP', start= '2021-11-05', end= '2021-11-05', as_index= True)

sq
```

<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>open</th>      <th>high</th>      <th>low</th>      <th>close</th>      <th>volume</th>      <th>adjclose</th>    </tr>    <tr>      <th>date</th>      <th></th>      <th></th>      <th></th>      <th></th>      <th></th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th>2021-11-05</th>      <td>103412.0</td>      <td>105555.0</td>      <td>103412.0</td>      <td>104824.0</td>      <td>12595000.0</td>      <td>104824.0</td>    </tr>  </tbody></table>


### Requirements

Using pandas datareader requires the following packages:

-   pandas>=1.0
-   requests>=2.19.0
-   plotly>=5.3.1


### Install latest development version

``` shell
python -m pip install pybacen
```

or

``` shell
git clone https://github.com/RPCastro07/pybacen.git
cd pybacen
python setup.py install
```
