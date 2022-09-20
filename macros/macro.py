import pyttsx3 as tts
import json
import random
from break_exception import *

class Macro:
    data = None
    binding = None

    def __init__(self, path):
        with open(path ,encoding='utf-8') as f:
            self.data = json.load(f)
        self.binding["start"] = self.start
        self.binding["stop"] = self.stop
        self.binding["unknown"] = self.unknown


    # Intents
    def match_intent(self, txt="",intent=""):
        match = False
        for k in self.data[intent]["keywords"]:
            if k in txt.lower():
                match = True
        return match  


    def find_intent(self, txt=""):
        for intent in self.data:
            for k in self.data[intent]["keywords"]:
                if k in txt.lower():
                    return intent

    def get_parameters(self, txt="", intent=""):
        for k in self.data[intent]["keywords"]:
            if k in txt.lower() :
                txt = txt.lower().replace(k,"")
                break
        return txt

    def pick_response(self, intent=""):
        lim = len(self.data[intent]["response"])
        return self.data[intent]["response"][random.randint(0, lim - 1)]

    def speak(self, txts):
        speaker = tts.init()
        speaker.setProperty('rate', 200)
        voice = speaker.getProperty('voices')[0] # the french voice
        speaker.setProperty('voice', voice.id)

        for txt in txts:
            speaker.say(txt)
        speaker.runAndWait()

    def start(self, parameter=""):
            self.speak([self.pick_response("start")])

    def stop(self, parameter=""):
        self.speak([self.pick_response("stop")])
        raise BreakException()

    def unknown(self, parameter=""):
        self.speak([self.pick_response("unknown")])
