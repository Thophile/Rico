import re
import webbrowser
import pyttsx3
import httplib2

def parse(txt):
    cmd = txt.lower()
    
    # Nav
    if re.search(r'va sur.*', cmd):
        nav = re.sub(r'.*va sur ', '', cmd)

        #Search query will be replace with advanced parsing at some point
        h = httplib2.Http()
        def tryNav(nav, domain=['.com','.fr','']):
            for ext in domain:
                if re.search(ext,nav) and ext != '':
                    break
                try:
                    url = f"http://www.{nav}{ext}"
                    resp = h.request(url, 'HEAD')

                    if int(resp[0]['status']) < 400 :
                        webbrowser.open(url)
                        return True
                        break
                except:
                    pass
            return False

        if not tryNav(nav) : webbrowser.open('https://www.google.com/search?client=firefox-b-d&q=' + nav)

    # Run
    elif re.search(r'lance.*', cmd):
        run = re.sub(r'.*lance ', '', cmd)
        print('run = ' + run)
        pass

    # Open
    elif re.match(r'ouvre.*', cmd):
        pass

    # Default
    else:
        pyttsx3.speak("Je n'ai pas compris")