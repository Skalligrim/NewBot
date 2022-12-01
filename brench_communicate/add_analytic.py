import telebot
from classes.database import DataBase
from classes.user import User
from classes.analytic import Analytic

from view import settings
from view.menu_btn import get_default_menu, button_menu


def set_status_analytic(message, bot):
    user_id = message.from_user.id
    db = DataBase()
    if db.is_exist_analytic(user_id):
        bot.send_message(user_id, "Вы уже являетесь аналитиком.", reply_markup=get_default_menu(user_id))
        return
    if db.is_exist_user(user_id):
        user = db.get_user(user_id)
        user.role = "Потенциальный аналитик"
        db.update_user(user)
        bot.send_message(user_id, "Запрос на смену статуса 'Аналитик' отправлен.",
                         reply_markup=get_default_menu(user_id))
        text = "Новый запрос аналитика.\nВсего запросов: {}".format(len(db.get_user_role("Потенциальный аналитик")))
        for id_admin in settings.admin_ids:
            bot.send_message(id_admin, text)
    else:
        bot.send_message(user_id, "Вы не зарегистрированы.", reply_markup=get_default_menu())


def get_requests(message, bot):
    user_id = message.from_user.id
    db = DataBase()
    users = db.get_user_role("Потенциальный аналитик")
    text = "Текущие запросы на аналитиков:\n"
    index = 1
    for user in users:
        text += "{}. {}\n".format(index, user)
        index += 1
    text += "\nЗапишите номера через проблел. Положительные - принять, отрицательные - отклонить."
    bot.send_message(user_id, text,
                     reply_markup=button_menu(["Назад"]))
    bot.register_next_step_handler(message, select_analytic, bot)


def select_analytic(message, bot):
    user_id = message.from_user.id
    if message.text.lower() == "назад":
        bot.send_message(user_id, "Возврат в главное меню.", reply_markup=get_default_menu(user_id))
        return
    db = DataBase()
    users = db.get_user_role("Потенциальный аналитик")
    count = len(users)
    request_list = message.text.split()
    text = "Применены следующие действия:\n"
    for request in request_list:
        if not request.lstrip('+-').isnumeric():
            continue
        request = int(request)
        if abs(request) > count:
            continue
        index = request - 1 if request >= 0 else -1 * request - 1
        text += "\n{}. {} - ".format(index + 1, users[index])
        if request >= 0:
            db.add_analytic(Analytic(users[index].id, users[index].name))
            user = db.get_user(users[index].id)
            user.role = "Аналитик"
            db.update_user(user)
            bot.send_message(users[index].id, "✅ Заявка на изменение статуса 'Аналитик' принята.\n"
                                              "Доступен новый функционал.",
                             reply_markup=get_default_menu(users[index].id))
            text += "принят."
        else:
            request *= -1
            user = db.get_user(users[index].id)
            user.role = "Студент"
            db.update_user(user)
            bot.send_message(users[index].id, "❌ Заявка на изменение статуса 'Аналитик' отклонена.\n"
                                              "Ваш профиль имеет статус 'Студент'.")
            text += "отклонен."
    bot.send_message(user_id, text, reply_markup=get_default_menu(user_id))
