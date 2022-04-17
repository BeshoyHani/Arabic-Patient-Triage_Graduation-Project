import os
from threading import Thread
from tkinter import *
from tkinter.ttk import Combobox

from PIL import Image, ImageTk
import speech_recognition as sr
#import VoiceRecognition as VC
#import Keras
import  KeyWordsExtraction
import Descison_Tree
import json
import pandas as pd
import time

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'idyllic-striker-341412-40c520a7335a.json'

def Arabic_Triage (text) :
    text = KeyWordsExtraction.get_english_symptoms(text)
    return Descison_Tree.testing(text)
class Main:
    def __init__(self):
        self.window = Tk()
        self.window.title("Patient Triage")
        self.window.geometry("300x400")
        self.window.eval('tk::PlaceWindow . center')

        # Counter
        self.Minute = StringVar()
        self.Second = StringVar()

        self.Minute.set("00")
        self.Second.set("00")

        self.Minute_entry = Label(width=3, font=("Arial", 18, ""), justify="center", textvariable=self.Minute)
        self.Minute_entry.place(x=105, y=80)

        Label(width=1, font=("Arial", 18, ""), justify="center", text=":").place(x=145, y=80)

        self.Second_entry = Label(width=3, font=("Arial", 18, ""), justify="center", textvariable=self.Second)
        self.Second_entry.place(x=155, y=80)

        # Language

        self.selected_language = StringVar()
        self.selected_language.set("عربي")
        self.language_cb = Combobox(textvariable=self.selected_language, justify="right")
        self.language_cb['values'] = ["عربي", "English"]
        self.language_cb['state'] = 'readonly'
        self.language_cb.pack(fill=X, padx=15, pady=15)

        # Load Icon for record button
        self.file = 'assets/images/mic2.ico'
        self.image = Image.open(self.file)
        self.mic_icon = ImageTk.PhotoImage(self.image.resize((100, 100)))

        # Label for Record Button
        self.btn_lbl = StringVar()
        self.btn_lbl.set("Click to Record")
        Label(textvariable=self.btn_lbl).pack(anchor=CENTER, pady=(100, 20))

        self.sound_btn = Button(self.window, image=self.mic_icon, width=64, height=64, relief=FLAT,
                                command=self.start_triage)
        self.sound_btn["border"] = "0"
        self.sound_btn.pack(anchor=CENTER)

        self.window.mainloop()

    def start_triage(self):
        # Update the Record Button Label
        self.btn_lbl.set("Recording...")
        self.window.update()

        # Record Voice
        mic = sr.Microphone(device_index=1)
        voice_recognizer = sr.Recognizer()

        start_counter = 0
        def record_audio():
            with mic as source:
                print("Say Hi")
                voice_recognizer.adjust_for_ambient_noise(source)
                audio = voice_recognizer.listen(source)
                nonlocal start_counter
                start_counter = 1
                with open('idyllic-striker-341412-40c520a7335a.json', 'r') as data_file:
                    credentials = data_file.read()

                text = voice_recognizer.recognize_google_cloud(audio, language="ar-EG", credentials_json=credentials)
                print("Test\n", text)
                Diagnosis = Arabic_Triage(text);
                print("Triage\n", Diagnosis)

                # Update Record Button Label
                self.btn_lbl.set("Click to Record")

                # if self.selected_language.get() == "English":
                # else:
                #

        def update_counter():
            for i in range(61):
                counter = "" + "0"+str(i) if i < 10 else ""+str(i)
                self.Second.set(counter)
                if i == 60:
                    self.Minute.set("01")
                time.sleep(1)
                if start_counter:
                    break

        t1 = Thread(target=record_audio)
        t2 = Thread(target=update_counter)
        t1.start()
        t2.start()

        print(self.selected_language.get())
        # print(VC.getText(audio))


main = Main()
