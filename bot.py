#!/usr/bin/env python
# -*- coding: utf-8 -*-

##### IMPORTS ######
import logging
from subprocess import (PIPE, Popen)
import telebot
from Token import TOKEN
from mongo_auth import dbuser, dbpass
import pymongo
import utils
####################

## CONST MESSAGES ##
START_MESSAGE = "Hi, all you need to do is add me to a group and then reply 'fa or فا' to any message and I will transliterate it for you.\n or just send me a message"
HELP_MESSAGE = "Use this bot to transliterate Finglish messages to Farsi.\n add this bot to your groups, and if you see any finglish message, reply 'fa', 'فا' to the message.\n\nبا این ربات می‌توانید پیام های فینگلیش را به فارسی تبدیل کنید، کافی است ربات را در گروه های خود اضافه کرده و اگر پیام فینگلیش دیدید، در پاسخ به آن بنویسید 'fa' یا 'فا'"
CONTACT_MESSAGE = "please email me :\n mfg1376@gmail.com"
ABOUT_MESSAGE = "من محمد فغان‌پور گنجی هستم،\n اطلاعات بیشتر در مورد من رو در mohganji.ir می‌تونید ببینید"

####################


## INITIALIZATION ##
bot = telebot.TeleBot(TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

db = pymongo.MongoClient('mongodb://%s:%s@127.0.0.1:27017/finToFa' % (dbuser, dbpass)).finToFa
# collections = db.collection_names()
# if "users" not in collections:
#     db.create_collection("users")
# if "words" not in collections:
#     db.create_collection("words")


####################


#### FUNCTIONS #####
def transliterate_to_farsi(message):
    """ transliterate finglish messages to farsi, returns farsi text """
    text = message.text
    user_id = message.from_user.id
    logging.critical(str(user_id) + " : " + text)
    if text:
        if text[0] == '/':
            text = text[1:]

        text = text.replace("@TransliterateBot", "")
        text = text.split()
        # defallahi(text)
        # irregularHandle(text)
        shcommand = ['php', './behnevis.php']
        shcommand.extend(text)
        pipe = Popen(shcommand, stdout=PIPE, stderr=PIPE)
        text, err = pipe.communicate()
        if err:
            logging.critical("PHP ERR: " + err)
        logging.critical("res : " + str(user_id) + " : " + text)
        return text
####################


##### HANDLERS #####
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """ function for start command """
    utils.addNewUser(db, message.from_user.username, message.from_user.id)
    bot.reply_to(message,
                 (START_MESSAGE))


@bot.message_handler(commands=['help'])
def help_provider(message):
    """ function for help command """

    bot.reply_to(message,
                 (HELP_MESSAGE))

@bot.message_handler(commands=['contact'])
def contact_creator(message):
    """ function for contact command command """

    bot.reply_to(message,
                 (CONTACT_MESSAGE))

@bot.message_handler(commands=['about'])
def about_me(message):
    """ function for about creator of this bot command """

    bot.reply_to(message,
                 (ABOUT_MESSAGE))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_group_or_user(message):
    """ check if message is sent to the bot or in a group """
    if message.chat.type == "private":
        text = transliterate_to_farsi(message)
        bot.reply_to(message, text)
    else:
        if message.text == 'fa' or message.text == 'Fa' or message.text == 'FA' or message.text == 'فا'.decode('utf-8'):
            msg = message.reply_to_message
            if msg is not None:
                text = transliterate_to_farsi(msg)
                bot.reply_to(msg, text)
            else:
                logging.critical("Err : message is empty")
####################


###### RUNNER ######
bot.skip_pending = True
bot.polling()
####################
