import os
from tkinter import *
from PIL import Image, ImageTk
import speech_recognition as sr
import VoiceRecognition as VC


class Main:
    def __init__(self):
        self.window = Tk()
        self.window.title("Patient Triage")
        self.window.geometry("300x400")
        self.window.eval('tk::PlaceWindow . center')

        # Load Icon for record button
        self.file = './assets/images/mic2.ico'
        self.image = Image.open(self.file)
        self.mic_icon = ImageTk.PhotoImage(self.image.resize((100, 100)))

        # Label for Record Button
        self.btn_lbl = StringVar()
        self.btn_lbl.set("Click to Record")
        Label(textvariable=self.btn_lbl).pack(anchor=CENTER, pady=(100, 20))

        self.sound_btn = Button(self.window, image=self.mic_icon, width=64, height=64, relief=FLAT,
                                command=self.record_audio)
        self.sound_btn["border"] = "0"
        self.sound_btn.pack(anchor=CENTER)

        self.window.mainloop()

    def record_audio(self):
        # Update the Record Button Label
        self.btn_lbl.set("Recording...")
        self.window.update()

        # Record Voice
        mic = sr.Microphone(device_index=1)
        voice_recognizer = sr.Recognizer()

        with mic as source:
            print("Say Hi")
            voice_recognizer.adjust_for_ambient_noise(source)
            audio = voice_recognizer.listen(source)

        print(voice_recognizer.recognize_google(audio, language="ar-EG"))
        # print(VC.getText(audio))

        # Update Record Button Label
        self.btn_lbl.set("Click to Record")


main = Main()
