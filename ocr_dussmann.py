#!/bin/python3
# -*- coding: utf-8 -*-

# Written by Otis Sotek for c't Magazin

import re
import pytesseract
import datetime
from pdf2image import convert_from_path
import numpy
import time
import os 

price_re = re.compile("(\d+,\d+\s*€)")
linebreak_re = re.compile("\n+")
euro_re = re.compile("€.*$")
illegal_char_re = re.compile('([^a-zA-Z0-9äöüÄÖÜ€ß",\.\-– ]|(\s,))')
double_space_re = re.compile("\s+")
special_re = re.compile("(highlight der woche|fit men[üu])", re.IGNORECASE)


# Konstanten

soup_x = 0.152
soup_y = 0.234
soup_h = 0.031
soup_w = 0.790

main1_x = soup_x
main1_y = 0.268
main1_h = 0.163
main1_w = soup_w

main2_x = soup_x
main2_y = 0.433
main2_h = main1_h
main2_w = soup_w

veg_x = soup_x
veg_y = 0.597
veg_h = main1_h
veg_w = soup_w

soup_price = "0,85 €"

pdf = "speiseplan.pdf"


class Food:
    name = None
    price = None
    special = None

    def __init__(self, name, price, special=None):
        self.name = name
        self.price = price
        self.special = special


class Menu:
    soup = None
    main1 = None
    main2 = None
    veg = None

    def __init__(self, soup, main1, main2, veg):
        self.soup = soup
        self.main1 = main1
        self.main2 = main2
        self.veg = veg

    def pre(self):
        nl = "\n"
        return f"""*Speiseplan Dussmann*

{self.soup.name}
`{self.soup.price}`

{"_" + self.main1.special + "_ " + nl if self.main1.special else ""}{self.main1.name}
`{self.main1.price}`

{"_" + self.main2.special + "_ " + nl if self.main2.special else ""}{self.main2.name}
`{self.main2.price}`

{"_" + self.veg.special + "_ " + nl if self.veg.special else ""}🌱 {self.veg.name}
`{self.veg.price}`
"""


def menu(day):
    if not day in range(0, 5):
        return None

    global pdf
    image = convert_from_path(pdf)[0].convert('P', dither=None)

    soup = parse(crop(image, (soup_x, soup_y, soup_w, soup_h)), "soup")
    main1 = parse(crop(image, (main1_x, main1_y, main1_w, main1_h)))
    main2 = parse(crop(image, (main2_x, main2_y, main2_w, main2_h)))
    veg = parse(crop(image, (veg_x, veg_y, veg_w, veg_h)))

    return Menu(soup[day], main1[day], main2[day], veg[day])


def fifths(image):
    fifths = []
    for i in range(0, 5):
        #                    x      y  w    h
        fifth = crop(image, (i*0.2, 0, 0.2, 1))
        fifths.append(fifth)
    return fifths


def parse(image, food_type="normal"):
    food = []
    for fifth in fifths(image):
        x = pytesseract.image_to_string(fifth, lang="deu")
        current_food = prettify(x, food_type)
        if current_food.price == None and food_type != "normal":
            if food_type == "soup":
                current_food.price = soup_price
        food.append(current_food)
    return food


def prettify(line, food_type):
    line = re.sub(linebreak_re, " ", line)
    line = re.sub(illegal_char_re, "", line)
    line = re.sub(double_space_re, " ", line).strip()
    price = None
    name = line
    split = re.split(price_re, line)
    if len(split) > 2:
        price = split[1].strip()
        name = split[0].strip()
    name = re.sub(r"\d", "", name)
    name = re.sub(double_space_re, " ", name).strip()
    special = None
    split = re.split(special_re, name)
    if len(split) > 2:
        special = split[1].strip()
        name = split[2].strip()
    return Food(name, price, special)


def crop(image, box):
    w, h = image.size
    x = int(box[0]*w)
    y = int(box[1]*h)
    cropped_w = int(box[2]*w)
    cropped_h = int(box[3]*h)
    return image.crop((x, y, x + cropped_w, y + cropped_h))


def saveMenuToFile(targetfolder):
    week = str("%02d" % datetime.date.today().isocalendar()[1])
    year = str(datetime.datetime.now().year)
    global pdf
    pdf = targetfolder + year + week + ".pdf"
    print("Converting Dussmann to text")
    for dow in range(0, 5):
        filename = targetfolder + year + week + str(dow) + ".txt"
        m = menu(dow)
        file = open(filename, "w")
        file.write(m.pre())
        file.close()

def getCurrentFood():
    targetfolder = os.environ.get('DATAFOLDER', './data/')
    targetfolder += "dussmann/"
    week = datetime.date.today().isocalendar()[1]
    year = str(datetime.datetime.now().year)
    hour = datetime.datetime.now().hour
    dow = datetime.datetime.today().weekday()
    if hour >= 14:
        dow += 1
    if dow > 4:
        dow = 0
        week += 1
    week = str("%02d" % week)
    filename = targetfolder + year + week + str(dow) + ".txt"
    file = open(filename, "r")
    return file.read() 

if __name__ == "__main__":
    targetfolder = "./data/dussmann/"
    saveMenuToFile(targetfolder)
    m = menu(datetime.datetime.today().weekday())
    if m:
        print(m.pre())
