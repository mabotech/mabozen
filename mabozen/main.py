# -*- coding: utf-8 -*-

"""
main of mabozen

command line

"""

import argparse

parser = argparse.ArgumentParser(prog='mabozen.py', description='mabozen command line.')

parser.add_argument('-j', '--tojson', dest='tojson', action='store_true',
                   help='from PostgreSQL db schema to json', default=False)

parser.add_argument('-b', '--backup', dest='backup', action='store_true',
                   help='backup function from PostgreSQL', default=False)

parser.add_argument('-d', '--deploy', dest='load', action='store_true',
                   help='deploy function to PostgreSQL', default=False)

parser.add_argument('-w', '--web', dest='web', action='store_true',
                   help='generate web pages(HTML, Javascript, CSS)', default=False)
                   
parser.add_argument('-t', '--test', dest='test', action='store_true',
                   help='generate unit test scripts(Python, Javascript)', default=False)
                   
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.1')                   
                   
args = parser.parse_args()

NOARG = True

if args.tojson:
    NOARG = False
    from mabozen.pg_json_model import PgJsonModel
    
    print("to json")
    jsonm = PgJsonModel()
    
    table_names = ["address","company", "deploys"]
    jsonm.run(table_names)

if args.backup:
    NOARG = False    
    from mabozen.pg_backup import PgBackup
    
    print("backup")
    backup = PgBackup()
    backup.func_backup()
    
if args.load:
    
    NOARG = False
    
    from mabozen.pg_deployer import PgDeployer
    
    print("load")
    deployer = PgDeployer()
    deployer.func_deploy()
    
if args.web:
    NOARG = False
    
    from mabozen.code_gen import CodeGen
    
    gen = CodeGen()
    gen.run()
    
    print("gen web")

if args.test:
    NOARG = False
    print("gen test scripts")
    
if NOARG:
    parser.print_help()



