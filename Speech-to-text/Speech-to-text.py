# References:
# Speech to text:
    # https://towardsdatascience.com/easy-speech-to-text-with-python-3df0d973b426
    # https://pypi.org/project/SpeechRecognition/
    # https://realpython.com/python-speech-recognition/
    # https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
    # https://www.tutorialexample.com/converting-m4a-to-wav-using-pydub-in-python-python-tutorial/
# Similarity metric between two strings
    # Converting m4a to wav using pydub in Python – Python Tutorial - https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings

# pip install SpeechRecognition
import speech_recognition as sr # Library for speech-to-text
from difflib import SequenceMatcher # Library to find the similarity metric between two strings
import pandas as pd

#%%
# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# Directory:
file_folder = 'C:\\Aphonso_C\\Git\\Projects\\Speech-to-text\\'
file = file_folder+'English_test.wav'

language = 'en-GB' #'en-US' --> GB and US had the same accuracy.

#%%
# Reading Audio file as source
# listening the audio file and store in audio_text variable
attempt = 0
attempt_success = 0
attempt_fail = 0
with sr.AudioFile(file) as source:

    while attempt_success == 0:

        audio_text = r.listen(source)
        # recoginize_google() method will throw a request error if the API is unreachable, hence using exception handling
        attempt = attempt+1

        print('This is the attempt number '+str(attempt))

        try:
            # using google speech recognition
            text = r.recognize_google(audio_text, language=language)
            attempt_success = attempt_success+1
            print('Converting audio transcripts into text ...')
            print(text)
        except:
            attempt_fail = attempt_fail + 1
            print('Sorry.. run again...')

print('Process finished.')


#%%
# Adding french langauge option
#text = r.recognize_google(audio_text, language = "fr-FR")
#%%
# Function to compare strings:
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#%%
# Testing audio conversiona accuracy:
text_transcribed_by_me = """Hello everyone my name is aphonso this is a test of speech to text audio recording and I'm doing that to test one python library and basically this is part of my... ah, let's say personal project to test a library a then see how can use this in future products that I've been thinking to develop. basically I'm 32 years old I'm from Brazil and nowadays I live in London and today is, let me check because I forgot today is 19th October of 2022 thank you"""

#%%
# Raw comparison:
accuracy_raw_comparison = similar(text_transcribed_by_me, text)
print(str(round(accuracy_raw_comparison,4) * 100) + ' %')

#%%
# 1st batch of error handling / checking:

## Errors identifyied -> solution to be tested:
# my name -> include stopwords checking
# lowercase -> include ".lower()" on string comparison -> words_normalization
# dashes -> words_normalization
# numers -> words_normalization
# ellipsis -> words_normalization
# commas -> words_normalization
# contractions

## Actual errors: True value / Python recognised error:
## Aphonso / full
## Future / computer
## Let me / like a

#%%
# Improvements:

# 1. Words normalization:

# Defining a function for words normalization.
# Source: https://github.com/aphonsoar/Projects/blob/master/Files/words_normalization.py
import re
import unidecode

def words_normalization(string):
    string = string.lower()  # convert the whole sentence to lowercase
    string = re.sub(r'\W', ' ', string)  # remove all the punctuation
    string = re.sub(r'\s+', ' ', string)  # remove empty spaces
    string = re.sub('(\d)+', '', string)  # remove all numbers from the string
    string = unidecode.unidecode(string)  # remove accents from words

    return string

#%%
# Run the function on the list of words:
text_normalized = words_normalization(text)
text_transcribed_by_me_normalized = words_normalization(text_transcribed_by_me)

#%%
# Normalized comparison:
accuracy_normalized_comparison = similar(text_transcribed_by_me_normalized, text_normalized)
print(str(round(accuracy_normalized_comparison,4) * 100) + ' %')

#%%
# 2. Stopwords:
# import nltk
# nltk.download('stopwords')

stopwords_file = 'C:\\Aphonso_C\\Git\\Projects\\Speech-to-text\\stopwords.txt'
stopwords_nltk_library = 'C:\\Aphonso_C\\Git\\Projects\\Speech-to-text\\stopwords_english_nltk.txt'

stopwords_file_df = pd.read_csv(stopwords_file, header=None)
stopwords_nltk_library_df = pd.read_csv(stopwords_nltk_library, header=None)

stopwords_speech_to_text = pd.concat([stopwords_file_df, stopwords_nltk_library_df])
stopwords_speech_to_text.columns = ['word']
stopwords_speech_to_text = stopwords_speech_to_text['word'].tolist()

#%%
# Stopwords:
# Function to remove stopwords from a string
def remove_stopwords_string(string,stopwords):
    string1 = string
    stopwords = stopwords
    string1words = string1.split()

    resultwords  = [word for word in string1words if word not in stopwords]
    string1_result = ' '.join(resultwords)

    return(string1_result)

#%%
text_normalized_stopwords = remove_stopwords_string(text_normalized, stopwords_speech_to_text)
text_transcribed_by_me_normalized_stopwords = remove_stopwords_string(text_transcribed_by_me_normalized, stopwords_speech_to_text)

accuracy_normalized_stopwords_comparison = similar(text_transcribed_by_me_normalized_stopwords, text_normalized_stopwords)
print(str(round(accuracy_normalized_stopwords_comparison,4) * 100) + ' %')

#%%
# Final results:
print(str(round(accuracy_raw_comparison,4) * 100) + ' %')
print(str(round(accuracy_normalized_comparison,4) * 100) + ' %')
print(str(round(accuracy_normalized_stopwords_comparison,4) * 100) + ' %')
# 1. Raw: 75.22 %
# 2. Normalized: 70.42 %
# 3. Normalized + stopwords: 82.31 %




