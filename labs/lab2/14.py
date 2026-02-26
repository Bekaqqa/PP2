a = int(input())
b = list(map(int , input().split()))
maxcnt = 0
maxval = 9999
for i in range(a):
    cnt = 0
    for j in range(a):
        if b[i] == b[j]:
            cnt += 1
    if cnt > maxcnt or (cnt == maxcnt and b[i] < maxval):
        maxcnt = cnt
        maxval = b[i]

print(maxval)