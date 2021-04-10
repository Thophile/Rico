## Rico project
# Author : Thophile
# Date : 10/10/2021

import speech_recognition
import pyttsx3

reco = speech_recognition.Recognizer

while True:

    try:

        with speech_recognition.Microphone() as mic:

            reco.adjust_for_ambient_noise(mic, duration=0.2)
            audio = reco.listen(mic)

            text = reco.recognize_google(audio).lower()

            print(f"\"{text}\"")
            
    except speech_recognition.UnknownValueError():

        reco = speech_recognition.Recognizer()
        continue