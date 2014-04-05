
import glob

import re


import pg

class Table(object):
    
    def __init__(self):
        
        connString = "port=6432 dbname=maboss user=mabotech password=mabouser"
        self.db = pg.Pg(connString)
        pass
        
    def get_tablename(self, line):
        
        rawstr = r"""CREATE TABLE\s(.*)\s?"""

        compile_obj = re.compile(rawstr,   re.MULTILINE)
        
        match_obj = compile_obj.search(line)
        
        return match_obj.group(1)

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

    def drop(self, tablename):
        
        sql = "drop table %s cascade" %(tablename)
        
        self.db.execute(sql)
        self.db.commit()
        
        print("drop")
        pass
        
    def rename(self, tablename):
        
        sql = """ ALTER TABLE %s RENAME TO %s_1""" %(tablename, tablename)
        self.db.execute(sql)
        self.db.commit()
        print("rename")
        pass
        
    def create(self, tablename, ddl):
        
        print("create table %s" %(tablename))
        self.db.execute(ddl)
        self.db.commit()

    def run(self):
        
        ddl = glob.glob("output/*.sql")

        filename =  ddl[0]

        fh = open(filename, 'r')

        s = fh.read()

        ps  = s.split(';')

        for line in ps:
            
            if len(line) > 10:
                tablename = self.get_tablename(line)
                
                if self.exists(tablename):
                        
                        #self.rename(tablename)                        
                        self.drop(tablename) 
                        
                self.create(tablename, line)
        
        fh.close()