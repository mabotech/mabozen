# -*- coding: utf-8 -*-

"""
backup PostgreSQL functions from db information schema

"""
import os
import re
import hashlib

import traceback

from mabozen.config import get_db_config
from mabozen.config import logging

logger = logging("zen_backup")

from mabozen.zen_factory import ZenFactory
#from mabozen.pg_schema import PgSchema


class PgBackup(object):
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
        
    def get(self, name):
        """
        get what?
        """
        pass
    
    def get_file_digest(self, filename):
        """
        get file digest while functionname.sql exists
        """
        with open(filename, 'r') as fileh:            
            sql = fileh.read()            
            rawstr = r"""\$BODY\$(.*)\$BODY\$"""
            compile_obj = re.compile(rawstr,  re.DOTALL)
            match_obj = compile_obj.search(sql)
            body = match_obj.group(1)
        
        return self.get_digest(body)        
    
    @classmethod
    def _save(cls, full_filename, func_dict):
        """
        render and save
        """
        
        sql = """CREATE OR REPLACE FUNCTION %(name)s(%(args_dtype)s)
  RETURNS %(result_dtype)s AS
$BODY$%(body)s$BODY$
  LANGUAGE %(language)s VOLATILE
  """% func_dict
        #{"name":name,"return_type": result_dtype,  "args_dtype":args_dtype, "body":body, "language":language}
  
        with open(full_filename, 'w') as fileh:
            
            fileh.write(sql)
            
    @classmethod
    def _save_coffee(cls, full_filename, func_dict):            
        """
        save coffee
        """
        
        with open(full_filename.replace(".sql",".coffee"), 'w') as fileh:
            
            fileh.write(func_dict["body"])
        
    def save(self, func_dict):
        """
        save sql to file system
        """
        filename = "%s.sql" % (func_dict["name"])
        
        full_filename = os.sep.join([self.function_root, filename])
        
        self._save_coffee(full_filename, func_dict)
        
        if os.path.exists(full_filename):
            
            old_digest = self.get_file_digest(full_filename)
            
            digest = self.get_digest(func_dict["body"])
            
            if old_digest != digest:
        
                filename = "%s@%s.sql" % (func_dict["name"], digest)   
                
                full_filename_digest = os.sep.join([self.function_root, filename])
                
                #check if already backuped
                if  os.path.exists(full_filename_digest):
                    print(">.backuped")
                else:
                    print(full_filename_digest)
                    self._save(full_filename_digest, func_dict)                
            else:
                #print("same file")
                pass
        else:
            
            self._save(full_filename, func_dict)
            
        #print sql
  
    @classmethod
    def get_digest(cls, body):
        """
        get body digest
        """
        md5 = hashlib.md5()

        md5.update(body)

        digest = md5.hexdigest()
        
        #print(digest)
            
        return digest
        
    def func_backup(self):
        
        """
        backup function from pg
        """
        
        functions = self.schema.get_functions()  #self._get_functions()
        
        for fname in functions:
            
            try:
                func_dict = self.schema.function_info(fname) #self.query_source(fname)
            
                self.save(func_dict)
                
            except Exception, ex:
                print(ex.message)
                traceback.print_exc()
                raise Exception("error")

        

def main():
    """
    for run and test
    """
    backup = PgBackup()
    backup.func_backup()

        
if __name__ == "__main__":
    
    main()