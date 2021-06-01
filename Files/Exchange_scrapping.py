import pandas as pd
import urllib.request
import bs4 as bs
from datetime import date
# Google sheets
# https://medium.com/analytics-vidhya/how-to-read-and-write-data-to-google-spreadsheet-using-python-ebf54d51a72c

#%%
# Ler página
raw_html = urllib.request.urlopen('https://dourada.com.br/cotacao/')
raw_html = raw_html.read()

# Formatar página e converter em string
article_html = bs.BeautifulSoup(raw_html, 'lxml')
html_str = str(article_html)

# Identificar a cotação da moeda - GBP
GBP_pos = html_str.find('>GBP</div>')
GBP_dia = html_str[GBP_pos+51:GBP_pos+55]

# Identificar a cotação da moeda - EUR
EUR_pos = html_str.find('>EUR</div>')
EUR_dia = html_str[EUR_pos+51:EUR_pos+55]

# Obter data do dia
today = date.today().strftime("%d/%m/%Y")

#%%
try:
    del Tabela
except:
    pass

Tabela = {'Data': today,
          'GBP': GBP_dia,
          'EUR': EUR_dia}

df = pd.DataFrame(Tabela.items())

df = df.T
df.columns = df.iloc[0]
df = df.iloc[1]
df = pd.DataFrame(df).T

#%%
try:
    Cotacoes = pd.read_csv('C:\\Aphonso\\Git\\Cotacoes.csv', sep='|')
    Cotacoes = Cotacoes.append(df)
    pd.DataFrame.to_csv(Cotacoes, sep='|', path_or_buf='C:\\Aphonso\\Git\\Cotacoes.csv', index=False)
except:
    pd.DataFrame.to_csv(df, sep='|', path_or_buf='C:\\Aphonso\\Git\\Cotacoes.csv', index=False)
