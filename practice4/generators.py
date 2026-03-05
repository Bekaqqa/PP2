#1
def my_generator():
    yield 1
    yield 2
    yield 3

for value in my_generator():
    print(value)

#2
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

for number in count_up_to(5):
    print(number)

#3
def squares(n):
    for i in range(n):
        yield i * i

for s in squares(6):
    print(s)

#4
def even_numbers(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

for num in even_numbers(10):
    print(num)

#5
numbers = (x * 2 for x in range(5))

for num in numbers:
    print(num)