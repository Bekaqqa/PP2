a = int(input())
b = list(map(int , input().split()))
for i in range(a):
    b[i]=b[i]**2
for i in range(a):
    print(b[i], end=" ")