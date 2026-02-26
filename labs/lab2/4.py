a = int(input())
b = list(map(int , input().split()))
cnt = 0
for i in range(a):
    if b[i]>0:
        cnt += 1
print(cnt)