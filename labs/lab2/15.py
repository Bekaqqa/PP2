n = int(input())
names = []

for _ in range(n):
    names.append(input().strip())

names.sort()

cnt = 0
for i in range(n):
    if i == 0 or names[i] != names[i - 1]:
        cnt += 1

print(cnt)
