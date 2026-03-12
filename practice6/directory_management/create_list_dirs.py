import os

#1
dir_name = "my_folder"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
    print(f"Example 1: Directory '{dir_name}' created")
else:
    print(f"Example 1: Directory '{dir_name}' already exists")
print()

#2
dirs = ["folder1", "folder2", "folder3"]
for d in dirs:
    if not os.path.exists(d):
        os.mkdir(d)
        print(f"Example 2: Directory '{d}' created")
    else:
        print(f"Example 2: Directory '{d}' already exists")
print()

#3
print("Example 3: List all items in current folder")
for item in os.listdir("."):
    print(item)
print()

#4
print("Example 4: List only directories")
for item in os.listdir("."):
    if os.path.isdir(item):
        print(item)
print()

#5
check_dir = "folder2"
if os.path.exists(check_dir) and os.path.isdir(check_dir):
    print(f"Example 5: Directory '{check_dir}' exists")
else:
    print(f"Example 5: Directory '{check_dir}' does not exist")