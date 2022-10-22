# Function to remove stopwords from a string
def remove_stopwords_string(string, stopwords):
    string1 = string
    stopwords = stopwords
    string1words = string1.split()

    resultwords = [word for word in string1words if word not in stopwords]
    string1_result = ' '.join(resultwords)

    return (string1_result)