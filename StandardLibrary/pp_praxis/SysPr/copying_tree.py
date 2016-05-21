
import os
import shutil
from exceptions import RuntimeError

def copy_tree(dir_source,dir_target):
  if not(os.path.exists(dir_source) and os.path.isdir(dir_source)):
    raise RuntimeError("Source directory doesn't exists")
  
  if not(os.path.exists(dir_target) and os.path.isdir(dir_target)):
    os.mkdir(dir_target)
  
  for name in os.listdir(dir_source):
    args = (os.path.join(dir_source,name),os.path.join(dir_target,name))
    if os.path.isdir(args[0]):
      copy_tree(*args)
    else:
      shutil.copyfile(*args)
      
   

if __name__ == "__main__":

  dir_source = raw_input("Source directory?\n")
  dir_target = raw_input("Target directory?\n")
  
  copy_tree(dir_source,dir_target)
  