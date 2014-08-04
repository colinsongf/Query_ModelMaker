import urllib
import os

def readWebPage(url):
    assert(url.startswith("http://"))
    fin = contents = None
    try:
        fin = urllib.urlopen(url)
        contents = fin.read()
    finally:
        if (fin != None): fin.close()
    return contents

def readFile(filename, mode="rt"):
    # rt stands for "read text"
    fin = contents = None
    try:
        fin = open(filename, mode)
        contents = fin.read()
    finally:
        if (fin != None): fin.close()
    return contents

def writeFile(filename, contents, mode="wt"):
    # wt stands for "write text"
    fout = None
    try:
        fout = open(filename, mode)
        fout.write(contents)
    finally:
        if (fout != None): fout.close()
    return True

