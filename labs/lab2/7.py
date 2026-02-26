a = int(input())
b = list(map(int , input().split()))
max = -999999
maxind = 0
for i in range(a):
    if b[i] > max:
        max = b[i]
        maxind = i+1
print(maxind)