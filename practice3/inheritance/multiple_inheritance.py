# 1. Два родительских класса
class Fly:
    def move(self):
        return "Flying"

class Swim:
    def move(self):
        return "Swimming"

class Duck(Fly, Swim):
    pass

# 2. Методы из разных классов
class Read:
    def read(self):
        return "Reading"

class Write:
    def write(self):
        return "Writing"

class Student(Read, Write):
    pass

# 3. Переопределение метода при множественном наследовании
class A:
    def action(self):
        return "A"

class B:
    def action(self):
        return "B"

class C(A, B):
    def action(self):
        return "C"

# 4. Использование super()
class Parent1:
    def hello(self):
        return "Hello from Parent1"

class Parent2:
    def hello(self):
        return "Hello from Parent2"

class Child(Parent1, Parent2):
    def hello(self):
        return super().hello()

# 5. Общие атрибуты
class Engine:
    power = 100

class Electric:
    battery = 80

class Car(Engine, Electric):
    pass