class User:
    """Класс пользователя"""

    def __init__(self, id, name=None, qdata=None, role=None, root=3):  # Кто сколько вопросов сделал
        self.id = id
        self.name = name
        self.role = role
        self.root = root
        self.question_count = 0
        self.question_accepted = 0
        self.question_denied = 0
        if qdata is not None:
            if len(qdata) == 3:
                self.question_count = qdata[0]
                self.question_accepted = qdata[1]
                self.question_denied = qdata[2]

    def get_properties(self):
        return [self.id, self.name, self.question_accepted, self.question_count, self.question_denied, self.role,
                self.root]

    def __str__(self):
        text = "{}, {}".format(self.name if self.name else "Нет имени",
                               self.role if self.role else "Нет роли")
        return text
