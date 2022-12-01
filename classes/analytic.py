class Analytic:
    """Класс аналитика"""

    def __init__(self, id, name=None, qs=0):
        self.id = id
        self.name = name
        self.question_solved = qs

    def get_properties(self):
        return [self.id, self.name, self.question_solved]

    def __str__(self):
        text = "{}\nРешил вопросов: {}".format(self.name if self.name else "Нет имени",
                                               self.question_solved)
        return text
