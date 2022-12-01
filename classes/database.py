import datetime
import sqlite3

from classes.user import User
from classes.analytic import Analytic
from classes.question import Question


# Static function


def get_table_form(params):
    text = "("
    for item in params:
        if isinstance(item, (int, float)):
            item = str(item)
        text += item + ","
    text = text[:-1] + ")"
    return text


def get_insert_format(table, params: dict):
    req = "INSERT INTO {} {} VALUES (".format(table, get_table_form(params.keys()))
    for item in params.values():
        req += '"{}",'.format(item)
    req = req[:-1] + ");"
    return req


def get_set_format(params: dict):
    res = str()
    for item in params.items():
        res += "`{}`='{}',".format(item[0], item[1])
    return res[:-1]


def get_where_format(params: dict):
    res = str()
    for item in params.items():
        res += "`{}`='{}' AND ".format(item[0], item[1])
    return res[:-4]


def get_update_format(table, params: dict, where_params: dict):
    req = "UPDATE {} SET {} WHERE {}".format(table, get_set_format(params), get_where_format(where_params))
    return req


class DataBase:
    """Создавать и использовать только в одной функции. Нельзя делать свойством другого класса."""

    def __init__(self):
        self.conn = sqlite3.connect("botdata.db")
        self.cursor = self.conn.cursor()
        self.create_all_tables()

    def create_all_tables(self):
        self.create_table_user()
        self.create_table_analytic()
        self.create_table_question()

    def create_default_table(self, name, properties_str):
        request_user = """CREATE TABLE IF NOT EXISTS {}\n(id INTEGER PRIMARY KEY AUTOINCREMENT""".format(name)
        for item in properties_str:
            request_user += ",\n{} TEXT".format(item)
        request_user += ");"
        self.cursor.execute(request_user)

    def create_table_user(self):
        obj = User(-1)
        properties_str = [variable for variable in dir(obj) if not variable.startswith('__') and
                          not callable(getattr(obj, variable)) and not variable.startswith('id')]
        self.create_default_table("user", properties_str)

    def create_table_analytic(self):
        obj = Analytic(-1)
        properties_str = [variable for variable in dir(obj) if not variable.startswith('__') and
                          not callable(getattr(obj, variable)) and not variable.startswith('id')]
        self.create_default_table("analytic", properties_str)

    def create_table_question(self):
        obj = Question(-1)
        properties_str = [variable for variable in dir(obj) if not variable.startswith('__') and
                          not callable(getattr(obj, variable)) and not variable.startswith('id')]
        self.create_default_table("question", properties_str)

    def execute_and_commit(self, request):
        """Выполняет request в БД MySQL"""
        print(request)
        my_file = open("log.txt", 'a')
        my_file.write(datetime.datetime.now().strftime("[%d-%m-%Y | %H:%M:%S] ") + request + "\n")
        my_file.close()
        self.cursor.execute(request)
        self.conn.commit()

    def add_item(self, table, params: dict):
        """Добавляет в таблицу какие-либо данные ( params )"""
        try:
            request_insert = get_insert_format(table, params)
            self.execute_and_commit(request_insert)
        except:
            pass

    def update_item(self, table, params: dict, where_params: dict):
        """Обновляет в таблице одну строку"""
        request_insert = get_update_format(table, params, where_params)
        self.execute_and_commit(request_insert)

    def select_item(self, table, search_id=None):
        """Выбирает в таблице строку с нужным id
        Требуется переделать под общие параметры"""
        request = "SELECT * FROM {}".format(table)
        if search_id is not None:
            request += " WHERE `id`='{}';".format(search_id)
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def delete_item(self, table: str, search_id):
        request = "DELETE FROM {} WHERE id == {}".format(table, search_id)
        self.execute_and_commit(request)

    def is_exist(self, table, search_parameter_name, search_parameter_value):
        request = "SELECT * FROM {} WHERE `{}`={}".format(table, search_parameter_name, search_parameter_value)
        self.cursor.execute(request)
        if self.cursor.fetchall():
            return True
        return False

    # Специализированные методы

    # Общие

    def is_exist_obj(self, table, obj_id):
        """Существует ли пользователь с obj_id в таблице"""
        if self.select_item(table, obj_id):
            return True
        return False

    def add_obj(self, table, obj, autoincrement=False):
        """Добавляет пользователя с id"""
        if obj.id is not None:
            if self.is_exist(table, "id", obj.id):
                return
        properties = {variable: 0 for variable in dir(obj) if not variable.startswith('__') and
                      not callable(getattr(obj, variable))}
        for key, val in zip(properties.keys(), [a for a in obj.get_properties()]):
            properties[key] = val
        if autoincrement:
            properties.pop("id")
        self.add_item(table, params=properties)

    def update_obj(self, table, obj):
        """Обновляет объект с id. Если в таблице нет такого объекта - создает новый
        TODO: Требуется переделать, считает параметры в алфавитном порядке.
        """
        # if not self.is_exist_user(obj.id):
        #     self.add_user(obj)
        properties = {variable: 0 for variable in dir(obj) if not variable.startswith('__') and
                      not callable(getattr(obj, variable))}
        for key, val in zip(properties.keys(), [a for a in obj.get_properties()]):
            properties[key] = val
        where = {"id": obj.id}
        self.update_item(table, properties, where)

    def delete_obj(self, table, obj):
        """Удаляет объект с obj.id"""
        if self.is_exist_user(obj.id):
            self.delete_item(table, obj.id)

    # Пользователь

    def is_exist_user(self, user_id):
        """Существует ли пользователь с user_id в таблице"""
        return self.is_exist_obj("user", user_id)

    def add_user(self, user: User):
        """Добавляет пользователя с user.id"""
        self.add_obj("user", user)

    def update_user(self, user: User):
        """Обновляет пользователя с user.id. Если в таблице нет такого пользователя - создает нового"""
        self.update_obj("user", user)

    def delete_user(self, user_id):
        """Удаляет пользователя с user_id"""
        self.delete_obj("user", User(user_id))

    def get_user(self, user_id):
        user_data = self.select_item("user", user_id)
        if not len(user_data):
            return None
        user_data = user_data[0]
        new_data = (*user_data[0:2], user_data[2:5], *user_data[5:])
        return User(*new_data)

    def get_user_role(self, role=None):
        table = "user"
        request = "SELECT * FROM {}".format(table)
        if role is not None:
            request += " WHERE `role`='{}';".format(role)
        self.cursor.execute(request)
        users = list()
        for user_data in self.cursor.fetchall():
            new_data = (*user_data[0:2], user_data[2:5], *user_data[5:])
            users.append(User(*new_data))
        return users

    def get_users_by_name(self, name):
        request = "SELECT * FROM user WHERE `name` LIKE '%{}%';".format(name)
        self.cursor.execute(request)
        users = list()
        for user_data in self.cursor.fetchall():
            new_data = (*user_data[0:2], user_data[2:5], *user_data[5:])
            users.append(User(*new_data))
        return users

    # Аналитик

    def is_exist_analytic(self, analytic_id):
        """Существует ли аналитик с analytic_id в таблице"""
        return self.is_exist_obj("analytic", analytic_id)

    def add_analytic(self, analytic: Analytic):
        """Добавляет аналитика с analytic.id"""
        self.add_obj("analytic", analytic)

    def update_analytic(self, analytic: Analytic):
        """Обновляет аналитика с analytic.id. Если в таблице нет такого аналитика - создает нового"""
        self.update_obj("analytic", analytic)

    def update_analytic_qsolved(self, analytic_id):
        """Обновляет аналитика с analytic.id. Если в таблице нет такого аналитика - создает нового"""
        item = self.get_analytic(analytic_id)
        item.question_solved = int(item.question_solved) + 1
        self.update_obj("analytic", item)

    def delete_analytic(self, analytic_id):
        """Удаляет аналитика с analytic_id"""
        self.delete_obj("analytic", Analytic(analytic_id))

    def get_analytic(self, analytic_id=None):
        """Выдает аналитков из БД"""
        if analytic_id is None:
            request = "SELECT * FROM {}".format("analytic")
            self.cursor.execute(request)
            analytic_data = self.cursor.fetchall()
            res = []
            for data in analytic_data:
                res.append(Analytic(*data))
            return res
        else:
            analytic_list = self.select_item("analytic", analytic_id)
            if len(analytic_list) > 0:
                return Analytic(*analytic_list[0])
            else:
                return None

    # Вопросы

    def is_exist_question(self, question_id):
        """Существует ли вопрос с user_id в таблице"""
        return self.is_exist_obj("question", question_id)

    def add_question(self, question: Question):
        """Добавляет вопрос с question.id"""
        ai = question.id is None
        self.add_obj("question", question, autoincrement=ai)

    def update_question(self, question: Question):
        """Обновляет вопрос с question.id. Если в таблице нет такого вопроса - создает новый"""
        self.update_obj("question", question)

    def delete_question(self, question_id):
        """Удаляет вопрос с question_id"""
        self.delete_obj("question", Question(question_id))

    def get_question(self, question_id=None, status=0):
        """Выдает вопросы из БД"""
        if question_id is None:
            request = "SELECT * FROM {}".format("question")
            request += " WHERE `status`='{}';".format(status)
            self.cursor.execute(request)
            question_data = self.cursor.fetchall()
            res = []
            for data in question_data:
                res.append(Question(*data))
            return res
        else:
            question_list = self.select_item("question", question_id)
            if len(question_list) > 0:
                return Question(*question_list[0])
            else:
                return None


# Чисто поиграться


def main():
    db = DataBase()
    db.add_user(User(1243, "Misha"))
    db.update_user((User(1243, "Lexa")))
    db.add_question(Question(1))


if __name__ == '__main__':
    main()
