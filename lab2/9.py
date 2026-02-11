a = int(input())
b = list(map(int , input().split()))
c = max(b)
d = min(b)
for i in range(a):
    if b[i] == c:
        b[i] = d
for i in range(a):
    print(b[i], end = " ")