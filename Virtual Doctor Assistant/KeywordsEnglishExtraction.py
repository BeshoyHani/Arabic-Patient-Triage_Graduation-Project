# importing spaCy
import nltk
import re
import spacy
from nltk.stem import WordNetLemmatizer
# nltk.download('wordnet')
# nltk.download('omw-1.4')


class EnglishKeywordsExtraction:
	def __init__(self):
		# Loading spaCy large dictionary
		self.nlp = spacy.load('en_core_web_lg')

		# loading Symptoms text file
		with open('symptoms/Symptoms.txt') as f:
			self.Symptoms_file = f.read().splitlines()

	def get_list_of_symptoms(self, text):
		split_input = text.split(' ')
		split_input = [word for word in split_input if word!= "pain"]
		set_of_symptoms = set()
		for i in range(len(split_input)):
			text = ""
			text = text + split_input[i]
			word1 = self.nlp(text)
			word2 = self.nlp(split_input[i])
			for symptom in self.Symptoms_file:
				symptom = self.nlp(symptom)
				similarity1 = word1.similarity(symptom)
				similarity2 = word2.similarity(symptom) if split_input[i] != "pain" else 0
				if similarity1 > 0.75:
					set_of_symptoms.add(str(symptom).replace(' ','_'))
				elif similarity2 > 0.8:
					set_of_symptoms.add(str(symptom).replace(' ','_'))
					print(split_input[i], similarity2)

		print(set_of_symptoms)
		result = [symptom for symptom in set_of_symptoms]
		return result

# key_word = EnglishKeywordsExtraction()
# key_word.get_list_of_symptoms("I have belly pain and itching and itchy and dog")