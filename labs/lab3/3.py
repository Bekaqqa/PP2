numbers ={
    "ONE" : "1",
    "TWO" : "2",
    "THR" : "3",
    "FOU" : "4",
    "FIV" : "5",
    "SIX" : "6",
    "SEV" : "7",
    "EIG" : "8",
    "NIN" : "9",
    "ZER" : "0"
}
a = input()
rev_numbers = {v:k for k,v in numbers.items()}
for i in "+-*/":
    if i in a:
        left, right = a.split(i)
        break

def triplets_to_num(s):
    return int("".join(numbers[s[i:i+3]] for i in range(0,len(s),3)))

n1 = triplets_to_num(left)
n2 = triplets_to_num(right)

res = n1+n2 if i=="+" else n1-n2 if i=="-" else n1*n2

print("".join(rev_numbers[d] for d in str(res)))