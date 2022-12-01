import telebot
from view import settings
from classes.database import DataBase
from enumerate.mode import Mode


def get_default_menu(user_id=None):
    """Выдает меню для пользователя. Зависит от прав пользователя."""

    menu = telebot.types.ReplyKeyboardMarkup()

    params = ['Зарегистрироваться', 'Помощь']
    db = DataBase()
    is_user = db.is_exist_user(user_id)
    is_analytic = db.is_exist_analytic(user_id)
    is_admin = user_id in settings.admin_ids
    if user_id:
        if is_user:
            if settings.mode.value.id == Mode.Classic.value.id:
                params = ['Задать вопрос', ['Изменить профиль', 'Помощь']]
            elif settings.mode.value.id == Mode.Suggestion.value.id:
                params = ['Высказать мнение', ['Изменить профиль', 'Помощь']]
            if is_analytic:
                if settings.mode.value.id == Mode.Classic.value.id:
                    params[0] = ["Ответить", "Задать вопрос"]
                elif settings.mode.value.id == Mode.Suggestion.value.id:
                    params[0] = ["Показать мнения", "Высказать мнение"]
                params.insert(1, "Блокировать пользователя")
            if is_admin:
                params.insert(1, ["Добавить аналитика", "Удалить аналитика"])
                if not is_analytic:  # Добавляется функция, если не является аналитиком
                    params.insert(2, "Блокировать пользователя")
                params.append("Сменить режим")

    for item in params:
        if isinstance(item, list):
            menu.add(*item)
        else:
            menu.add(item)
    return menu


def button_menu(params):
    """Шаблон всех меню"""
    qmenu = telebot.types.ReplyKeyboardMarkup()
    if len(params) > 3:
        for i in range(1, len(params), 2):
            qmenu.add(params[i - 1], params[i])
        if len(params) % 2:
            qmenu.add(params[-1])
    else:
        for item in params:
            if isinstance(item, list):
                qmenu.add(*item)
            else:
                qmenu.add(item)
    return qmenu


def get_help_text(user_id):
    db = DataBase()
    help_text = "⚡ Вас приветствует интерактивный конференц-бот кафедры СГН!\n\nМоя задача помочь наладить " \
                "коммуникацию между модераторами и слушателями.\n\n"
    if not db.is_exist_user(user_id):
        help_text += "Пока мы с вами не знакомы. Пожалуйста, пройдите регистрацию, чтобы вы могли " \
                     "задавать вопросы.\nДля этого напишите 'Зарегистрироваться'.\n"
    else:

        help_text += "Поскольку вы зарегистрированный пользователь, {}, то вам доступна возможность задавать " \
                     "вопросы.\nДля этого напишите 'Задать вопрос' и я с " \
                     "радостью передам его модераторам.\n".format(db.get_user(user_id))
    if db.is_exist_analytic(user_id):
        help_text += "\n⚡ Аналитик ⚡\nК тому же я смотрю, вы являетесь аналитиком!\nВам доступна функция просмотра " \
                     "вопросов участников по команде 'Ответить'. На каждый вопрос можно ответить 'Да', 'Нет' или " \
                     "'Другое'.\n"
    if user_id in settings.admin_ids:
        help_text += "\n⚡ Администратор ⚡\nВашей задачей является отбор аналитков. Когда кто-то ведет команду " \
                     "'Стать аналитиком' я изменю его статус на 'Потенциальный аналитик', после чего уведомлю вас. " \
                     "Чтобы принять или отклонить аналитика требуется команда 'Добавить аналитика' и я выдам список " \
                     "всех претендентов.\nАдминистратор также может стать аналитиком!"
    return help_text