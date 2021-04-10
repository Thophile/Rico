import os
from datetime import datetime

def log(msg):
    path = os.path.join(os.getenv('APPDATA') , 'Rico', 'log.txt')
    try:
        f = open(path, 'a')
        str(datetime.now())
        f.write(str(datetime.now()) + ' : ' + msg + '\n')
        f.close()
    except (IOError, FileNotFoundError):
        os.makedirs(os.path.dirname(path))
        log(msg)

