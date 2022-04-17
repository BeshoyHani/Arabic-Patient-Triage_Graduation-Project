# importing spaCy
import nltk
from seg.newline.segmenter import NewLineSegmenter
import re
import warnings
import spacy
from nltk.stem import WordNetLemmatizer
# nltk.download('wordnet')
# nltk.download('omw-1.4')
nlseg = NewLineSegmenter()

lemmatizer = WordNetLemmatizer()
warnings.filterwarnings("ignore", message=r"\[W008\]", category=UserWarning)
# Loading spaCy large dictionary
nlp = spacy.load('en_core_web_lg')
# nlp.add_pipe(nlseg.set_sent_starts, name='sentence_segmenter', before='parser')
# Taking input from user
print("Type a symptom: ")
words = input()
# Turning it into tokens
# tokens = nlp(words)
# loading Symptoms text file
with open('Symptoms.txt') as f:
	Symptoms_file = f.read().splitlines()

# print(Symptoms_file)
Output = []
word = nlp(words)
split_input = words.split(' ')

set_of_symptoms = set()
for i in range(len(split_input)):
	text = ""
	text = text + split_input[i]
	word1 = nlp(text)
	word2 = nlp(split_input[i])
	for symptom in Symptoms_file:
		symptom = nlp(symptom)
		similarity1 = word1.similarity(symptom)
		similarity2 = word2.similarity(symptom)
		if similarity1 > 0.7:
			set_of_symptoms.add(str(symptom))
		elif similarity2 > 1.0:
			set_of_symptoms.add(str(symptom))

print(set_of_symptoms)

#
# for symptom in Symptoms_file:
# 	symptom = nlp(symptom)
# 	if word.similarity(symptom) > 0.7:
# 		print(str(word)+ " is similar with "+ str(symptom))
# 		print("Similarity:", word.similarity(symptom))
# 		Output.append(str(symptom))
print(Output)