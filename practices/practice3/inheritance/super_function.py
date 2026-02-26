# 1. Вызов метода родителя
class Animal:
    def speak(self):
        return "Animal sound"

class Cat(Animal):
    def speak(self):
        return super().speak() + " meow"

# 2. super() в __init__
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

# 3. Добавление логики к методу
class Vehicle:
    def start(self):
        return "Vehicle started"

class Car(Vehicle):
    def start(self):
        return super().start() + " with engine"

# 4. super() при множественном наследовании
class A:
    def action(self):
        return "A"

class B(A):
    def action(self):
        return super().action() + " B"

class C(B):
    def action(self):
        return super().action() + " C"

# 5. super() и переопределение
class Shape:
    def draw(self):
        return "Drawing shape"

class Circle(Shape):
    def draw(self):
        return super().draw() + " circle"