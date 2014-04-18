# -*- coding: utf-8 -*-

"""
load function

glob filename, read sql and compare hash with same name function in db.

if glob file has multi version (function_name_version_hash) then load the last created one.

if function exists and has same hash then pass
if exists and different hash then backup function in db and load sql file
if not exists then load directly

"""

import os
import re
import glob
import traceback

from mabozen.config import get_db_config
from mabozen.config import logging

logger = logging("zen_loader")

from mabozen.pg_schema import PgSchema

class PgDeployer(object):
    """ class """
    
    def __init__(self):
        """  init db schema """
        
        ZEN_CFG = get_db_config()
        
        self.pgs = PgSchema(ZEN_CFG['PORT'],ZEN_CFG['DATABASE'], ZEN_CFG['USERNAME'], ZEN_CFG['PASSWORD'])
        logger.debug("init")
        
    @classmethod
    def _get_function_name_from_sql(cls, sql):
        """ get function name from path"""
        
        return sql

    def load(self, obj):
        """ load pg functoin"""
        
        #print obj
        #ctime = obj[0]
        filename = obj[1]
        digest = obj[2]
        #print self._get_function_name(obj[1])
        function_name = obj[3]
        
        if digest != 0:
            #print digest
            pass
        with open(filename, 'r') as fileh:
            sql = fileh.read()
            
            #print(obj)
            if not self.pgs.function_exists(function_name):
                
                self.pgs.execute_sql(sql)
                logger.debug("%s loaded" % (function_name))
                #print function_name
                
            else:
                #logger.info("%s exists " % (function_name))
                pass
                
    def func_deploy(self):
        """run load"""
        
        funcs_dict = {}

        functions = glob.glob(r"E:\mabodev\maboss\database\functions\*.sql")

        for func in functions:
            
            file_stat = os.stat(func)
            ctime =  file_stat.st_ctime
            
            basepath = re.split("\@|\.", func)
            
            function_name =  basepath[0].split(os.sep)[-1:][0]
            
            #print function_name
            
            #fname = function_name.split(os.sep)[-1:][0]
            
            if function_name in funcs_dict:
                if ctime > funcs_dict[function_name][0]:
                    funcs_dict[function_name] = [ctime, func, basepath[1], function_name]
                else:
                    #print (func)
                    pass
            else:
                funcs_dict[function_name] = [ctime, func, 0, function_name]
                
        for function_name in funcs_dict:
            
            #filename = funcs_dict[function_name][1]
            
            self.load(funcs_dict[function_name])
           
def main():
    """ main """
    deployer = PgDeployer()
    deployer.func_deploy()
    
    
if __name__ == "__main__":
    main()