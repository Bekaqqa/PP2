#1
class Student(Person):
  pass

#2
x = Student("Mike", "Olsen")
x.printname()

#3
class Student(Person):
  def __init__(self, fname, lname):
    #add properties etc.

#4
class Student(Person):
  def __init__(self, fname, lname):
    Person.__init__(self, fname, lname)

#5
class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)