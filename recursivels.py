#!/usr/bin/env python3
# coding: utf-8

import os
import subprocess

def run(path):
  if os.path.isdir(path):
    command = ["/bin/ls", "--recursive", path,]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    (out, err) = p.communicate(input=None)
    return out.decode("utf-8"), err.decode("utf-8")
    
  else:
    return None
    
if "__main__" == __name__:
  print(run("/etc"))
