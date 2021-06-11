import pandas as pd
from datetime import date
import urllib.request
import bs4 as bs
import re

#%%
# Read and prepare the file:
file_excel = pd.read_excel("C:\\Users\\Aphon\\Desktop\\Lista_CNPJs.xlsx", header=0)

file_excel['CPF/CNPJ'] = [w.replace('.','') for w in file_excel['CPF/CNPJ'].astype(str)]
file_excel['CPF/CNPJ'] = [w.replace('/','') for w in file_excel['CPF/CNPJ'].astype(str)]
file_excel['CPF/CNPJ'] = [w.replace('-','') for w in file_excel['CPF/CNPJ'].astype(str)]

file_excel['Nome_limpo'] = [w.replace(' ','') for w in file_excel['Nome'].astype(str)]
file_excel['Nome_limpo'] = [w.replace('.','') for w in file_excel['Nome'].astype(str)]
file_excel['Nome_limpo'] = [w.replace('/','') for w in file_excel['Nome'].astype(str)]
file_excel['Nome_limpo'] = [w.replace('-','') for w in file_excel['Nome'].astype(str)]

file_excel = file_excel[file_excel['CPF/CNPJ'] != 'nan'] # DropNA
file_excel = file_excel.reset_index()
CNPJs = file_excel['CPF/CNPJ']

#%%
# Dataframe to check if it is MEI:
isMEI = pd.DataFrame(columns=['MEI'])
df_data_CNPJs = pd.DataFrame(columns=['Email', 'Endereco', 'Natureza jurídica', 'Fone consulta'])

i = 0
#%%
for i in range(0, len(CNPJs)):
    print(str(i) + ' - ' + str(file_excel['Nome'][i]))

    # Search for CNPJ's data in public website:
    URL = 'https://cnpjs.rocks/cnpj/' + CNPJs[i]

    raw_html = urllib.request.urlopen(URL)
    raw_html = raw_html.read()

    # Format HTML and convert it in a string
    page_items = bs.BeautifulSoup(raw_html, 'lxml')
    html_str = str(page_items)

    # Email:
    email_value_clean = ''
    string_email_search = r'<li>E-mail:  <strong>'
    len_string_email_search = len(string_email_search)
    email_pos = html_str.find(string_email_search)
    email_value = html_str[email_pos+len_string_email_search:email_pos+50]
    email_value_clean = email_value[0:email_value.find(r'</strong></li>')]
    email_value_clean = email_value[0:email_value.find(r'</')]
    if email_value_clean.find('@') == -1:
        email_value_clean = 'Não encontrado'
    else:
        email_value_clean

    # Endereço
    endereco_value_clean_2 = ''
    string_endereco_search = r'Endereço</strong><ul><li>'
    len_string_endereco_search = len(string_endereco_search)
    endereco_pos = html_str.find(string_endereco_search)
    endereco_value = html_str[endereco_pos+len_string_endereco_search:endereco_pos+1000]
    endereco_value_clean = endereco_value[0:endereco_value.find(r'</strong></li></ul><hr><center><ins class="')]
    endereco_value_clean = endereco_value[0:endereco_value_clean.find(r'</li></ul><hr/><center><ins class=')]

    endereco_value_clean_2 = endereco_value_clean.replace(r' <strong>','')
    endereco_value_clean_2 = endereco_value_clean_2.replace(r' </strong>',' - ')
    endereco_value_clean_2 = endereco_value_clean_2.replace(r'</strong>',' - ')
    endereco_value_clean_2 = endereco_value_clean_2.replace(r'</li><li>',' ')
    endereco_value_clean_2 = endereco_value_clean_2[:-3]

    # Identificar MEI
    natJur_value_clean = ''
    string_natJur_search = r'<li>Natureza Jurídica:  <strong>'
    len_string_natJur_search = len(string_natJur_search)
    natJur_pos = html_str.find(string_natJur_search)
    natJur_value = html_str[natJur_pos+len_string_natJur_search:natJur_pos+1000]
    natJur_value_clean = natJur_value[0:natJur_value.find(r'</strong></li><li>Capital')]

    # Phone:
    phone_value_clean = ''
    string_phone_search = r'<ul><li>Telefone:  <strong>'
    len_string_phone_search = len(string_phone_search)
    phone_pos = html_str.find(string_phone_search)
    if phone_pos == -1:
        phone_value_clean = 'Não encontrado'
    else:
        phone_value = html_str[phone_pos + len_string_phone_search:phone_pos + 100]
        phone_value_clean = phone_value[0:phone_value.find(r'</strong>')]

    # Insert data in dataframe:
    df_data_CNPJs = df_data_CNPJs.append({'Email': email_value_clean, 'Endereco': endereco_value_clean_2, 'Natureza jurídica': natJur_value_clean, 'Fone consulta': phone_value_clean}, ignore_index=True)

    if natJur_value_clean[0:5] == '213-5' and str.isnumeric(file_excel['Nome_limpo'].iloc[i][-11:]) == True: # Check if the "Natureza Jurídica" is "Empresário individual" + Name has CPF in the end (last 11 characters)
        isMEI = isMEI.append({'MEI': 'Sim'}, ignore_index=True)
    else:
        isMEI = isMEI.append({'MEI': 'Não'}, ignore_index=True)

#%%
df_data = pd.merge(left=file_excel[['Nome', 'Tipo da Pessoa', 'Tipo de contato', 'CPF/CNPJ', 'Fone']],
                   right=df_data_CNPJs,
                   how='left',
                   left_index=True,
                   right_index=True)

df_data2 = pd.merge(left=df_data,
                    right=isMEI,
                    how='left',
                    left_index=True,
                    right_index=True)

#%%
output_file = "C:\\Aphonso\\Dados_RFB\\Consulta_Tiffin.csv"
pd.DataFrame.to_csv(df_data2, sep='|', path_or_buf=output_file, index=False, encoding='ANSI')