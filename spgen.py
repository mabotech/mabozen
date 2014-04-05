import glob

import re
import md5

import pg

class SpGen(object):
    
    def __init__(self):
        
        connString = "port=6432 dbname=maboss user=mabotech password=mabouser"
        self.db = pg.Pg(connString)
        pass
        
    def get_source(self):
        
        fn = "templates/mt_user_c_cf7.sql"
        
        fh = open(fn, 'r')
        
        sql = fh.read()
        
        fh.close()

        # common variables

        rawstr = r"""\$BODY\$(.*)\$BODY\$"""
        compile_obj = re.compile(rawstr,  re.DOTALL)
        match_obj = compile_obj.search(sql)
        body = match_obj.group(1)
        
        self.get_digest(body)
        
    def exists(self, tablename):
        
        sql = "select count(1) from information_schema.tables where table_name = '%s'" %(tablename)
        
        self.db.execute(sql)
        
        rtn = self.db.fetchone()

        if rtn[0] == 1:        
            print("%s exists" %(tablename))
            return True
        else:
            print("%s not exists" %(tablename))
            return False
        #return True
        
    def backup(self, name, language, body, digest):
        
        fn = "%s_%s.sql" %(name, digest)
        
        print(fn)
        
        sql = """CREATE OR REPLACE FUNCTION %(name)s(i_json json)
  RETURNS json AS
$BODY$%(body)s$BODY$
  LANGUAGE %(language)s VOLATILE
  """%{"name":name, "body":body, "language":language}
  
        print sql 
    
    def gen(self, filename):
        
        if self.exists(sp):
            diff = compare(sp)
            if diff:
                dump(sp)
                create(sp)
            else:
                pass
        else:
            create(sp)
            
    def create(self, filename):
        
        fh = open(filename, 'r')

        s = fh.read()

        self.db.execute(s)
        
        fh.close()

    def run(self):
        
        ddl = glob.glob("output/pl/*.sql")

        fns =  ddl
        
        for filename in fns:
            self.gen(filename)       
        
    def query_source(self):
        
        fname = 'mt_user_c_cf7'
        
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
        
        name = rtn[0]
        language = rtn[4]
        body =  rtn[6]
        
        digest = self.get_digest(body)
        
        self.backup(name, language, body, digest)
        
        
        
    def get_digest(self, body):
        
        m = md5.new()

        m.update(body)

        digest = m.hexdigest()
        
        print(digest)
        
        return digest

                
def main():

    spgen = SpGen()
    #spgen.run()
    spgen.query_source()
    
    spgen.get_source()
    
    
if __name__ == "__main__":

        main()