#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import ChatAction, ParseMode
from telegram.ext import Updater, CommandHandler 
import os
import datetime
import random
import pickle
import logging
import ocr_dussmann
import ocr_mensa
from threading import Event
from uuid import uuid4
from time import time
from functools import wraps

bot_token = os.environ.get('BOTTOKEN')
bot_token = "794278284:AAGXxdZkUXX9ZMOchm1w4DmfJKeLxTS9ZQg"


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


greetings = ["Bon Appetit!", "Mir schmeckt's!", "Alles Topf!", "Lecker!", "Der Küchenchef präsentiert...",
             "Frisch für Sie aus dem Tisch:", "Auch wenn Sie lieber zum Döner wollen...:", "Das Menü!",
             "Vielleicht mal was Vegetarisches?", "Muss ja.", "Mahlzeit!", "Der Gaumenschmaus für heute:",
             "Es ist nicht gerade Paul Bocuse, aber was solls.", "Topf-Angebote!", "Der Hunger treibt's rein.",
             "Aus der Gulaschkanone:", "Maggi-Meisterklasse!", "Frisch von Mama Miracoli",
             "Schmeckt auch der Schwiemu!", "Den WuKis und dem Göga schmeckt´s!", "Frisch aus dem Zaubertopf:",
             "Sie glauben nicht, was man im Dampfgarer machen kann. (Bei Gericht #3 musste ich weinen.)",
             "Was dieser Küchenchef präsentiert ist unglaublich!", "Bolo geht immer!", "Bolo statt Volo!",
             "Vom Praktikanten... äh ... Chefkoch für Sie gekocht:", "Vong Küche her:",
             "Alexa... sag Pizzadienst...", "McDussmann – I'm accepting it™",
             "Heute bleibt die Küche kalt, wir fahren in den Wienerwald.",
             "Gehse inne Stadt, wat macht dich da satt? Ne Currywurst.",
             "Kantinencard ist Dussmanns Liebling!", "Oh, Baby, Baby... Es gibt Reis!",
             "Mittagshunger lohnt sich nicht, my Darling...", "Carbonara... e una Coca Cola...",
             "Hier kam noch sweimal ohne...", "Das habe ich hier schonmal vorbereitet.",
             "Peter von Frosta... dass ich nicht lache!", "Dussmann ist für alle da!",
             "Ihr lieben, goldigen Menschen", "Liebe Freunde in Lucullus", "Verehrte Feinschmeckergemeinde",
             "Das (im)perfekte Dinner", "Es liegt mir auf der Zunge...", "Einmal Alles mit viel Scharf",
             "Ich hab 'ne Zwiebel auf dem Kopf, ich bin ein Dussmann!", "Hochgejazzte Tomatensoße nach Art des Hauses",
             "Kantinen-Glücksrad: Ich kaufe alle Es.", "Fleisch ist mein Gemüse!", "Es muss nicht immer Hack sein!"
             ]

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func
    
    return decorator

send_typing_action = send_action(ChatAction.TYPING)
send_upload_video_action = send_action(ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)

@send_typing_action
def start(update, context):
    helptext = """Hi! Ich bin der Heise-Essensbot.
Ich sag dir was es in der Dussmann-Kantine und der MHH-Mensa gibt.
Bedenke: Die Heise-Kantine ist nicht öffentlich und nur für Mitarbeiter.\n
Hier eine Liste der möglichen Kommandos:
/essen – Manuelle Abfrage
/uhrzeit HH:MM – Automatische Benachrichtigung festlegen
/ruhe – Automatische Benachrichtigung abschalten
Probleme und Störungen kannst du gern an mls@ct.de melden!"""
    
    update.message.reply_text(helptext)


@send_typing_action
def get_food(update, context):
    message_text = "_" + random.choice(greetings) + "_ \n\n"
    
    try:
        dussmann_text = ocr_dussmann.getCurrentFood();
    except Exception as e:
        print(e)
        dussmann_text = "\n_Das Dussmann-Angebot konnte ich nicht laden. Sorry._ \n"
    finally:
        try:
            mensa_text = ocr_mensa.getCurrentFood();
        except Exception as e:
            print(e)
            mensa_text = "\n_Das Mensa-Angebot konnte ich nicht laden. Sorry._ \n"
        finally:
            message_text += dussmann_text + "\n\n"
            message_text += mensa_text + "\n\n"
            context.bot.send_message(chat_id=update.effective_message.chat_id, text=message_text, parse_mode=ParseMode.MARKDOWN)


def time_broken(update, context):
    update.message.reply_text("Die Uhrzeitfunktion ist im moment kaputt. :(")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('essen', get_food))

    dispatcher.add_handler(CommandHandler('ruhe', time_broken))
    dispatcher.add_handler(CommandHandler('uhrzeit', time_broken))
    
    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
