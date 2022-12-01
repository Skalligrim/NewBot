import random
from view.settings import admin_ids


def no_registration():
    return random.choice(["Упс... Я вас не знаю. Зарегистрируйтесь, пожалуйста с помощью команды 'Зарегистрироваться'",
                          "Вы не зарегистрированны. Используйте команду 'Зарегистрироваться', чтобы мы могли работать "
                          "с вами"])

# Удаленные смайлы 😊


def send_question():
    return random.choice(["Ваш вопрос передан аналитикам.",
                          "Данный вопрос отправлен. Скоро вам ответят.", "Я передал вопрос модераторам, спасибо!"])


def send_message():
    return random.choice(["Ваше предложение передано. Благодарю за помощь!",
                          "Данное мнение отправлено. Спасибо!"])


def check_question():
    return random.choice(["Вопрос обработан.", "Так держать! На один вопрос стало меньше!"])


def back():
    return random.choice(["Возвращаюсь назад.", "Уходим на один шаг назад.", "Отмена действия."])


def accepted_question(question):
    texts = ["Прекрасно! Ваш вопрос попал модератору.", "Ваш вопрос прошёл проверку и модератор видит его."]
    for i in range(len(texts)):
        texts[i] = "✅ " + texts[i]
        texts[i] += "\nСодержание вопроса: {}".format(question)
    return random.choice(texts)


def denied_question(question):
    texts = ["Ваш вопрос отклонен.", "К сожалению, ваш вопрос не прошёл проверку.",
             "Возможно ваш вопрос несоответствует тематике или был задан уже ранее. Он был отклонен."]
    for i in range(len(texts)):
        texts[i] = "❌ " + texts[i]
        texts[i] += "\nСодержание вопроса: {}\n".format(question)
        texts[i] += "\nКомментарий: {}\n".format(question.comment)
    return random.choice(texts)


def dont_know():
    return random.choice(["Упс... Я не совсем правильно понял вас.",
                          "Не знаю, что вы хотите... Напишите 'Помощь', чтобы узнать команды",
                          "К сожалению, возникло недопонимание. "
                          "Если напишите 'Помощь', то я расскажу, на что способен"])


def blocked(bot):
    texts = ["Команды недоступны. Вы заблокированы.", "К сожалению, ваш профиль заблокирован.",
             "Команды недоступны. Аккаунт был заблокирован за некорректное поведение."]
    support = "\n\nЕсли вы считаете, что вас заблокировали несправедливо, напишите администраторам:"
    for admin_id in admin_ids:
        user_info = bot.get_chat_member(admin_id, admin_id).user
        support += " @" + user_info.username
    for i in range(len(texts)):
        texts[i] = "🛑 " + texts[i] + support
    return random.choice(texts)
