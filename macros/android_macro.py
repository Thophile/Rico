from macro import *
import random
import re
import webbrowser
import pyttsx3 as tts
import httplib2
import os,fnmatch
from log import log

class WindowsMacro(Macro):
    
    def __init__(self, path):
        self.binding = {
            "navigate": self.navigate,
            "run": self.run,
            "search": self.search}
        super.__init__(self, path)

    def search(self, parameter=""):
        self.speak([self.pick_response("search")])
        webbrowser.open('https://www.google.com/search?client=firefox-b-d&q=' + parameter)
        
    def navigate(self, parameter=""):
        self.speak([self.pick_response("navigate")])
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

    def run(self, parameter=""):
        self.speak([self.pick_response("run")])
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