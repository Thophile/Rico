# Rico project
# Author : Thophile
# Date : 10/10/2021

from log import log
import macro
import speech_recognition as sr
import time

DEBUG = True
r = sr.Recognizer()

# Words that sphinx should listen closely for. 0-1 is the sensitivity
# of the wake word.

source = sr.Microphone()

def callback(recognizer, audio):  # this is called from the background thread

    try:
        speech_as_text = recognizer.recognize_google(audio, language='fr',pfilter=0)
        log(speech_as_text)
        if DEBUG: print(speech_as_text)

        # Look for your "rico" keyword in speech_as_text
        if "rico" in speech_as_text or "Rigaud" or "frigo":
            macro.parse(speech_as_text)

    except sr.UnknownValueError:
        if DEBUG: print("Je n'ai pas compris")


r.listen_in_background(source, callback, phrase_time_limit=6)
while True : time.sleep(0.1)
