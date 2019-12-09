#!/bin/python
import datetime
import os
import urllib.request
from helpers import with_logging

targetdir = os.environ.get('DATAFOLDER', '/data/')
targetdir += 'mensa/'

week = datetime.date.today().isocalendar()[1]
year = datetime.datetime.now().year
next_week = False


def getDate():
    global week 
    week = datetime.date.today().isocalendar()[1]
    global year
    year = datetime.datetime.now().year
    global dow 
    dow = datetime.datetime.today().weekday()
    if dow > 4:
        week += 1
        next_week = True
    if week > 52:
        year += 1
        week = 1
        next_week = True


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)


# @with_logging
def getMensa():
    createFolder(targetdir)
    getDate()
    global year
    global week 
    filepath = targetdir + str(year)+str('%02d' % week)+'.pdf'
    if next_week:
        pdf = "https://www.mhh.de/fileadmin/mhh/zentralkueche/downloads/speisepl_nwo.pdf"
    else:
        pdf = "https://www.mhh.de/fileadmin/mhh/zentralkueche/downloads/speisepl_akt.pdf"
    urllib.request.urlretrieve(pdf, filepath)


if __name__ == "__main__":
    getMensa()
