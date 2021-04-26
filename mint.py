import json
import random
import winapps
import re
import webbrowser
import pyttsx3 as tts
import httplib2
import threading
import os,fnmatch
import subprocess
from log import log


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

class BreakException(BaseException): # Exception raised when a method need the listen thread to stop
        pass
def start(parameter=""):
    speak([pick_response("start")])

def unknown(parameter=""):
    speak([pick_response("unknown")])

def stop(parameter=""):
    speak([pick_response("stop")])
    raise BreakException()

def search(parameter=""):
    speak([pick_response("search")])
    webbrowser.open('https://www.google.com/search?client=firefox-b-d&q=' + parameter)
    
def navigate(parameter=""):
    speak([pick_response("navigate")])
    parameter = parameter.replace(' ','')


    domain = ["",".fr",".com"]
    h = httplib2.Http(timeout=3)
    found = False
    for d in domain:
        if d in parameter and d != "":
            continue
        try:
            log(f"trying : https://www.{parameter}{d}")
            url = f"http://www.{parameter}{d}"
            resp = h.request(url, 'HEAD')

            log(resp[0]['status'])
            if int(resp[0]['status']) < 400 :
                webbrowser.open(url)
                found = True
                break
        except Exception as e:
            log(e)

    if not found : webbrowser.open('https://www.google.com/search?client=firefox-b-d&q=' + parameter)

def run(parameter=""):
    speak([pick_response("run")])
    parameter = parameter.replace(' ','')

    # Searching global and user specific install
    def search(root,parameter):
        for root, dirs, files in os.walk(root):
            for name in files:
                if fnmatch.fnmatch(name, '*.lnk') and re.search(parameter,name,re.IGNORECASE):
                    os.startfile(os.path.join(root,name))
                    break

    search(os.path.join(os.getenv('APPDATA'),'Microsoft\Windows\Start Menu\Programs'), parameter)
    search('C:\ProgramData\Microsoft\Windows\Start Menu\Programs', parameter)

binding = {"start": start,"unknown": unknown, "navigate": navigate, "stop": stop, "run": run}

# Tts
def speak(txts):
    speaker = tts.init()
    speaker.setProperty('rate', 200)
    voice = speaker.getProperty('voices')[0] # the french voice
    speaker.setProperty('voice', voice.id)

    for txt in txts:
        speaker.say(txt)
    speaker.runAndWait()

# Test
run('firefox')

