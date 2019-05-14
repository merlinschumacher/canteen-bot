#!/bin/python3
# -*- coding: utf-8 -*-

#Written by Otis Sotek for c't Magazin

import re
import pytesseract
import datetime
from pdf2image import convert_from_path
import numpy
import time
import os 
from helpers import with_logging

#price_re = re.compile("(\d+,\d+\s*€)")
linebreak_re = re.compile("\n+")
euro_re = re.compile("€.*$")
illegal_char_re = re.compile("([^a-zA-Z0-9äöüÄÖÜ€ß,\.\-– ]|(\s,))")
double_space_re = re.compile("\s+")
calories_re = re.compile("\d{2,4}.kcal.\d{3,4}\skJ")
iconmess_re = re.compile("(.E.?|.?uu.|\s?C\s|\?|.frn.?|\s\d\s)")

# Konstanten

main1_x = 0.085
main1_y = 0.17
main1_h = 0.388
main1_w = 0.20

main2_x = 0.31
main2_y = main1_y
main2_h = main1_h
main2_w = main1_w

main3_x = 0.51
main3_y = main1_y
main3_h = main1_h
main3_w = main1_w

market_x = 0.73
market_y = main1_y
market_h = main1_h
market_w = main1_w

pdf = "mensa.pdf"

class Food:
        name = None;
        calories = None;

        def __init__(self, name, calories):
                self.name = name
                self.calories = calories

class Menu:
        main1 = None;
        main2 = None;
        main3 = None;
        extras = None;

        def __init__(self, main1, main2, main3, market):
                self.main1 = main1
                self.main2 = main2
                self.main3 = main3
                self.market = market
        
        def pre(self):
                nl = "\n"
                return f"""*Speiseplan Mensa*

{self.main1.name}
`{self.main1.calories}`

{self.main2.name}
`{self.main2.calories}`

{self.main3.name}
`{self.main3.calories}`

{self.market.name}
`{self.market.calories}`
"""

def menu(day):
        if not day in range(0, 5):
            return None
        global pdf
        image = convert_from_path(pdf, dpi=600)[0].convert('LA')

        main1 = parse(crop(image, (main1_x, main1_y, main1_w, main1_h)))
        main2 = parse(crop(image, (main2_x, main2_y, main2_w, main2_h)))
        main3 = parse(crop(image, (main3_x, main3_y, main3_w, main3_h)))
        market = parse(crop(image, (market_x, market_y, market_w, market_h)))

        return Menu(main1[day], main2[day], main3[day], market[day])

def splits(image):
        splits = []
        for i in range(0, 5):
                #                    x  y         w  h
                split = crop(image, (0, i * 0.205, 1, 0.20))
                splits.append(split)
        return splits

def parse(image, food_type="normal"):
        food = []
        for split in splits(image):
                x = pytesseract.image_to_string(split, lang="deu")
                current_food = prettify(x, food_type)
                food.append(current_food)
        return food

def prettify(line, food_type):
        line = re.sub(linebreak_re, " ", line)
        line = re.sub(illegal_char_re, "", line)
        line = re.sub(double_space_re, " ", line).strip()
        line = re.sub(iconmess_re, " ", line).strip()
        calories = re.search(calories_re, line)
        if calories is not None:
                calories = calories.group()
        else:
                calories  = "? kcal / ? kJ"
        line = re.sub(calories_re, " ", line).strip()
        name = re.sub(r"\d", "", line)
        name = re.sub(double_space_re, " ", name).strip()
        return Food(name, calories)

def crop(image, box):
        w, h = image.size
        x = int(box[0]*w)
        y = int(box[1]*h)
        cropped_w = int(box[2]*w)
        cropped_h = int(box[3]*h)
        return image.crop((x, y, x + cropped_w, y + cropped_h))

# @with_logging
def saveMenuToFile(targetfolder):
    week = str("%02d" % datetime.date.today().isocalendar()[1])
    year = str(datetime.datetime.now().year)
    global pdf
    pdf = targetfolder + year + week + ".pdf"
    for dow in range (0,5):
        filename = targetfolder + year + week + str(dow) + ".txt"
        m = menu(dow)
        file = open(filename, "w")
        file.write(m.pre())
        file.close()

def getCurrentFood():
    targetfolder = os.environ.get('DATAFOLDER', '/data/')
    targetfolder += "mensa/"
    week = str("%02d" % datetime.date.today().isocalendar()[1])
    year = str(datetime.datetime.now().year)
    hour = datetime.datetime.now().hour
    dow = datetime.datetime.today().weekday()
    if hour >= 14:
        dow += 1
    if dow > 4:
        dow = 0;
    filename = targetfolder + year + week + str(dow) + ".txt"
    file = open(filename, "r")
    return file.read() 

if __name__ == "__main__":
    targetfolder = "/data/mensa/"
    saveMenuToFile(targetfolder)
    m = menu(datetime.datetime.today().weekday())
    if m:
        print(m.pre())
