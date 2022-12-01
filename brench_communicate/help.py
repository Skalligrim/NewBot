from view.menu_btn import get_default_menu, get_help_text


def send_help_text(message, bot):
    bot.send_message(message.from_user.id, get_help_text(message.from_user.id),
                     reply_markup=get_default_menu(message.from_user.id))