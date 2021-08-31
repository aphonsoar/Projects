import random
import plotly.express as px
import plotly.io as pio
import pandas as pd
pio.renderers.default = "browser"

list = []
n = 1000
try:
    del r
except:
    pass

for i in range(n):
    r = random.randint(1,10)
    list.append(r)

df = pd.DataFrame(list)
df.columns = ['Values']
df_agg = df.groupby('Values')['Values'].count()
df_agg = pd.DataFrame(df_agg)

fig = px.bar(df_agg, y='Values', x=df_agg.index, text='Values')
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
fig.update_layout(width=1500, height=900)
fig.show()