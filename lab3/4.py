a = input()
b = []
for i in range (len(a)):
    c = a[i]
    if c.isalpha():
        c = c.upper()
        b.append(c)
    else:
        b.append(c)
for i in range (len(b)):
    print(b[i], end="")
