# 1. Фильтрация четных чисел
numbers = [1, 2, 3, 4, 5, 6]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even:", even_numbers)

# 2. Фильтрация чисел больше 10
nums = [5, 12, 7, 18, 3]
greater_than_10 = list(filter(lambda x: x > 10, nums))
print("Greater than 10:", greater_than_10)

# 3. Фильтрация строк длиннее 4 символов
words = ["cat", "house", "car", "elephant"]
long_words = list(filter(lambda w: len(w) > 4, words))
print("Long words:", long_words)

# 4. Фильтрация положительных чисел
values = [-3, -1, 0, 2, 5]
positive = list(filter(lambda x: x > 0, values))
print("Positive:", positive)

# 5. Фильтрация слов, начинающихся с буквы 'a'
items = ["apple", "banana", "avocado", "cherry"]
starts_with_a = list(filter(lambda x: x.startswith("a"), items))
print("Starts with 'a':", starts_with_a)