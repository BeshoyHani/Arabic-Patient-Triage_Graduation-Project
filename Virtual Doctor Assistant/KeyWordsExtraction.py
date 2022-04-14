#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process
import textdistance
import csv
import preprocessing

def get_all_symptoms(path):
    list = []
    with open(path, 'r', encoding='utf8') as rf:
        reader = csv.reader(rf)
        next(reader)
        for row in reader:
            for i in range(1, len(row)) :
                if row[i] != '':
                    list.append(row[i])

    list = preprocessing.preprocess(list)
    print(list)
    return list

all_diseases = get_all_symptoms('GP_ArabicDataSet.csv')

def getHighestSimilarity(word):
    sim = [(textdistance.Prefix().normalized_similarity(candidate, word)) for candidate in all_diseases]
    idx = sim.index(max(sim))
    return sim[idx] , all_diseases[idx]

def extract_diseases(text):
    list = []


    words = text.split()
    words = preprocessing.preprocess(words)

    print(words)
    for i in range(len(words)):
        list.append(getHighestSimilarity(words[i]))

    return list


print(extract_diseases("عندي"))