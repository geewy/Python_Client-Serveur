#!/usr/bin/env python3
# coding: utf-8

"""
Le serveur écoute sur une socket TCP et fournit les API suivantes :
    • help('function') : retourne une documentation pour la fonction 
    'function', si le nom n'est pas fourni, retourne une aide globale
    • functions() : retourne la liste des fonctions disponibles
    • rot13(string) : retourne la chaîne de caractères encodées en rot13
    • max_even(int1, ...) : retourne le plus grand entier pair
    • calls() : retourne le nombre d'appels résolus depuis le démarrage
    du serveur (celui-ci compris)
    • file_exists(filename, [path]) : retourne True si le fichier existe.
    La recherche est faite dans le chemin indiqué en paramètre ou dans le 
    dossier courant si aucun chemin n'est fourni
    • list_files(path) : retourne une liste des fichiers présents dans le 
    dossier 'path'
    • list_files2(path, recursive) : liste les fichiers de façon récursive
    • list_files3(path, recursive) : pareil que list_files2 mais utilise la
    commande "dir"
"""

import sys
import os
import logging
import argparse
import functools
import socketserver
import json
import codecs
import recursivels

BUFFSIZE = 4096
logger = logging.getLogger(__file__)
calls = 0

def debug(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        logger.debug("Function %s called", f.__name__)
        return f(*args, **kwargs)
    return inner
    
def record_call(f):
    def inner(*args, **kwargs):
        global calls
        calls += 1
        return f(*args, **kwargs)
    return inner
    
class Commands:
    def __init__(self):
        self.commands = {
            "help": (self.help, "Online help for the given function, example: help('function')"),
            "functions": (self.functions, "Return the list of the avalaible functions"),
            "rot13": (self.rot13, "Return the string encoded with rot13"),
            "max_even": (self.max_even, "Return the greater even integer"),
            "calls": (self.calls, "Return the number of calls resolved since the starting of the server (including this one)"),
            "list_files": (self.list_files, "Return the files' list of the path repository"),
            "list_files2": (self.list_files2, "Recursive list of the files"),
            "list_files3": (self.list_files3, "Same as list_files2 but use the system command dir"),
        }
    
    def execute(self, data):
        j = json.loads(data)
        print(j)
        function = j["function"]
        args = j["args"]
        logger.debug("function %s args %s", function, str(atgs))
        if function in self.commands:
            logger.debug("Calling function %s", function)
            callback, _ = self.commands[function]
            r = callback(args)
        else:
            r = "Unknown function"
        return r
        
    @record_call
    @debug
    def help(self, args):
        if len(args):
            function = args[0]
            if function in self.commands:
                _, r = self.commands[function]
            else:
                r = "Unknown function %s" % function
        else:
            r = """Usage: help 'function' This server executes the following functions : %s""" % __doc__
        return r
        
    @record_call
    def functions(self, args):
        r = " ".join(list(self.commands))
        return r
    
    @record_call
    def rot13(self, args):
        r = ""
        if len(args):
            r = codecs.encode(args[0], encoding="rot13")
        return r
    
    @record_call
    def max_even(self, args):
        l = [int(x, 0) for x in args]
        m = max([x for x in l if 0 == x % 2])
        r = str(m)
        return r
    
    @record_call
    def calls(self, args):
        global calls
        r = "%i calls so far ..." % calls
        return r
        
    @record_call
    def list_files(self, args):
        r = ""
        if len(args):
            path = args[0]
            logger.debug("Listing directory %s files", path)
            if os.path.isdir(path):
                l = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
                r = " ".join(l)
        return r
        
    @record_call
    def list_files2(self, args):
        r = ""
        if len(args):
            path = args[0]
            logger.debug("Listing directory %s files recursivly", path)
            for root, dirs, files in os.walk(path):
                for f in files:
                    fullname = os.path.join(root, f)
                    r += " " + fullname
        return r
        
    @record_call
    def list_files3(self, args):
        r = ""
        if len(args):
            path = args[0]
            logger.debug("Listing directory %s files recursivly, ls-based", path)
            out, err = recursivels.run(path)
            r += "Output\n" + out + "\n"
            r += "Errors\n" + err + "\n"
        return r

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUFFSIZE).decode("utf-8")
        data = data.strip()
        logger.debug("From %s %s %s", str(self.client_address[0]), str(self.client_address[1]), data)
        if len(data):
            cmd = Commands()
            r = cmd.execute(data)
            logger.debug("Reply %s", r)
            r += "\r\n"
            self.request.sendall(r.encode("utf-8"))
            
class MyTCPServer(socketserver.TCPServer):
    def __init__(self, *args, **kwargs):
        self.allow_reuse_address = True
        super().__init__(*args, **kwargs)
        
def main(arguments):
    "our logic"
    r = 0
    if arguments.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    host, port = arguments.server_name[0], arguments.port_number[0]
    with MyTCPServer((host, port), TCPHandler, blind_and_activate=True) as ts:
        logger.info("Serving on %s %i", host, port)
        ts.serve_forever()
    return r
    
if "__main__" == __name__:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-d", "--debug", action="store_true", help="debug infos")
    parser.add_argument("server_name", type=str, nargs=1, default=None, help="Mandatory server name argument")
    parser.add_argument("port_number", type=int, nargs=1, default=None, help="Mandatory port number agument")
    arguments = parser.parse_args(sys.argv[1:])
    sys.exit(main(arguments))
        
        
