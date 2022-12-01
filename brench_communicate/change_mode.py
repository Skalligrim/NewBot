import view
from classes.database import DataBase
from classes.user import User

from view.menu_btn import get_default_menu, button_menu
from view import random_text
from enumerate.mode import Mode


def select_mode(message, bot):
    user_id = message.from_user.id
    bot.send_message(user_id, "На какой режим переходим?",
                     reply_markup=button_menu(["Классический режим!", "Режим поддержки!", "Назад"]))
    bot.register_next_step_handler(message, change_mode, bot)  # Переход на этап получения данных о пользователе


def change_mode(message, bot):
    db = DataBase()
    user_id = message.from_user.id
    if message.text.startswith("Классический режим"):
        view.settings.mode = Mode.Classic
    elif message.text.startswith("Режим поддержки"):
        view.settings.mode = Mode.Suggestion
    else:
        bot.send_message(message.from_user.id, random_text.back(), reply_markup=get_default_menu(user_id))
        return
    text_to_all = "Конференция сменила режим работы. Будьте внимательны, ваши текущие действия были отменены.\n{}"\
        .format(view.settings.mode.value.name.value)
    users = db.get_user_role()
    if message.text.find("!") != -1:
        for user in users:
            bot.send_message(user.id, text_to_all, reply_markup=get_default_menu(user_id))
