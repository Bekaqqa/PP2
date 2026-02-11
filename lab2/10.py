a = int(input())
b = list(map(int , input().split()))
b.sort(reverse=True)
for i in range(a):
    print(b[i], end=" ")