from classes.database import DataBase
from view import settings, random_text
from view.menu_btn import get_default_menu, button_menu


def show_question(message, bot, offset=0):
    db = DataBase()
    questions = db.get_question()
    if not len(questions):
        text = "Вопросов нет.\nРешено всего вопросов: " + db.get_analytic(message.from_user.id).question_solved
        bot.send_message(message.from_user.id, text, reply_markup=get_default_menu(message.from_user.id))
        return
    offset %= len(questions)
    question = questions[offset]
    user = db.get_user(question.from_user)
    text = "❓ {}:\n{}".format(user, question)
    bot.send_message(message.from_user.id, text, reply_markup=button_menu([["Да", "Нет", "Другой"], "Назад"]))
    bot.register_next_step_handler(message, select_question, bot, question, offset)


def select_question(message, bot, question, offset):
    db = DataBase()
    cmd = message.text.lower()
    analytic_id = message.from_user.id

    if cmd in ["другой", "пропустить", "следующий", "/"]:
        show_question(message, bot, offset+1)
        return

    elif cmd in ["да", "хорошо", "+"]:
        new_question = question
        new_question.from_analytic = analytic_id
        new_question.status = settings.statuses["accepted"]
        db.update_question(new_question)
        bot.send_message(analytic_id, "Комментарий к данному решению.", reply_markup=button_menu(["Нет комментария"]))
        bot.register_next_step_handler(message, comment, bot, question, offset)

    elif cmd in ["нет", "удалить", "-"]:
        new_question = question
        new_question.from_analytic = analytic_id
        new_question.status = settings.statuses["denied"]
        db.update_question(new_question)
        bot.send_message(analytic_id, "Комментарий к данному решению.", reply_markup=button_menu(["Нет комментария"]))
        bot.register_next_step_handler(message, comment, bot, question, offset)

    elif cmd == "назад":
        item = db.get_analytic(analytic_id)
        text = random_text.back() + "\nРешено всего вопросов: " + item.question_solved
        bot.send_message(analytic_id, text, reply_markup=get_default_menu(analytic_id))
        return


def comment(message, bot, question, offset):
    question.comment = message.text
    db = DataBase()
    db.update_question(question)
    db.update_analytic_qsolved(message.from_user.id)
    bot.send_message(message.from_user.id, random_text.check_question(),
                     reply_markup=get_default_menu(message.from_user.id))
    user = None
    if question.status == settings.statuses["accepted"]:
        user = db.get_user(question.from_user)
        user.question_accepted = int(user.question_accepted) + 1
        send_message_to_moderator(bot, question, user)
        bot.send_message(question.from_user, random_text.accepted_question(question))
    elif question.status == settings.statuses["denied"]:
        user = db.get_user(question.from_user)
        user.question_denied = int(user.question_denied) + 1
        bot.send_message(question.from_user, random_text.denied_question(question))
    db.update_user(user)

    show_question(message, bot, offset)


def send_message_to_moderator(bot, question, user):
    for moderator_id in settings.moderator_ids:
        text = "Новый вопрос от {}\n{}".format(user, question)
        bot.send_message(moderator_id, text)