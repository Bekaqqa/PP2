#1
import gc

# Включаем сборку мусора
gc.enable()

# Выводим количество объектов в каждом поколении
gen_counts = gc.get_count()
print("Объекты в поколениях (0,1,2):", gen_counts)

#2
import gc

# Создаём несколько объектов
a = [1, 2, 3]
b = [4, 5, 6]

print("До сборки:", gc.get_count())

# Принудительно запускаем сборку поколения 0
collected = gc.collect(0)
print(f"Собрано объектов в поколении 0: {collected}")
print("После сборки:", gc.get_count())

#3
import gc

class Node:
    def __init__(self):
        self.ref = None

# Создаём цикл
x = Node()
y = Node()
x.ref = y
y.ref = x

# Удаляем ссылки
del x
del y

# До сборки мусора
print("До сборки:", gc.get_count())

# Собираем мусор (удаляем циклические объекты)
gc.collect()
print("После сборки:", gc.get_count())

#4
import gc

# Создаём список объектов
objs = [list(range(1000)) for _ in range(10)]

print("До сборки:", gc.get_count())

# Несколько сборок — объекты перемещаются в старшие поколения
for i in range(3):
    gc.collect()
    print(f"После сборки {i+1}:", gc.get_count())

#5
import gc
# Включаем отладку для отслеживания объектов, которые не были собраны
gc.set_debug(gc.DEBUG_UNCOLLECTABLE)
# Создаём объекты с циклическими ссылками
class A:
    def __init__(self):
        self.ref = None
a1 = A()
a2 = A()
a1.ref = a2
a2.ref = a1
# Удаляем ссылки
del a1
del a2
# Собираем мусор
gc.collect()
# Проверяем наличие не собранных объектов
print("Невозможно собрать объекты:", gc.garbage)
