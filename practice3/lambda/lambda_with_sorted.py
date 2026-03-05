# 1. Сортировка чисел по возрастанию
numbers = [5, 2, 9, 1, 7]
sorted_numbers = sorted(numbers, key=lambda x: x)
print("Sorted numbers:", sorted_numbers)

# 2. Сортировка чисел по убыванию
descending = sorted(numbers, key=lambda x: x, reverse=True)
print("Descending:", descending)

# 3. Сортировка строк по длине
words = ["apple", "kiwi", "banana", "fig"]
sorted_by_length = sorted(words, key=lambda w: len(w))
print("Sorted by length:", sorted_by_length)

# 4. Сортировка списка кортежей по второму элементу
pairs = [(1, 3), (2, 1), (4, 2)]
sorted_pairs = sorted(pairs, key=lambda x: x[1])
print("Sorted by second element:", sorted_pairs)

# 5. Сортировка списка словарей по возрасту
people = [
    {"name": "Anna", "age": 25},
    {"name": "Bob", "age": 20},
    {"name": "Charlie", "age": 30}
]

sorted_people = sorted(people, key=lambda person: person["age"])
print("Sorted by age:", sorted_people)