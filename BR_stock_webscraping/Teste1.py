import pandas as pd
from yahooquery import Ticker
from datetime import date
from datetime import timedelta
import datetime
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm


#%%
# Papel:
p = Ticker("ABEV3.SA")

# Período a ser analisado: últimos 30 dias:
Data_final = date.today()
Data_inicial = Data_final + timedelta(days=-30)


# Consultar toda série histórica: p.history(period="max")
# ph = p.history(period="60d")

ph = p.history(start=Data_inicial, end=Data_final + timedelta(days=1))
ph = ph.reset_index().sort_values(by=["date"], ascending=False)
ph = ph[["symbol", "date", "close"]].reset_index()
del ph["index"]
ph = ph.reset_index()

y1 = ph[ph["index"] == 0]
del y1["index"]

y1 = y1.set_index(['symbol','date']).stack()
y1 = pd.DataFrame(y1)
y1 = y1.reset_index()
del y1["level_2"]
y1.columns = ["symbol","date","close"]

y1_2 = ph["close"][(ph["index"] >= 1) & (ph["index"] <= 15)]
y1_2 = pd.DataFrame(y1_2).T
y1_2 = y1_2.reset_index()
del y1_2["index"]
y1_2.columns = ["x1","x2","x3","x4","x5","x6","x7","x8","x9","x10","x11","x12","x13","x14","x15"]
y1_2 = y1_2.reset_index()
del y1_2["index"]

y = pd.merge(left=y1,
             right=y1_2,
             how='inner',
             left_index=True,
             right_index=True)
#%%
fit1 = sm.ols(formula="close ~ x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11+x12+x13+x14+x15", data=y).fit()
print(fit1.summary())

#%%
# Informações financeiras
p_df = p.income_statement()   # Chama função de Demonstração de resultados
p_df = p_df.transpose()       # Transpõe a matriz
p_df.columns = p_df.iloc[0,:] # Renomeia colunas
p_df = p_df.iloc[2:,:-1]      # Seleciona dados
p_df = p_df.iloc[:, ::-1]     # Inverte colunas
p_df