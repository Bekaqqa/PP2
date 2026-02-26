parts = input().split()

a = parts[0]
b = parts[1]
c = int(parts[2])

if a == "Manager":
    d = int(parts[3])
    proc = c + (c * d / 100)
    print(f"Name: {b}, Total: {proc:.2f}")

elif a == "Developer":
    d = int(parts[3])
    proc = c + 500 * d
    print(f"Name: {b}, Total: {proc:.2f}")

else:
    print(f"Name: {b}, Total: {c:.2f}")