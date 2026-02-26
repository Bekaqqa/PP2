numbers = list(map(int, input().split()))
b = []
for i in numbers:
    cnt = 0
    for j in range(1, i+1):
        if i%j==0:
            cnt+=1
    if cnt==2:
        b.append(i)

if len(b) == 0:
    print("No primes")

else:
    print(*b)