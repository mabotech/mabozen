# -*- coding: utf-8 -*-

"""


"""
import os
import re
import hashlib

import traceback

from mabozen.config import get_db_config
from mabozen.config import logging

logger = logging("zen_backup")

from mabozen.zen_factory import ZenFactory

class CoffeeFmt(object):
    """
    class
    """
    
    def __init__(self):
        """
        init
        """

        ZEN_CFG = get_db_config()
        
        #self.pgs = PgSchema(ZEN_CFG['PORT'],ZEN_CFG['DATABASE'], ZEN_CFG['USERNAME'], ZEN_CFG['PASSWORD'])
        
        zenfactoy = ZenFactory(ZEN_CFG['DB_URL'])
        
        self.schema = zenfactoy.get_schema()        
        
        self.function_root = ZEN_CFG['FUNCTIONS_ROOT']
        
        logger.debug("init")
        
    @classmethod
    def clean(self, lines):
        new_lines = []

        for line in lines.split('\n'):
            line = line.replace('\t','    ')
            line = line.rstrip()
            #print line
            new_lines.append(line)
            
        script_str = '\n'.join(new_lines)
        
        return script_str
        
    def replace(self, func_dict):
        """
        render and save
        """
        func_dict["body"] = self.clean(func_dict["body"])
        
        sql = """CREATE OR REPLACE FUNCTION %(name)s(%(args_dtype)s)
  RETURNS %(result_dtype)s AS
$BODY$%(body)s$BODY$
  LANGUAGE %(language)s VOLATILE
  """% func_dict
  
        self.schema.execute_sql(sql)

    def run(self):
        
        """
        backup function from pg
        """
        
        functions = self.schema.get_functions()  #self._get_functions()
        
        for fname in functions:
            
            try:
                func_dict = self.schema.function_info(fname) #self.query_source(fname)
                
                if func_dict["language"] == 'plcoffee':
                    
                    print (func_dict["name"])
                    
                    self.replace(func_dict)
                
            except Exception, ex:
                print(ex.message)
                traceback.print_exc()
                raise Exception("error")

        

def main():
    """
    for run and test
    """
    fmt = CoffeeFmt()
    fmt.run()

        
if __name__ == "__main__":
    
    main()