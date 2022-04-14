import nltk as nltk
from nltk.stem.isri import ISRIStemmer

egyption_stop_words = ['عندي', 'شويه', 'عندها', 'مش', 'حبه', 'جايز', 'باين', 'اوي', 'جدا']

def stemming(word_tokens):
    st = ISRIStemmer()
    filtered_sentence = [st.stem(w) for w in word_tokens]
    return filtered_sentence


def generalize_similar_chars(word):
    word.replace('ة', 'ه')
    word.replace('ى', 'ي')
    return word


def preprocess(data):
    data_without_stop_words = remove_stop_words(data)
    stemmed_data = stemming(data_without_stop_words)
    return stemmed_data


def remove_stop_words(word_tokens):
   # nltk.download("stopwords")
    arb_stopwords = nltk.corpus.stopwords.words("arabic")

    for x in egyption_stop_words:
        arb_stopwords.append(x)
    for i in range(0, len(arb_stopwords)):
        arb_stopwords[i] = generalize_similar_chars(arb_stopwords[i])
    arb_stopwords = set(arb_stopwords)
    filtered_sentence = [w for w in word_tokens if not w.lower() in arb_stopwords]
    return filtered_sentence
