import os

print os.getcwd()

print os.path.relpath("dir1")
print os.path.relpath(os.getcwd()+"/..")