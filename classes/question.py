class Question:
    """Класс вопроса. Хранит в себе данные, имеет статус."""

    def __init__(self, id=None, comment=None, from_analytic=None, from_user=None, status=None, text=None):
        self.id = id
        self.from_user = from_user
        self.from_analytic = from_analytic
        self.text = text
        self.status = status
        self.comment = comment

    def get_properties(self):
        return [self.comment, self.from_analytic, self.from_user, self.id, self.status, self.text]
        # Требуется в алфавитном порядке

    def __str__(self):
        return self.text
