import telebot
from classes.database import DataBase
from classes.user import User
from classes.analytic import Analytic

from view import settings
from view.menu_btn import get_default_menu, button_menu


def get_requests(message, bot):
    user_id = message.from_user.id
    db = DataBase()
    analytics = db.get_analytic()
    text = "Текущие аналитики:\n"
    index = 1
    for analytic in analytics:
        text += "{}. {}\n".format(index, analytic)
        index += 1
    text += "\nЗапишите номера аналитиков через проблел, которых требуется удалить."
    bot.send_message(user_id, text,
                     reply_markup=button_menu(["Назад"]))
    bot.register_next_step_handler(message, select_analytic, bot)


def select_analytic(message, bot):
    user_id = message.from_user.id
    if message.text.lower() == "назад":
        bot.send_message(user_id, "Возврат в главное меню.", reply_markup=get_default_menu(user_id))
        return
    db = DataBase()
    analytics = db.get_analytic()
    count = len(analytics)
    request_list = message.text.split()
    text = "Применены следующие действия:\n"
    for request in request_list:
        if not request.isdigit():
            continue
        request = int(request)
        if abs(request) > count:
            continue
        request -= 1
        current_id = analytics[request].id
        db.delete_analytic(current_id)
        user = db.get_user(current_id)
        user.role = "Студент"
        db.update_user(user)
        text += "\n{}. {} - удален.".format(request+1, analytics[request])

        bot.send_message(user_id, text, reply_markup=get_default_menu(user_id))





