import json
import random

import re
import webbrowser
import pyttsx3 as tts
import httplib2

speaker = tts.init()
speaker.setProperty('rate', 210)
voice = speaker.getProperty('voices')[0] # the french voice
speaker.setProperty('voice', voice.id)



with open('intents.json',encoding='utf-8') as f:
    data = json.load(f)

# Intents

def match_intent(txt="",intent=""):
    match = False
    for k in data[intent]["keywords"]:
        if k in txt.lower():
            match = True
    return match  


def find_intent(txt=""):
    for intent in data:
        for k in data[intent]["keywords"]:
            if k in txt.lower():
                return intent

def get_parameters(txt="", intent=""):
    for k in data[intent]["keywords"]:
        if k in txt.lower() :
            txt = txt.lower().replace(k,"")
            break
    return txt

def pick_response(intent=""):
    lim = len(data[intent]["response"])
    return data[intent]["response"][random.randint(0, lim - 1)]


# Macro

def start():
    speaker.say(pick_response("start"))
    speaker.runAndWait()

def unknown():
    speaker.say(pick_response("unknown"))
    speaker.runAndWait()

def navigate(parameter=""):
    speaker.say(pick_response("navigate"))
    speaker.runAndWait()
    parameter = parameter.replace(' ','')


    domain = ["",".fr",".com"]
    h = httplib2.Http(timeout=3)
    found = False
    for d in domain:
        
        if d in parameter and d != "":
            continue
        try:
            print(f"trying : https://www.{parameter}{d}")
            url = f"http://www.{parameter}{d}"
            resp = h.request(url, 'HEAD')

            print(resp[0]['status'])
            if int(resp[0]['status']) < 400 :
                webbrowser.open(url)
                found = True
                break
        except Exception:
            continue

    if not found : webbrowser.open('https://www.google.com/search?client=firefox-b-d&q=' + parameter)

def run():

    speaker.say(pick_response("run"))
    speaker.runAndWait()


binding = {"start": start,"unknown": unknown, "navigate": navigate}
