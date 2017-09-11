import logging
from subprocess import (PIPE, Popen)

def addNewUser(db, username, chatId):
    """ add a new user to database for broadcasting."""
    new_user = {'id': chatId, 'username': username}
    if not db.users.find_one({"id" : new_user["id"]}):
        logging.critical("db: " + str(new_user) + " added.")
        db.users.insert_one(new_user)
    else:
        logging.critical("db: " + str(new_user) + " : " + "user exists!")

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
