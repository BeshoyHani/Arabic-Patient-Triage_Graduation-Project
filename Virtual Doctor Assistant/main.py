import os
import pandas as pd
import speech_recognition as sr
import KeyWordsExtraction
from KeywordsEnglishExtraction import EnglishKeywordsExtraction
import Descison_Tree
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import eel


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'idyllic-striker-341412-40c520a7335a.json'


class Main:
    def __init__(self):
        prognosis= pd.read_csv("prognosis.csv")
        self.clinics = {}
        for index, row in prognosis.iterrows():
            self.clinics[row[1]] = row[2]

        # User Info
        self.patient_name=""
        self.patient_age = 0
        self.patient_gender = "male"
        self.arabic_questions = ['ذكر ولا أنثي', 'اسمك ايه؟' , 'عندك كام سنة؟', 'ايه الاعراض اللي عندك؟']
        self.english_questions = ['Male or Female?', "What is your name?", "How old are you?", 'What are the symptoms do you feel?']

        # Language
        self.selected_language = 'ar-EG'

    def set_langage(self, lang):
        self.selected_language = lang
    def set_patient_info(self):
        questions = self.arabic_questions if self.selected_language == 'ar-EG' else self.english_questions

        # Gender
        self.play_sound(self.selected_language[:2], questions[0])
        self.patient_gender = self.convert_voice_to_text(self.selected_language)

        # Name
        self.play_sound(self.selected_language[:2], questions[1])
        self.patient_name = self.convert_voice_to_text(self.selected_language)

        # Age
        self.play_sound(self.selected_language[:2], questions[2])
        self.patient_age = self.convert_voice_to_text(self.selected_language)

        print(self.patient_name)
        print(self.patient_gender)
        print(self.patient_age)

    def start_triage(self):
        # Update the Record Button Label

        if self.selected_language != "English":
            self.play_sound(self.selected_language[:2], self.arabic_questions[3])
            text = self.convert_voice_to_text("ar-EG")
            Diagnosis = self.Arabic_Triage(text)
            print("Triage\n", Diagnosis)
            clinic= self.clinics.get(''.join(Diagnosis))
            print("clinic ", clinic)
            translated_text = self.Translate_to_Arabic(clinic)
            self.play_sound("ar", "يجب عليك التوجه إلىَ عيادة " + translated_text)
        else:
            self.play_sound(self.selected_language[:2], self.english_questions[3])
            text = self.convert_voice_to_text("en-US")
            Diagnosis = self.English_Triage(text)
            clinic = self.clinics.get(''.join(Diagnosis))
            self.play_sound("en", "You Should go to the " + clinic + " clinic")
            print(text)

        # print(VC.getText(audio))

    def convert_voice_to_text(self, lang):
        # Record Voice
        mic = sr.Microphone(device_index=1)
        voice_recognizer = sr.Recognizer()
        with mic as source:
            print("Say Hi")
            voice_recognizer.adjust_for_ambient_noise(source)
            audio = voice_recognizer.listen(source)
            with open('idyllic-striker-341412-40c520a7335a.json', 'r') as data_file:
                credentials = data_file.read()

            text = voice_recognizer.recognize_google(audio, language=lang)#, credentials_json=credentials)
            return text

    def Arabic_Triage(self, text):
        text = KeyWordsExtraction.get_english_symptoms(text)
        return Descison_Tree.testing(text)

    def English_Triage(self, text):
        KE = EnglishKeywordsExtraction()
        text = KE.get_list_of_symptoms(text)
        return Descison_Tree.testing(text)

    def Translate_to_Arabic(self, text):
        translator = Translator()
        text = translator.translate(text, dest="ar", src="en")
        return text.text

    def play_sound(self, lang, text):
        text = ''.join(text)
        print(text)
        obj = gTTS(text=text, lang=lang, slow=False)
        obj.save("voice.mp3")
        playsound("voice.mp3")
        os.remove("voice.mp3")


main = Main()

# Define EEL for link python with frontend
eel.init('web_interface')

@eel.expose
def triage():
    main.set_patient_info()
    main.start_triage()
    eel.hide_voice_animation()()

@eel.expose
def set_language():
    eel.get_language()(main.set_langage)


eel.start('index.html')