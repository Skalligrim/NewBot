import telebot
from view import secret
import classes as model
from classes.database import DataBase
from brench_communicate import user_profile_edit
from view import settings, random_text
from view.menu_btn import get_default_menu
from view.commands import menu

token = "2075824842:AAE670x9klLinwSsjVxr1AuSsF8Vnzq5BeY"
bot = telebot.TeleBot(token, parse_mode=None)


@bot.message_handler(commands=['start'])
def start_command(message):
    name_conf = "Политехника 2021"
    text = """Здравствуй, {}, я интерактивный помощник конференции <b>"{}"</b> МГТУ им. Баумана.
Здесь можно задать вопрос по текущей тематике конференции, пока лектор рассказывает материал.

Но для начала требуется регистрация🙂 Следуйте моим инструкциям.""".format(message.from_user.username, name_conf)
    bot.send_message(message.from_user.id, text, parse_mode="HTML")
    user_profile_edit.registration(message, bot)


@bot.message_handler(func=lambda message: True)
def listen_message(message):
    text = message.text.lower()
    db = DataBase()

    if secret.check(text):
        uid = message.from_user.id
        user = db.get_user(uid)
        user.root = 3
        db.update_user(user)
        bot.send_message(uid, "Рад тебя снова видеть, {}".format(user), reply_markup=get_default_menu(uid))
        return

    if db.get_user(message.from_user.id):
        if int(db.get_user(message.from_user.id).root) // 2 % 2 == 0:
            bot.send_message(message.from_user.id, random_text.blocked(bot))
            return

    #  Определение команд для пользователя

    types_user = [None]
    if db.is_exist_user(message.from_user.id):
        types_user = [model.user.User]
        if message.from_user.id in settings.admin_ids:
            types_user.append("Admin")
    if db.is_exist_analytic(message.from_user.id):
        types_user = [model.analytic.Analytic]
        if message.from_user.id in settings.admin_ids:
            types_user.append("Admin")

    mode_menu = menu.get(settings.mode.value.id)
    for type_user in types_user:
        actions = mode_menu[type_user]
        for name, action in actions.items():
            if name.lower() == text:
                action(message, bot)
                return

    bot.send_message(message.from_user.id, random_text.dont_know(), reply_markup=get_default_menu(message.from_user.id))


def main():
    print("Бот запущен")
    bot.polling()


if __name__ == '__main__':
    main()
