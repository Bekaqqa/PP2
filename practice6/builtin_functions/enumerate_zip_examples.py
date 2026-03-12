#1
fruits = ["apple", "banana", "cherry"]
print("Example 1: enumerate()")
for i, fruit in enumerate(fruits):
    print(i, fruit)
print()

#2
print("Example 2: enumerate() with start=1")
for i, fruit in enumerate(fruits, start=1):
    print(i, fruit)
print()

#3
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
print("Example 3: zip()")
for name, age in zip(names, ages):
    print(name, age)
print()

#4
colors = ["red", "green"]
print("Example 4: zip() with different lengths")
for name, color in zip(names, colors):
    print(name, color)
print()

#5
scores = [90, 85, 92]
print("Example 5: enumerate() with zip()")
for i, (name, score) in enumerate(zip(names, scores), start=1):
    print(i, name, score)