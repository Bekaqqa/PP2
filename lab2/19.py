a = int(input())
b = {}
for i in range(a):
    name, series = input().split()
    series = int(series)
    if name in b:
        b[name]+= series
    else:
        b[name] = series
    
for i in sorted(b):
    print(i, b[i])