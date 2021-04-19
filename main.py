# Rico project
# Author : Thophile
# Date : 10/10/2021

# External
import speech_recognition as sr
import pyttsx3 as tts
import time

# File import
from mint import *

from log import log

# Env const
DEBUG = True

# Init
r = sr.Recognizer()
mic = sr.Microphone()

def listen(bool):
    global r
    done = False

    while not done or bool:
        with sr.Microphone() as mic :

            try:
                audio = r.listen(mic, timeout=3, phrase_time_limit=5)


                txt = r.recognize_google(audio, language='fr-FR')
                print(txt)

                if match_intent(txt,"start"):
                    txt = get_parameters(txt,"start")

                    # Find function to call from text
                    intent = find_intent(txt)
                    print(f"intent : {intent}")
                    binding[intent](get_parameters(txt, intent))
                    done = True

            except sr.WaitTimeoutError:
                if DEBUG : print("timeout")
                pass
            except sr.UnknownValueError:
                r = sr.Recognizer()
            except KeyError:
                binding["unknown"]()

listen(True)
