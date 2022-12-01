import datetime

from classes.database import DataBase
from classes.question import Question

from view import settings
from view.menu_btn import get_default_menu, button_menu
from view import random_text


def show_suggestions(message, bot, offset=0):
    db = DataBase()
    questions = db.get_question(status=settings.statuses["suggestion"])
    if questions is None:
        text = "Предложений нет."
        bot.send_message(message.from_user.id, text, reply_markup=get_default_menu(message.from_user.id))
        return
    if not len(questions):
        text = "Предложений нет."
        bot.send_message(message.from_user.id, text, reply_markup=get_default_menu(message.from_user.id))
        return
    index = 1
    text = ""
    for item in questions:
        user = db.get_user(item.from_user)
        text += "{}. {}:\n{}\n".format(index, user, item)
        index += 1
    misc = open("suggestion_{}.txt".format(datetime.datetime.now().strftime("%H-%M-%S")), "w+")
    f = open("suggestion_{}.txt".format(datetime.datetime.now().strftime("%H-%M-%S")), "r")
    misc.write(text)
    misc.close()
    bot.send_document(message.from_user.id, f)
    f.close()
