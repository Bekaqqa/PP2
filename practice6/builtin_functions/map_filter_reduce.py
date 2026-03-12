from functools import reduce

#1
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))
print("Example 1: map() squares:", squares)

#2
str_numbers = list(map(str, numbers))
print("Example 2: map() to strings:", str_numbers)

#3
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Example 3: filter() evens:", evens)

#4
greater_than_3 = list(filter(lambda x: x > 3, numbers))
print("Example 4: filter() >3:", greater_than_3)

#5
sum_numbers = reduce(lambda x, y: x + y, numbers)
print("Example 5: reduce() sum:", sum_numbers)