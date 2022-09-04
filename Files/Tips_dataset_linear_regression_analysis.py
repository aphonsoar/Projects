import pandas as pd
from scipy.stats import pearsonr
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set_theme(color_codes=True)

tips = sns.load_dataset("tips")
g = sns.lmplot(x="total_bill", y="tip", data=tips)

#%% Correlatation matrix
data_corrMatrix = tips[['total_bill','tip','size']]
corrMatrix = data_corrMatrix.corr()

# Filter the dataframe with correlations greater or smaller than the threshold value: https://stackoverflow.com/questions/17778394/list-highest-correlation-pairs-from-a-large-correlation-matrix-in-pandas
threshold_matrix = 0 #0.5
filteredDf = corrMatrix[((corrMatrix >= threshold_matrix) | (corrMatrix <= -threshold_matrix)) & (corrMatrix !=1.000)]
filteredDf_dropNA = filteredDf.dropna(axis = 0, how = 'all') # Keep just the rows greater than the trheshold
filteredDf_dropNA = filteredDf_dropNA.dropna(axis = 1, how = 'all') # Keep just the columns greater than the trheshold

#%%
# Select which matrix should be used to plot: full, filtered or filtered and drop the columns
matrix_used = filteredDf # corrMatrix / filteredDf
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


#%%
## Analysing the regression parameters

from scipy import stats
# Slope: change of y for a one unit increase in x
# Intercept: the point where the function crosses the y-axis. It means, the start value for y when x is zero.
# R_value: R2
# p_value: p_value of the parameter
# std_error: standard error -> represents the average distance that the observed values fall from the regression line

#%%
# Analysing y = tip
bill_slope, bill_intercept, bill_r_value, bill_p_value, bill_std_err = stats.linregress(tips.total_bill,tips.tip)
print('The mean value of the tip is =', round(tips.tip.mean(),3),'\n',
      'The median value of the bill is =', round(tips.tip.median(),3),'\n',
      'The standard error for tip =', round(bill_std_err,3),'\n',
      'The standard error corresponds to % of the mean =', round(bill_std_err / tips.tip.mean(),3))

#%%
# Analysing y = total_bill
tip_slope, tip_intercept, tip_r_value, tip_p_value, tip_std_err = stats.linregress(tips.tip,tips.total_bill) # y = total_bill
print('The mean value of the bill is =', round(tips.total_bill.mean(),3),'\n',
      'The median value of the bill is =', round(tips.total_bill.median(),3),'\n',
      'The standard error for tip =', round(tip_std_err,3),'\n',
      'The standard error corresponds to % of the mean =', round(tip_std_err / tips.total_bill.mean(),3))

#%%
fig, ax= plt.subplots(1,2, figsize=(figsize, figsize))
sns.histplot(tips, x="total_bill", hue="day", kde=True, ax=ax[0])
sns.histplot(tips, x="tip", hue="day", kde=True, ax=ax[1])
plt.tight_layout()
plt.show()
