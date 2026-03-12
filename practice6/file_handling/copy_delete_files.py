#1
import os
os.remove("demofile.txt")

#2
import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")

#3
import os
os.rmdir("myfolder")

#4
import os

# Check if the file exists before trying to delete it
if os.path.exists("demofile.txt"):
    os.remove("demofile.txt")
    print("file deleted successfully.")
else:
    print("The file does not exist.")