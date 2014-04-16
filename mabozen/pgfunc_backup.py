# -*- coding: utf-8 -*-

"""
pg function backup and load

"""
import os
import re
import hashlib

import traceback

from mabozen.lib.pg import Pg

class PgFunction(object):
    """
    class
    """
    
    def __init__(self):
        """
        init
        """
        conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        self.dbi = Pg(conn_string)
        
        self.function_root = r"E:\mabodev\maboss\database\functions"
        
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
  
    def query_source(self, fname):
        """
        get function from information_schema
        """
        #fname = 'mt_user_c_cf7'
        
        sql = """SELECT p.proname AS procedure_name,
          p.pronargs AS num_args,
          -- t1.typname AS return_type,          
          pg_catalog.pg_get_function_result(p.oid) as result_data_type,
          pg_catalog.pg_get_function_arguments(p.oid) as args_data_types,
          a.rolname AS procedure_owner,
          l.lanname AS language_type,
          p.proargtypes AS argument_types_oids,
          prosrc AS body
FROM pg_proc p
LEFT JOIN pg_type t1 ON p.prorettype=t1.oid
LEFT JOIN pg_authid a ON p.proowner=a.oid
LEFT JOIN pg_language l ON p.prolang=l.oid
    WHERE p.proname ='%s' """ % (fname)
    
        self.dbi.execute(sql)
        
        #print(sql)
        
        rtn = self.dbi.fetchone()
        
        if not rtn:
            raise Exception("no function:%s" % (fname))
            
        name = rtn[0]
        result_dtype = rtn[2]
        args_dtype = rtn[3]
        language = rtn[5]
        body =  rtn[7]
        
        return {"name" : name, "result_dtype" : result_dtype,  
                        "args_dtype" : args_dtype, "language" : language, "body" : body }
        
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
        
    def _get_functions(self):
        """
        get functions name from schema.
        """
        
        sql = """  select p.proname 
from pg_proc p 
LEFT JOIN pg_type t1 ON p.prorettype=t1.oid
LEFT JOIN pg_authid a ON p.proowner=a.oid
left join pg_catalog.pg_namespace ns on  p.pronamespace = ns.oid
where ns.nspname = '%(schema)s'  and proname not like 'uuid%%'
        """ % {"schema":"mabotech"}
        
        self.dbi.execute(sql)
        
        rows = self.dbi.fetchall()
        
        proc_list = []
        
        for row in rows:
            proc_list.append(row[0])
        
        return  proc_list #["mtp_search_cf2"]
        
    def load(self):
        """
        glob filename, read sql and compare hash with same name function in db.
        
        if glob file has multi version (function_name_version_hash) then load the last created one.
        
        if function exists and has same hash then pass
        if exists and different hash then backup function in db and load sql file
        if not exists then load directly
        """
    
    def backup(self):
        
        """
        backup function from pg
        """
        
        functions = self._get_functions()
        
        for fname in functions:
            
            try:
                func_dict = self.query_source(fname)
            
                self.save(func_dict)
                
            except Exception, ex:
                print(ex.message)
                traceback.print_exc()
                raise Exception("error")

        

def main():
    """
    for run and test
    """
    pgf = PgFunction()
    pgf.backup()

        
if __name__ == "__main__":
    
    main()