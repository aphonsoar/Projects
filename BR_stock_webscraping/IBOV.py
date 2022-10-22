import pandas as pd
import time
import matplotlib.pyplot as plt
import mplcursors
import numpy as np

plt.style.use('ggplot')
plt.isinteractive()

small_size = 8
medium_size = 10
bigger_size = 12

plt.rc('font', size=small_size)          # controls default text sizes
plt.rc('axes', titlesize=small_size)     # fontsize of the axes title
plt.rc('axes', labelsize=medium_size)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=small_size)    # fontsize of the tick labels
plt.rc('ytick', labelsize=small_size)    # fontsize of the tick labels
plt.rc('legend', fontsize=small_size)    # legend fontsize
plt.rc('figure', titlesize=bigger_size)  # fontsize of the figure title


PAPEL_Analise = input('Selecione o papel para ser analisado: ')
PAPEL_Analise = PAPEL_Analise.upper()
Dias_analise = input('Insira a quantidade de dias para análise (D-X): ')

Media_movel_1 = int(input('Insira a quantidade de dias da 1ª média móvel: '))
Media_movel_2 = int(input('Insira a quantidade de dias da 2ª média móvel: '))


url = 'https://www.fundamentus.com.br/amline/cot_hist.php?papel='
url2 = url+PAPEL_Analise

PAPEL = pd.read_csv(url2, sep=',', skiprows=0)

# path = '~/cot_hist.php?papel=PETR4'
# PAPEL = pd.read_csv(path, sep=',', skiprows=0)

PAPEL = PAPEL.reset_index()
PAPEL = PAPEL.reset_index()
del PAPEL["index"]
PAPEL = PAPEL.sort_values(by='level_0', ascending=False)
del PAPEL["level_0"]
PAPEL.columns = ["Data", "Cotacao_fechamento"]
PAPEL = PAPEL.dropna()

PAPEL = PAPEL.head(int(Dias_analise))
PAPEL = PAPEL.reset_index()
del PAPEL["index"]


for i in range(PAPEL.shape[0]):
    PAPEL["Cotacao_fechamento"].iloc[i] = float(PAPEL["Cotacao_fechamento"].iloc[i].replace(']', ''))
    PAPEL["Data"].iloc[i] = PAPEL["Data"].iloc[i].replace('[', '')
    PAPEL["Data"].iloc[i] = time.strftime('%Y-%m-%d', time.gmtime(int(PAPEL["Data"].iloc[i]) / 1000))
    #print('Arrumei a linha: ' + str(i+1))

PAPEL = PAPEL.sort_values(by='Data', ascending=True)

# Média móvel 1:
for i in range(0,PAPEL.shape[0]-Media_movel_1):
    PAPEL.loc[PAPEL.index[i+Media_movel_1],'MM1 '+ str(Media_movel_1)] = np.round(((PAPEL.iloc[i,1] + PAPEL.iloc[i+1,1] + PAPEL.iloc[i+Media_movel_1,1])/3),2)

# Média móvel 2:
for i in range(0,PAPEL.shape[0]-Media_movel_2):
    PAPEL.loc[PAPEL.index[i+Media_movel_2],'MM2 '+ str(Media_movel_2)] = np.round(((PAPEL.iloc[i,1] + PAPEL.iloc[i+1,1] + PAPEL.iloc[i+Media_movel_2,1])/3),2)

x = PAPEL["Data"]
y = PAPEL["Cotacao_fechamento"]
MM1 = PAPEL["MM1 "+ str(Media_movel_1)]
MM2 = PAPEL["MM2 "+ str(Media_movel_2)]

# Original funcionando:
# fig, ax = plt.subplots()
#
# lines = ax.plot(x, y, color='blue', label='Cotação fechamento') # marker='o', linestyle='--'
# mplcursors.cursor(lines)
#
# lines2 = ax.plot(x, MM1, color='yellow', label='MM1 '+ str(Media_movel_1))
# mplcursors.cursor(lines2)
#
# lines3 = ax.plot(x, MM2, color='red', label='MM2 '+ str(Media_movel_2))
# mplcursors.cursor(lines3)
#
# plt.title('Cotacação do papel ' + str(PAPEL_Analise) + ' nos últimos ' + str(Dias_analise) + ' dias.')
# plt.xlabel('', size=9)
# plt.xticks(size=9, rotation=80)
# #plt.ylabel('Valor de fechamento no dia', size=9)
# plt.yticks(size=9)
# plt.legend()
# ax.axes.get_xaxis().set_visible(False)
# ax.axes.get_yaxis().set_visible(True)
# plt.tight_layout()
# plt.show()

fig, ax = plt.subplots()

lines = ax.plot(x, y, color='blue', label='Cotação fechamento') # marker='o', linestyle='--'
mplcursors.cursor(lines)

lines2 = ax.plot(x, MM1, color='yellow', label='MM1 '+ str(Media_movel_1))
mplcursors.cursor(lines2)

lines3 = ax.plot(x, MM2, color='red', label='MM2 '+ str(Media_movel_2))
mplcursors.cursor(lines3)

plt.title('Cotacação do papel ' + str(PAPEL_Analise) + ' nos últimos ' + str(Dias_analise) + ' dias.')
plt.xlabel('', size=9)
plt.xticks(size=9, rotation=80)
#plt.ylabel('Valor de fechamento no dia', size=9)
plt.yticks(size=9)
plt.legend()
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(True)
plt.tight_layout()
plt.show()

