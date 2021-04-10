# Rico project
# Author : Thophile
# Date : 10/10/2021

from log import log
import macro
import speech_recognition
import pyttsx3

reco = speech_recognition.Recognizer()

while True:

    try:

        with speech_recognition.Microphone() as mic:

            reco.adjust_for_ambient_noise(mic, duration=0.2)
            audio = reco.listen(mic)

            text = reco.recognize_google(audio, language='fr')
            text = text.lower()

            macro.parse(text)
            print(text)
            log(text)
            
    except speech_recognition.UnknownValueError:
        reco = speech_recognition.Recognizer()
            