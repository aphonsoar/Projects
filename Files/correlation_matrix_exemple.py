import pandas as pd
from scipy.stats import pearsonr
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Correlation matrix of N variables from a DataFrame
#corr, _ = pearsonr(data1[data1.columns], data1[data1.columns])
#print('Pearsons correlation: %.3f' % corr)

data_corrMatrix = data1[[
               #'Qtde_tickets','Qtde_tickets_impostos','Faturamento', # Count
               'Flag_tickets','Flag_tickets_impostos','Flag_faturamento', # Binária
               'SIMPLES', 'INSS_SIMPLES', 'IRRF', 'INSS_PRESUMIDO', 'COFINS', 'PIS', 'ISS', 'FGTS']]
corrMatrix = data_corrMatrix.corr()

# Filter the dataframe with correlations greater or smaller than the threshold value: https://stackoverflow.com/questions/17778394/list-highest-correlation-pairs-from-a-large-correlation-matrix-in-pandas
threshold_matrix = 0.5
filteredDf = corrMatrix[((corrMatrix >= threshold_matrix) | (corrMatrix <= -threshold_matrix)) & (corrMatrix !=1.000)]
filteredDf_dropNA = filteredDf.dropna(axis = 0, how = 'all') # Keep just the rows greater than the trheshold
filteredDf_dropNA = filteredDf_dropNA.dropna(axis = 1, how = 'all') # Keep just the columns greater than the trheshold

#%%
# Select which matrix should be used to plot: full, filtered or filtered and drop the columns
matrix_used = filteredDf_dropNA # corrMatrix / filteredDf
figsize = 10

# Using just the bottom diagonal from the matrix:
#mask = np.zeros_like(corrMatrix)
#mask[np.triu_indices_from(mask)] = True

# Using just the upper diagonal from the matrix:
mask = np.ones_like(matrix_used)
mask[np.triu_indices_from(arr=mask, k=+1)] = False

# Plotar matriz de correlação:
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(figsize, figsize))
    ax = sns.heatmap(data=matrix_used,
                     annot=True,
                     fmt='.2f',
                     cmap= 'bwr', #'twilight_shifted', # Colormaps: https://matplotlib.org/stable/tutorials/colors/colormaps.html
                     linewidths=0.07,
                     linecolor='lightgray',
                     mask=mask, # o mask oculta a diagonal da figura.
                     vmax=1, vmin=-1,
                     center=0,
                     square = True)
    title='Matriz de correlação'
    f.suptitle(title)
    #ax.set(title='Análise binária: Ter tickets / ter tickets de impostos / ter guias dos impostos')
    plt.xticks(rotation=90)
    plt.tight_layout()
    #plt.savefig('C:\\Aphonso\\BI\\business_intelligence\\data_science\\aphonso\\Engajamento\\Contact_rate_impostos_mai21\\'+
    #            title + '_binaria_'+periodo_analise_tickets+'.png')
    plt.show()
    # Gif maker: https://ezgif.com/maker

#Dataset_analise.to_clipboard()