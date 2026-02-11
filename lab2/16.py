n = int(input())
b = list(map(int , input().split()))
unique = []
for i in range(n):
    if b[i] not in unique:
        unique.append(b[i])
    else:
        unique.append(0)
for i in range(n):
    if unique[i]!=0:
        print("YES")
    else:
        print("NO")