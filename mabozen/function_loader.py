# -*- coding: utf-8 -*-

"""
load function
"""

import os
import glob

import re

from flask.config import Config

from mabozen.lib.logging_factory import get_logger

from mabozen.pg_schema import PgSchema


APP = "mabozen"
LOGGING_CONFIG_FILE = 'conf/logging_config.py'


LOG_CFG = Config('')

LOG_CFG.from_pyfile(LOGGING_CONFIG_FILE)

logger = get_logger(APP, '..\\logs', LOG_CFG['LOGGING']) 

class Loader(object):
    """ class """
    
    def __init__(self):
        """  init db schema """
        
        self.pgs = PgSchema(6432, 'maboss', 'mabotech', 'mabouser')
        
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
                
    def run(self):
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
    loader = Loader()
    loader.run()
    
    
if __name__ == "__main__":
    main()