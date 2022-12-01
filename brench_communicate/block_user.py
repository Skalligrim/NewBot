import telebot
from classes.database import DataBase
from classes.user import User
from classes.question import Question

from view import settings
from view.menu_btn import get_default_menu, button_menu
from view import random_text


def search_user(message, bot):
    text = "Введите <b>ID</b> или <b>Имя пользователя</b>."
    bot.send_message(message.from_user.id, text, reply_markup=button_menu(["Назад"]), parse_mode="HTML")
    bot.register_next_step_handler(message, select_user, bot)


def select_user(message, bot):
    db = DataBase()
    text = message.text
    if text.lower() == "назад":
        bot.send_message(message.from_user.id, random_text.back(), reply_markup=get_default_menu(message.from_user.id))
        return
    req = None
    send_text = "Не удалось найти пользователя с "
    if text.isdecimal():
        if db.is_exist_user(text):
            req = [db.get_user(text.replace(" ", ""))]
        else:
            send_text += "ID: " + text
    else:
        req = db.get_users_by_name(text)
        send_text += "именем: " + text
    if req is None or req == []:
        send_text += "\nПопробуйте снова."
        bot.send_message(message.from_user.id, send_text, reply_markup=button_menu(["Назад"]), parse_mode="HTML")
        search_user(message, bot)
        return
    bot.send_message(message.from_user.id, "Результаты поиска: ")
    k = 1
    send_text = ""
    for user in req:
        send_text += "{}. {}\n".format(k, user)
        k += 1
    send_text += "\nЗапишите номера пользователей через проблел для их блокировки."
    bot.send_message(message.from_user.id, send_text, reply_markup=button_menu(["Назад"]))
    bot.register_next_step_handler(message, ban_user, bot, req)


def ban_user(message, bot, req):
    user_id = message.from_user.id
    if message.text.lower() == "назад":
        bot.send_message(user_id, random_text.back(), reply_markup=get_default_menu(user_id))
        return
    db = DataBase()
    request_list = message.text.split()
    text_result = "Заблокированы следующие пользователи:\n\n"

    for request in request_list:
        if not request.lstrip('+-').isnumeric():
            continue
        request = int(request)
        if request <= 0:
            continue
        index = request - 1
        req[index].root = 1
        db.update_user(req[index])
        text_result += str(req[index]) + "\n"
        text_block = "🛑 Ваш профиль заблокирован! 🛑\nЗа нарушение правил пользования ботом.\n\n" \
                     "Если вы несогласны с этим, прошу написать администраторам"
        for admin_id in settings.admin_ids:
            user_info = bot.get_chat_member(admin_id, admin_id).user
            text_block += " @" + user_info.username

        bot.send_message(req[index].id, text_block)
    bot.send_message(user_id, text_result, reply_markup=get_default_menu(user_id))
