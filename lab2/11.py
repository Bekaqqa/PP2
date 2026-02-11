a, b, c = map(int, input().split())
d = list(map(int, input().split()))
b -= 1
c -= 1
d[b:c+1] = d[b:c+1][::-1]
print(*d)
