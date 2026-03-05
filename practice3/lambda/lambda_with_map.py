# 1. Возведение чисел в квадрат
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x ** 2, numbers))
print("Squares:", squares)

# 2. Умножение чисел на 10
nums = [3, 7, 9]
multiplied = list(map(lambda x: x * 10, nums))
print("Multiplied by 10:", multiplied)

# 3. Преобразование строк в верхний регистр
words = ["cat", "dog", "bird"]
upper_words = list(map(lambda w: w.upper(), words))
print("Uppercase:", upper_words)

# 4. Получение длины строк
items = ["apple", "kiwi", "banana"]
lengths = list(map(lambda x: len(x), items))
print("Lengths:", lengths)

# 5. Сложение элементов двух списков
list1 = [1, 2, 3]
list2 = [4, 5, 6]
summed = list(map(lambda x, y: x + y, list1, list2))
print("Summed lists:", summed)