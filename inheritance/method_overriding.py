# 1. Простое переопределение метода
class Animal:
    def speak(self):
        return "Animal sound"

class Dog(Animal):
    def speak(self):
        return "Woof"

# 2. Переопределение с вызовом родителя
class Vehicle:
    def move(self):
        return "Moving"

class Car(Vehicle):
    def move(self):
        return super().move() + " by car"

# 3. Изменение логики метода
class Shape:
    def area(self):
        return 0

class Square(Shape):
    def area(self):
        return 4 * 4

# 4. Переопределение метода с параметрами
class Printer:
    def print_text(self, text):
        return text

class UpperPrinter(Printer):
    def print_text(self, text):
        return text.upper()

# 5. Переопределение метода __str__
class Person:
    def __str__(self):
        return "Person"

class Student(Person):
    def __str__(self):
        return "Student"