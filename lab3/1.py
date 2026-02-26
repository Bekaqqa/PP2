a = int(input())
sum = 0
c = a
for i in range(len(str(a))):
    b = a%10
    if b%2 == 0:
        sum += 1
    a = a//10
if sum == len(str(c)):
    print("Valid")
else:
    print("Not valid")