# -*- coding: utf-8 -*-

"""
main of mabozen

command line

"""

import argparse

parser = argparse.ArgumentParser(description='mabozen command line.')

parser.add_argument('--noarg', action="store_false", default=True)

parser.add_argument('-j', '--tojson', dest='tojson', action='store_true',
                   help='from pg db schema to json', default=False)

parser.add_argument('-b', '--backup', dest='backup', action='store_true',
                   help='backup function from db', default=False)

parser.add_argument('-l', '--load', dest='load', action='store_true',
                   help='load function to db', default=False)
                   
parser.add_argument('-v', '--version', action='version', version='mabozen 0.0.1')                   
                   
args = parser.parse_args()

if args.noarg:
    logo = """
        \      /
        --**--
        | O O |  \\
        \     /   |\\
         [   ]
         - - -    
    """
    print logo
    print parser.parse_args(['-h'])

if args.tojson:
    
    from mabozen.schema2json import JsonModels
    
    print("to json")
    jsonm = JsonModels()
    jsonm.run()

if args.backup:
    
    from mabozen.pgfunc_backup import PgFunction
    
    print("backup")
    func = PgFunction()
    func.backup()
    
if args.load:
    
    from mabozen.function_loader import Loader
    
    print("load")
    loader = Loader()
    loader.run()