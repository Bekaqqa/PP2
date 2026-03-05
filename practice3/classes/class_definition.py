# 1. Простейший класс
class Person:
    pass

# 2. Класс с атрибутами
class Car:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

# 3. Класс с методом
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        return "Woof!"

# 4. Класс с методом, использующим атрибуты
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def is_passed(self):
        return self.grade >= 60

# 5. Класс с переменной класса
class Counter:
    total = 0

    def __init__(self):
        Counter.total += 1