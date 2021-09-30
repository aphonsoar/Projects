#%% Function to normalize words for text mining:

# List to test:
#list = ['é DHUEHD ÉÉÉ ´I ´U )(', 'TESTE123', 'ççÇÇ       ..., , . \ 88 jioasjdioajs TESTE123']

import re
import unidecode

def words_normalization(list_of_strings):
    for i in range(len(list_of_strings)):
        list_of_strings[i] = list_of_strings[i].lower()  # convert the whole sentence to lowercase
        list_of_strings[i] = re.sub(r'\W', ' ', list_of_strings[i])  # remove all the punctuation
        list_of_strings[i] = re.sub(r'\s+', ' ', list_of_strings[i])  # remove empty spaces
        list_of_strings[i] = re.sub('(\d)+', '', list_of_strings[i])  # remove all numbers from the string
        list_of_strings[i] = unidecode.unidecode(list_of_strings[i])  # remove accents from words

    return list_of_strings

# Run the function on the list of words:
list_normalized = words_normalization(list)

#print(['é DHUEHD ÉÉÉ ´I ´U )(', 'TESTE123', 'ççÇÇ       ..., , . \ 88 jioasjdioajs TESTE123'])
#print(list_normalized)