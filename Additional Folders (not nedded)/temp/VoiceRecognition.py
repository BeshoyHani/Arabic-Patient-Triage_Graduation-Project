import os

from google.cloud import speech
import pandas as pd
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'idyllic-striker-341412-40c520a7335a.json'
speech_client = speech.SpeechClient()


# Example 1 & 2. Transcribe Local Media File
# File Size: < 10mbs, length < 1 minute

disease_to_triage = {}


y = pd.read_csv("prognosis.csv")

for i in range(len(y["old"])):
    disease_to_triage[y["old"][i]] = y["new"][i]

def getText(path):
    with open(path, "rb") as audio_file:
        content = audio_file.read()

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="ar-EG",
       # audio_channel_count=2,
    )

    operation = speech_client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    text = ""
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        text += result.alternatives[0].transcript
        # The first alternative is the most likely one for this portion.
        # print(u"Transcript: {}".format(result.alternatives[0].transcript))
        # print("Confidence: {}".format(result.alternatives[0].confidence))

    return text


import KeyWordsExtraction
import Keras

def Arabic_Triage (text) :
    text = KeyWordsExtraction.get_english_symptoms(text)
    print(text)
    res = Keras.testing(text)
    return disease_to_triage[res[0]]

txt = getText('doc.wav')
print(txt)
print(Arabic_Triage(txt))


