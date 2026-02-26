import math
a , b = map(int, input().split())
c , d = map(int, input().split())
e , f = map(int, input().split())
g = math.sqrt((c-e)**2 + (d-f)**2)

print(f"({a}, {b})")
print(f"({c}, {d})")
print(f"{g:.2f}")