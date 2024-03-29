# Rico project
# Author : Thophile
# Date : 10/10/2021

# External
from infi.systray import SysTrayIcon
import speech_recognition as sr
import pyttsx3 as tts
import time
import threading
import os
import subprocess

# File import
import macros.windows_macro as windows_macro
import macros.android_macro as android_macro
from log import log


# Env const
DEBUG = True

# Init
running_in_bkg = True
is_listenning = False

def listen(initiate):
    global is_listenning
    r = sr.Recognizer()
    done = False

    while not done or initiate:
        if not is_listenning : break

        with sr.Microphone() as mic :

            try:
                audio = r.listen(mic, timeout=3, phrase_time_limit=5)


                txt = r.recognize_google(audio, language='fr-FR')
                log(txt)

                if match_intent(txt,"start"):
                    txt = get_parameters(txt,"start")

                    # Find function to call from text
                    intent = find_intent(txt)
                    log(f"intent : {intent}")
                    log(f"parameter {get_parameters(txt, intent)}")
                    binding[intent](get_parameters(txt, intent))
                    done = True

            except sr.WaitTimeoutError:
                if DEBUG : log("timeout")
                pass
            except sr.UnknownValueError:
                r = sr.Recognizer()
            except KeyError:
                binding["unknown"]()
            except BreakException:
                is_listenning = False
                break

def toggle(systray):
    global is_listenning

    is_listenning = not is_listenning
    if is_listenning : 
        t = threading.Thread(name="listening", target=listen, args=[True])
        t.start()

def terminate(systray):
    global running_in_bkg, is_listenning
    running_in_bkg = is_listenning = False

def open_log(systray):
    path = os.path.join(os.getenv('APPDATA') , 'Rico', 'log.txt')
    subprocess.Popen(f'explorer /select,\"{path}\"')

menu_options = (("On/Off", None, toggle),("Open logs", None, open_log),)
systray = SysTrayIcon("rico_logo.ico", "Rico", menu_options, on_quit=terminate)
systray.start()

while running_in_bkg : time.sleep(0.1)

# Killing tray icon after end of other thread
systray.shutdown()

