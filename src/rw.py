# rw.py
# Hongyu Li

# This file contains helper functions to read/write files

import urllib
import os

# Read a web page
# returns the content as a string
def readWebPage(url):
    assert(url.startswith("http://"))
    fin = contents = None
    try:
        fin = urllib.urlopen(url)
        contents = fin.read()
    finally:
        if (fin != None): fin.close()
    return contents

# Read a file
# filename is the path of the file, string type
# returns the content as a string
def readFile(filename, mode="rt"):
    # rt stands for "read text"
    fin = contents = None
    try:
        fin = open(filename, mode)
        contents = fin.read()
    finally:
        if (fin != None): fin.close()
    return contents

# Write 'contents' to the file
# 'filename' is the path of the file, string type
# 'contents' is of string type
# returns True if the content has been written successfully
def writeFile(filename, contents, mode="wt"):
    # wt stands for "write text"
    fout = None
    try:
        fout = open(filename, mode)
        fout.write(contents)
    finally:
        if (fout != None): fout.close()
    return True

