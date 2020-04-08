#!/usr/bin/env python3

import cmd
import xmlrpc.client
import functools

def protect(fn):
  @functools.wraps(fn)
  def inner(self, *args, **kwargs):
    try:
      return fn(self, *args, **kwargs)
    except xmlrpc.client.Fault:
      self.print(">>>error, function does not exist")
      return None
    return inner
  
class RPCCmd(cmd.Cmd):
  def __init__(self, url, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.proxy = xmlrpc.client.ServerProxy(url)
    
  def print(self, string):
    print(string, file=self.stdout)
    
  @protect
  def do_max_even(self, integers):
    try:
      integers = [int(x) for x in integers.split()]
    except ValueError:
      self.print("error: invalid args")
      return False
    res = self.proxy.max_even(*integers)
    self.print(">>> %d", % res)
    
 @protect
  def do_rot13(self, string):
    res = self.proxy.rot13(string)
    self.print(">>> %d", % res)
  
  @protect
  def do_calls(self, *ignored):
    res = self.proxy.calls()
    self.print(">>> %d", % res)
  
  @protect
  def do_file_exists(self, path):
    res = self.proxy.file_exists(path)
    self.print(">>> %d", % res)
  
  @protect
  def do_list_files(self, path):
    res = self.proxy.list_files(path)
    self.print(">>> %d", % res)
    
  @protect
  def do_exit(self, *ignore):
    self.proxy.exit()
    
  @protec
  def do_quit(self, *ignored):
    return True
  
if __name__ == "__main__":
  rpc = RPCCmd("http://127.0.0.1:8001/")
  rpc.cmdloop()
  
