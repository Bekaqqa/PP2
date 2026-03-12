import shutil
import os

#1
shutil.move("file1.txt", "my_folder")
print("Example 1: file1.txt moved to my_folder")

#2
shutil.move("file2.txt", "my_folder/renamed_file2.txt")
print("Example 2: file2.txt moved and renamed")

#3
files = ["file3.txt", "file4.txt"]
for f in files:
    shutil.move(f, "my_folder")
    print(f"Example 3: {f} moved to my_folder")

#4
if not os.path.exists("text_files"):
    os.mkdir("text_files")
for f in os.listdir("."):
    if f.endswith(".txt"):
        shutil.move(f, "text_files")
        print(f"Example 4: {f} moved to text_files")

#5
shutil.move("my_folder/file1.txt", ".")
print("Example 5: file1.txt moved back to current folder")