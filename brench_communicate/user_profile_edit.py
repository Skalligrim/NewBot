from classes.database import DataBase
from classes.user import User

from view.menu_btn import get_default_menu, button_menu
from view import random_text


def registration(message, bot):
    user_id = message.from_user.id
    db = DataBase()
    if db.is_exist_user(user_id):
        bot.send_message(user_id, "Вы уже зарегистрированы", reply_markup=get_default_menu(user_id))
        return

    bot.send_message(user_id, "Введите свою фамилию и имя.", reply_markup=None)
    bot.register_next_step_handler(message, get_role, bot)  # Переход на этап получения данных о пользователе


def get_role(message, bot):
    user = User(message.from_user.id, message.text)
    bot.send_message(message.from_user.id, "Кем вы являетесь по профессии?\nСтудент или преподаватель.",
                     reply_markup=button_menu(["Студент", "Преподаватель"]))
    bot.register_next_step_handler(message, check_profile, bot, user)


def check_profile(message, bot, user):
    user.role = message.text
    menu = button_menu(["Все верно", "Исправить"])
    bot.send_message(message.from_user.id, "Проверьте все данные:\n{}".format(user), reply_markup=menu)
    bot.register_next_step_handler(message, finish, bot, user)


def finish(message, bot, user):
    if message.text == "Все верно":
        try:
            db = DataBase()
            db.add_user(user)
            menu = get_default_menu(message.from_user.id)
            bot.send_message(message.from_user.id, "Вы зарегистрированны!".format(user),
                             reply_markup=menu)
        except:
            bot.send_message(message.from_user.id, "Возникла ошибка при регистрации.".format(user),
                             reply_markup=get_default_menu(user.id))
    else:
        registration(message, bot)


def edit(message, bot):
    user_id = message.from_user.id
    db = DataBase()
    if not db.is_exist_user(user_id):
        bot.send_message(user_id, "Вы ещё не зарегистрированы.", reply_markup=get_default_menu())
        return

    user = db.get_user(user_id)
    bot.send_message(user_id, "Текущие данные: {}".format(user))
    bot.send_message(user_id, "Как вас зовут?\n( Фамилия и Имя )", reply_markup=button_menu(["Назад"]))
    bot.register_next_step_handler(message, edit_role, bot)


def edit_role(message, bot):
    if message.text.lower() == "назад":
        bot.send_message(message.from_user.id, random_text.back(), reply_markup=get_default_menu(message.from_user.id))
        return
    user = User(message.from_user.id, message.text)
    menu = button_menu(["Студент", "Преподаватель", "Назад"])
    bot.send_message(message.from_user.id, "Кем вы являетесь?", reply_markup=menu)
    bot.register_next_step_handler(message, edit_check, bot, user)


def edit_check(message, bot, user):
    if message.text.lower() == "назад":
        bot.send_message(message.from_user.id, random_text.back(), reply_markup=get_default_menu(message.from_user.id))
        return
    user.role = message.text
    menu = button_menu(["Все верно", "Исправить"])
    bot.send_message(message.from_user.id, "Проверьте все данные:\n{}".format(user), reply_markup=menu)
    bot.register_next_step_handler(message, edit_finish, bot, user)


def edit_finish(message, bot, user):
    if message.text == "Все верно":
        try:
            db = DataBase()
            db.add_user(user)
            menu = get_default_menu(message.from_user.id)
            bot.send_message(message.from_user.id, "Данные обновлены!".format(user),
                             reply_markup=menu)
        except:
            bot.send_message(message.from_user.id, "Возникла ошибка при изменении данных.".format(user),
                             reply_markup=get_default_menu(user.id))
    else:
        edit(message, bot)