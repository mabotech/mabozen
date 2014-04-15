
import os
import re
import hashlib

from mabozen.lib.pg import Pg

class PgFunction(object):
    
    def __init__(self):
        """
        init
        """
        connString = "port=6432 dbname=maboss user=mabotech password=mabouser"
        self.dbi = Pg(connString)
        
    def get(self, name):
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
    
    def _save(self, fn, name,  result_dtype,  args_dtype, language, body):
        
                sql = """CREATE OR REPLACE FUNCTION %(name)s(%(args_dtype)s)
  RETURNS %(return_type)s AS
$BODY$%(body)s$BODY$
  LANGUAGE %(language)s VOLATILE
  """%{"name":name,"return_type": result_dtype,  "args_dtype":args_dtype, "body":body, "language":language}
  
                fh = open(fn, 'w')
                fh.write(sql)
                fh.close()        
        
    def save(self, name,  result_dtype,  args_dtype, language, body):
        
        fn = "../output/plcoffee/%s.sql" %(name)
        
        if os.path.exists(fn):
            
            old_digest = self.get_file_digest(fn)
            
            digest = self.get_digest(body)
            
            if old_digest != digest:
        
                fn = "../output/plcoffee/%s_%s.sql" %(name, digest)        
                
                #check if already backuped
                if  os.path.exists(fn):
                    print(">.backuped")
                else:
                    print(fn)
                    self._save(fn, name,  result_dtype,  args_dtype, language, body)                
            else:
                print("same file")
        else:
            
            self._save(fn, name,  result_dtype,  args_dtype, language, body)
            
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
    WHERE p.proname ='%s' """ %(fname)
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
        
        return (name, result_dtype,  args_dtype, language, body)
        
    def get_digest(self, body):
        """
        get body digest
        """
        m = hashlib.md5()

        m.update(body)

        digest = m.hexdigest()
        
        #print(digest)
            
        return digest
        
    def _get_functions(self):
        
        sql = """  select p.proname from pg_proc p 
LEFT JOIN pg_type t1 ON p.prorettype=t1.oid
LEFT JOIN pg_authid a ON p.proowner=a.oid
where a.rolname = 'mabotech'  and t1.typstorage='x'        
        """
        
        self.dbi.execute(sql)
        
        rows = self.dbi.fetchall()
        list = []
        for row in rows:
            list.append(row[0])
        
        return  list #["mtp_search_cf2"]
        
    def backup(self):
        
        """
        backup function from pg
        """
        
        functions = self._get_functions()
        
        for fname in functions:
            
            try:
                (name,  result_dtype,  args_dtype,  language, body) = self.query_source(fname)
            
                self.save(name,  result_dtype,  args_dtype, language, body)
            except Exception, ex:
                print(ex.message)
        pass
        

def main():
    
    pgf = PgFunction()
    pgf.backup()
    pass
        
if __name__ == "__main__":
    
    main()