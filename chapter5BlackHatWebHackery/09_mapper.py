import contextlib
import os
import queue
import requests
import sys
import threading
import time
FILTERED=[".jpg",".gif",".png",".css"]
TARGET="https://wordpress.org"
THREADS=10
answers=queue.Queue()
web_paths=queue.Queue()
def gather_paths():
    for root,_,files in os.walk('.'):
        for fname in files:
            if os.path.splitext(fname)[1] in FILTERED: #os.path.splittext splits a path to root and extension
                continue
            path=os.path.join(root,fname)
            if path.startswith('.'):
                path=path[1:]
            print(path)
            web_paths.put(path)
@contextlib.contextmanager
def chdir(path):
    """
    On enter,change directory to specified path.
    On exit,change directory back to original
    """
    this_dir=os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(this_dir)
if __name__=='__main__':
    with chdir("/home/kali/Downloads/wordpress"):
        gather_paths()
        input('press enter to continue')