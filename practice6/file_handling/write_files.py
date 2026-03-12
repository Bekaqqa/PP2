#1
with open("demofile.txt", "a") as f:
  f.write("Now the file has more content!")

#open and read the file after the appending:
with open("demofile.txt") as f:
  print(f.read())

#2
with open("demofile.txt", "w") as f:
  f.write("Woops! I have deleted the content!")

#open and read the file after the overwriting:
with open("demofile.txt") as f:
  print(f.read())

#3
f = open("myfile.txt", "x")

#4
# Open and read the file line by line
with open("demofile.txt", "r") as f:
    for line in f:
        print(line.strip())  # .strip() removes the newline character