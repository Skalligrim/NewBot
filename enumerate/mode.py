import enum


class Mode(enum.Enum):
    class Classic(enum.Enum):
        id = 0
        name = "Классический режим"

    class Suggestion(enum.Enum):
        id = 1
        name = "Режим рекомендаций"
