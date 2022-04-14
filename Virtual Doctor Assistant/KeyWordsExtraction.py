from fuzzywuzzy import process
import textdistance
import csv
import preprocessing


def get_all_symptoms(path):
    list = []
    with open(path, 'r', encoding='utf8') as rf:
        reader = csv.reader(rf)
        next(reader)
        for row in reader:
            for i in range(1, len(row)):
                if row[i] != '':
                    list.append(row[i])
    return list


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


all_symptoms = get_all_symptoms('GP_ArabicDataSet.csv')
all_symptoms = preprocessing.preprocess(all_symptoms)


def getHighestSimilarity(word):
    #sim = [(textdistance.Jaccard().normalized_similarity(candidate, word)) for candidate in all_symptoms]
    #idx = sim.index(max(sim))
    #return sim[idx], all_symptoms[idx]
    highest = process.extractOne(word,all_symptoms)
    return highest
# def calc_Highest_similarity (symptom , text) :


def extract_diseases(text):
    list = []

    words = text.split()
    words = preprocessing.preprocess(words)
    words = merge_symptoms(words, 3)

    print(words)
    for i in range(len(words)):
        sim = getHighestSimilarity(words[i])
        if sim[1] > 90:
            list.append(sim)

    return list


#print(textdistance.Jaccard(qval=1).normalized_similarity("كحة", "حكة"))
print(extract_diseases("جلدى طفح"))
print(extract_diseases("طفح جلدى"))

