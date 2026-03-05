# 1. Подсчёт созданных объектов
class User:
    count = 0

    def __init__(self, name):
        self.name = name
        User.count += 1

# 2. Общая валюта для всех заказов
class Order:
    currency = "RUB"

    def __init__(self, price):
        self.price = price

# 3. Максимальный уровень
class Game:
    max_level = 10

    def __init__(self, level):
        self.level = level

# 4. Общий список учеников
class School:
    students = []

    def add_student(self, name):
        self.students.append(name)

# 5. Статус по умолчанию
class Task:
    status = "new"

    def __init__(self, title):
        self.title = title