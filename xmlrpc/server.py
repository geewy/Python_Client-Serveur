#!/usr/bin/env python3

import os
import sys
import codecs
import threading
import logging

from xmlrpc.server import SimpleXMLRPCServer
from functools import wraps

call_counter = 0

def counted(f):
  @wraps(f)
  def inner(*args, **kwargs):
    global call_counter
    call_counter += 1
    return f(*args, **kwargs)
  return inner
  
@counted
def max_even(*args):
  """
  computer the greater even integer from params
  :param args: a list of integers
  :return: greater even integer or 0
  """
  try:
    return max([x for x in args if x % 2 == 0])
  except Exception as exc:
    logging.error("an error occured : %s", exc)
    return 0
  
@counted
def rot13(input):
  """
  encode a string with rot13
  :param args: input string to encoded
  :return: rot13 encoded string
  """
  return codecs.encode(input, "rot13")
  
@counted
def calls():
  """
  count the calls made
  :return: the calls counted
  """
  return call_counter
  
@counted
def file_exists(filename, path=None):
  if path is not None:
    filename = os.path.join(path, filename)
  return os.path.exists(filename)
  
@counted
def list_files(path=None):
  try:
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
  except Exception as exc:
    logging.error("could not list files in %r : %r", path, exc)
    return []
    
functions = {"max_even": max_even, "rot13": rot13, "calls": calls, "file_exists": file_exists, "list_files": list_files}

def main():
  server = SimpleXMLRPCServer(("localhost", 8001"))
  @counted
  def _exit(*args):
    server.server_close()
    def stop():
      server.shutdown()
    t = threading.Thread(target=stop)
    t.start()
    return 0
  
  server.register_introspection_functions()
  server.register_function(_exit, "exit")
  for func_name, func in functions.items():
    server.register_function(func, func_name)
  server.serve_forever()
  
if __name__==__"__main__":
  sys.exit(main())
