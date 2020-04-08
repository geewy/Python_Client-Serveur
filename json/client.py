#!/usr/bin/env python3
# coding: utf-8

"""
Client pour les RPC exigées par le serveur
usage :
  "./client rot13 'yourstring'"
  "./client listdir '/tmp' --recursive"
"""

import sys
import logging
import argparse
import socket
import json

INTRO = "Welcome stranger !!"
logger = logging.getLogger(__file__)

def main(arguments):
  "our logic"
  if arguments.debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)
  
  function = arguments.function[0]
  args = arguments.args
  
  if "listdir" == function:
    if arguments.recursive:
      if False:
        function = "list_files2"
      else:
        function = "list_files3"
    else:
      function = "list_files"
  
  host, port = arguments.host[0], arguments.port[0]
  logger.debug("Connect to %s %s", host, str(port))
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
    so.connect((host, port))
    logger.info("=> %s %s", function, str(args))
    j = {
        "function": function,
        "args": args,
    }
    command = json.dumps(j)
    so.sendall(command.encode("utf-8"))
    response = so.recv(8192).decode("utf-8")
    logger.info("<= %s", response)
  
  return 0

if "__main__" == __name__:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("-d", "--debug", action="store_true", help="debug infos")
  parser.add_argument("-r", "--recursive", action="store_true", help="Recursive command")
  parser.add_argument("-H", "--host", type=str, nargs=1, default=["127.0.0.1"], help="option server argument")
  parser.add_argument("-p", "--port", type=int, nargs=1, default=[7777], help="option port argument")
  parser.add_argument("function", type=str, nargs=1, default=None, help="function name")
  parser.add_argument("args", type=str, nargs="*", default=[], help="arguments")
  arguments = parser.parse_args(sys.argv[1:])
  sys.exit(main(arguments))
