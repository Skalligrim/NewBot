from brench_communicate import user_profile_edit, add_quetstion, check_question, add_analytic, delete_analytic, \
    block_user, help, change_mode
from brench_communicate.sugestion import add_suggestion, show_suggestion
import classes as model
from enumerate.mode import Mode

classic_cmd = {
    None: {
        "Зарегистрироваться": user_profile_edit.registration,
        "Помощь": help.send_help_text
    },
    model.user.User: {
        "Задать вопрос": add_quetstion.ask,
        "Изменить профиль": user_profile_edit.edit,
        "Помощь": help.send_help_text,
        "Стать аналитиком": add_analytic.set_status_analytic,
    },
    model.analytic.Analytic: {
        "Ответить": check_question.show_question,
        "Блокировать пользователя": block_user.search_user,
        "Задать вопрос": add_quetstion.ask,
        "Изменить профиль": user_profile_edit.edit,
        "Помощь": help.send_help_text,
    },
    "Admin": {  # Пока нет админов в БД
        "Добавить аналитика": add_analytic.get_requests,
        "Удалить аналитика": delete_analytic.get_requests,
        "Блокировать пользователя": block_user.search_user,
        "Задать вопрос": add_quetstion.ask,
        "Изменить профиль": user_profile_edit.edit,
        "Помощь": help.send_help_text,
        "Сменить режим": change_mode.select_mode,
    }
}

#  Режим поддержки

# suggestion_cmd = dict(classic_cmd)
# suggestion_cmd[model.user.User]["Высказать мнение"] = add_suggestion.ask
# suggestion_cmd[model.user.User].pop("Задать вопрос")
# suggestion_cmd[model.analytic.Analytic]["Высказать мнение"] = add_suggestion.ask
# suggestion_cmd[model.analytic.Analytic].pop("Задать вопрос")
# suggestion_cmd[model.analytic.Analytic].pop("Ответить")

suggestion_cmd = {
    None: {
        "Зарегистрироваться": user_profile_edit.registration,
        "Помощь": help.send_help_text
    },
    model.user.User: {
        "Высказать мнение": add_suggestion.ask,
        "Изменить профиль": user_profile_edit.edit,
        "Помощь": help.send_help_text,
        "Стать аналитиком": add_analytic.set_status_analytic,
    },
    model.analytic.Analytic: {
        "Показать мнения": show_suggestion.show_suggestions,
        "Блокировать пользователя": block_user.search_user,
        "Высказать мнение": add_suggestion.ask,
        "Изменить профиль": user_profile_edit.edit,
        "Помощь": help.send_help_text,
    },
    "Admin": {  # Пока нет админов в БД
        "Добавить аналитика": add_analytic.get_requests,
        "Удалить аналитика": delete_analytic.get_requests,
        "Блокировать пользователя": block_user.search_user,
        "Задать вопрос": add_quetstion.ask,
        "Изменить профиль": user_profile_edit.edit,
        "Помощь": help.send_help_text,
        "Сменить режим": change_mode.select_mode,
    }
}
menu = {
    Mode.Classic.value.id: classic_cmd,
    Mode.Suggestion.value.id: suggestion_cmd
}
