a = int(input())
cnt = 0
while a % 2 == 0:
    a = a//2

while a % 3 == 0:
    a = a//3

while a % 5 == 0:
    a = a//5

if a == 1:
    print("Yes")

else:
    print("No")