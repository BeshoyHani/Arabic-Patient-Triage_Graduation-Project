import nltk as nltk
from nltk.stem.isri import ISRIStemmer

egyption_stop_words = ['عندي', 'شويه', 'عندها', 'مش', 'حبه', 'جايز', 'باين', 'اوي', 'جدا']

def stemming_helper (text):
    text = text.split()
    st = ISRIStemmer()
    text = [st.stem(w) for w in text]
    text = " ".join(text)

    return text



def stemming(word_tokens):
    filtered_sentence = [stemming_helper(w) for w in word_tokens]
    return filtered_sentence


def generalize_similar_chars(word):
    word = word.replace('ة', 'ه')
    word = word.replace('ى', 'ي')
    return word


def preprocess(data):
    for i in range(0, len(data)):
        data[i] = generalize_similar_chars(data[i])
    data_without_stop_words = remove_stop_words(data)
    stemmed_data = stemming(data_without_stop_words)
    return stemmed_data

def remove_stop_words_helper(text):
    text = text.split()
    arb_stopwords = nltk.corpus.stopwords.words("arabic")
    for x in egyption_stop_words:
        arb_stopwords.append(x)
    arb_stopwords = [generalize_similar_chars(w) for w in arb_stopwords]
    arb_stopwords = set(arb_stopwords)

    text = [w for w in text if not (w in arb_stopwords)]
    text = " ".join(text)
    return text


def remove_stop_words(word_tokens):
   # nltk.download("stopwords")

    filtered_sentence = [remove_stop_words_helper(w) for w in word_tokens]
    filtered_sentence = list(filter(None, filtered_sentence))
    return filtered_sentence
