
import os
import re
import md5

import lib.pg

class PgFunction(object):
    
    def __init__(self):
        """
        init
        """
        connString = "port=6432 dbname=maboss user=mabotech password=mabouser"
        self.db = pg.Pg(connString)
        
    def get(self, name):
        pass
    
    def get_file_digest(self, filename):
        """
        get file digest while functionname.sql exists
        """
        pass
        
    def save(self, name, language, body):
        
        fn = "output/plcoffee/%s.sql" %(name)
        
        if os.path.exists(fn):
            digest = self.get_digest(body)
        
            fn = "output/plcoffee/%s_%s.sql" %(name, digest)
        
        print(fn)
        
        sql = """CREATE OR REPLACE FUNCTION %(name)s(i_json json)
  RETURNS json AS
$BODY$%(body)s$BODY$
  LANGUAGE %(language)s VOLATILE
  """%{"name":name, "body":body, "language":language}
  
        fh = open(fn, 'w')
        fh.write(sql)
        fh.close()
        
        #print sql
  
    def query_source(self, fname):
        """
        get function from information_schema
        """
        #fname = 'mt_user_c_cf7'
        
        sql = """SELECT p.proname AS procedure_name,
          p.pronargs AS num_args,
          t1.typname AS return_type,
          a.rolname AS procedure_owner,
          l.lanname AS language_type,
          p.proargtypes AS argument_types_oids,
          prosrc AS body
     FROM pg_proc p
LEFT JOIN pg_type t1 ON p.prorettype=t1.oid
LEFT JOIN pg_authid a ON p.proowner=a.oid
LEFT JOIN pg_language l ON p.prolang=l.oid
    WHERE proname ='%s' """ %(fname)
        self.db.execute(sql)
        
        #print(sql)
        
        rtn = self.db.fetchone()
        
        if not rtn:
            raise Exception("no function:%s" % (fname))
        
        name = rtn[0]
        language = rtn[4]
        body =  rtn[6]
        
        return (name, language, body)
        
    def get_digest(self, body):
        """
        get body digest
        """
        m = md5.new()

        m.update(body)

        digest = m.hexdigest()
        
        print(digest)
            
        return digest
        
    def backup(self):
        
        """
        backup function from pg
        """
        
        functions = ["mtp_find_active_cf1"]
        
        for fname in functions:
            
            try:
                (name, language, body) = self.query_source(fname)
            
                self.save(name, language, body)
            except Exception, ex:
                print(ex.message)
        pass
        

def main():
    
    pgf = PgFunction()
    pgf.backup()
    pass
        
if __name__ == "__main__":
    
    main()