from fuzzywuzzy import process
#import textdistance
import csv
import preprocessing


arabic_to_english = {}


def get_all_symptoms(path):
    list = []
    with open(path, 'r', encoding='utf8') as rf:
        reader = csv.reader(rf)
        next(reader)
        for row in reader:
            for i in range(1, len(row)):
                if row[i] != '':
                    sym = preprocessing.preprocess([row[i]])[0]
                    list.append(sym)
                    arabic_to_english[sym] = row[0].replace(' ', '_')
    return list


all_symptoms = get_all_symptoms('GP_ArabicDataSet.csv')


def get_english_symptoms(text):
    english_symptoms = []
    arabic_symptoms = get_arabic_symptoms(text)
    for x in arabic_symptoms:
        if arabic_to_english[x] not in english_symptoms :
            english_symptoms.append(arabic_to_english[x])
    return arabic_symptoms, english_symptoms


def merge_symptoms(words, length):
    if not (type(words) is list):
        words = words.split()

    List = []
    for i in range(len(words)):
        str = ""
        for j in range(i, min(i + length, len(words))):
            str += words[j]
            List.append(str)
            str += " "
    return List


def getHighestSimilarity(word):
    #sim = [(textdistance.Jaccard().normalized_similarity(candidate, word)) for candidate in all_symptoms]
    #idx = sim.index(max(sim))
    #return sim[idx], all_symptoms[idx]
    highest = process.extractOne(word,all_symptoms)
    return highest


def get_arabic_symptoms(text):
    list = []

    words = text.split()
    words = preprocessing.preprocess(words)
    words = merge_symptoms(words, 3)
    #print(words)
    for i in range(len(words)):
        sim = getHighestSimilarity(words[i])
        print(words[i] , sim)
        if sim[1] > 90 and sim[0] not in list:
            #print(sim ,words[i])
            list.append(sim[0])

    return list

