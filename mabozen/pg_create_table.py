# -*- coding: utf-8 -*-

"""
DDL for Table create, drop

"""
import glob

import re


import lib.pg


def get_table_name(line):
    """
    get table name from ddl scripts(sql)
    """
    
    rawstr = r"""CREATE TABLE\s(\w+)\s?"""

    compile_obj = re.compile(rawstr,   re.MULTILINE)
    
    match_obj = compile_obj.search(line)
    
    return match_obj.group(1)


class PgDDLGen(object):
    """
    DDL execution for table
    """
    
    def __init__(self):
        """
        init pg db
        """
        conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        self.dbi = pg.Pg(conn_string)
        


    def exists(self, tablename):
        """
        check table exists or not
        """
        sql = """select count(1) from information_schema.tables 
                where table_name = '%s' and table_schema = 'mabotech' """ % ( tablename.lower() )
        
        print(sql)
        
        self.dbi.execute(sql)
        
        rtn = self.dbi.fetchone()

        if rtn[0] == 1:        
            print("%s exists" %(tablename))
            return True
        else:
            print("%s not exists" %(tablename))
            return False
        #return True

    def drop_table(self, tablename):
        """
        drop table
        """  
        
        try:
        
            sql = """drop table %s cascade""" % (tablename)
            
            self.dbi.execute(sql)
            self.dbi.commit()

            sql = """drop table "%s" cascade""" % (tablename)
            
            self.dbi.execute(sql)
            self.dbi.commit()    
        except Exception, ex:
            self.dbi.rollback()    
            print (ex.message)
        
        #print(sql)
        
    def rename_table(self, tablename):
        """
        rename table
        """
        
        sql = """ ALTER TABLE %s RENAME TO %s_1""" % (tablename, tablename)
        self.dbi.execute(sql)
        self.dbi.commit()
        print(sql)
        
    def create_table(self, tablename, ddl):
        """
        create table
        """
        print("create table %s" % (tablename))
        self.dbi.execute(ddl)
        self.dbi.commit()

    def run(self):        
        """
        execute ddl sql
        """
        
        ddl = glob.glob("output/*.sql")

        #filename =  ddl[0]
        
        filename = "../templates/pg_new.sql"
        filename = "../output/pg_ddl_c49eca796ca91ad8d69a965f44141958.sql"

        with open(filename, 'r') as fileh:

            scripts = fileh.read()
            
            scripts = scripts.replace('"', '')

            script_array  = scripts.split(';')

            for line in script_array:
                
                if len(line) > 10:
                    
                    tablename = get_table_name(line)
                    
                    if self.exists(tablename):
                            
                        #self.rename_table(tablename)                        
                        self.drop_table(tablename) 
                            
                    self.create_table(tablename, line)
        
        #fh.close()
        
if __name__ == "__main__":
    
    tab = PgDDLGen()
    
    tab.run()
    
    