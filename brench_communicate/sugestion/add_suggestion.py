from classes.database import DataBase
from classes.question import Question

from view import settings
from view.menu_btn import get_default_menu, button_menu
from view import random_text


def ask(message, bot):
    user_id = message.from_user.id
    db = DataBase()
    if not db.is_exist_user(user_id):
        bot.send_message(user_id, random_text.no_registration(), reply_markup=get_default_menu())
        return

    bot.send_message(user_id, "Напишите мне ваше предложение:\nНазад - вернуться в главное меню",
                     reply_markup=button_menu(["Назад"]))
    bot.register_next_step_handler(message, suggestion_ready, bot)


def suggestion_ready(message, bot):
    if message.text.lower() == "назад":
        bot.send_message(message.from_user.id, "Отмена сообщения.",
                         reply_markup=get_default_menu(message.from_user.id))
        return
    bot.send_message(message.from_user.id, random_text.send_message(),
                     reply_markup=get_default_menu(message.from_user.id))
    db = DataBase()
    question = Question(from_user=message.from_user.id, text=message.text, status=settings.statuses["suggestion"])
    db.add_question(question)
