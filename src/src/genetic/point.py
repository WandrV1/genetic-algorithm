import math


class Point:
    def __init__(self, x: int, y: int):
        """
        Инициализация точки
        :param x: Координата x
        :param y: Координата y
        """
        self.x = x
        self.y = y

    def get_coord(self):
        """
        Вернуть координаты точки
        :return: Список из x и y координаты
        """
        return [self.x, self.y]

    def __str__(self):
        """
        Метод toStr
        :return: Строковое представление точки
        """
        return f"x: {self.x}, y: {self.y}"

    def __eq__(self, other):
        """
        Метод equals
        :param other: Другая точка
        :return: True если точки одинаковы, False в иных случаях
        """
        if not isinstance(other, Point):
            return False
        else:
            return self.x == other.x and self.y == other.y

    def distance(self, other) -> float:
        """
        Расстояние до полученной точки
        :param other: Другая точка
        :return: Расстояние между точками
        """
        return math.hypot(self.x - other.x, self.y - other.y)