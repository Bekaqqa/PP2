#1
import re
text = input()
pattern = r"ab*"
if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")

#2
import re
text = input()
pattern = r"ab{2,3}"
if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")

#3
import re
text = input()
pattern = r"[a-z]+_[a-z]+"
print(re.findall(pattern, text))

#4
import re
text = input()
pattern = r"[A-Z][a-z]+"
print(re.findall(pattern, text))

#5
import re
text = input()
pattern = r"a.*b"
if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")

#6
import re
text = input()
result = re.sub(r"[ ,\.]", ":", text)
print(result)

#7
import re
text = input()
result = re.sub(r'_([a-z])', lambda x: x.group(1).upper(), text)
print(result)

#8
import re
text = input()
result = re.split(r'(?=[A-Z])', text)
print(result)

#9
import re
text = input()
result = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)
print(result)

#10
import re
text = input()
result = re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()
print(result)