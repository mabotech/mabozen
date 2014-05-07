# -*- coding: utf-8 -*-

"""
run ddl to CREATE TABLE
"""
import glob

import re

#lib
from mabozen.config import get_db_config
from mabozen.config import logging

logger = logging("ctab")

from mabozen.zen_factory import ZenFactory

def get_table_name(line):
    """
    get table name from ddl scripts(sql)
    """
    
    rawstr = r"""create table\s(\w+)\s?"""

    compile_obj = re.compile(rawstr,   re.MULTILINE)
    
    match_obj = compile_obj.search(line)
    
    if match_obj:
        return match_obj.group(1)
    else:
        return None


class PgTable(object):
    """
    DDL execution for table
    """
    
    def __init__(self):
        """
        init pg db
        """
        logger.debug("init")
        
        ZEN_CFG = get_db_config()
        
        zenfactoy = ZenFactory(ZEN_CFG['DB_URL'])
        
        self.schema = zenfactoy.get_schema()
        

    '''
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
    '''
    def data_backup(self):
        """ rename table and insert into after new table created"""
        pass
        
    def drop_table(self, tablename):
        """ drop table """  
        
        try:
            
            """
            sql = " ""drop table %s cascade"" " % (tablename)
            
            self.dbi.execute(sql)
            self.dbi.commit()
            """
            sql = """drop table "%s" cascade""" % (tablename)
            
            #self.dbi.execute(sql)
            #self.dbi.commit()    
            self.schema.execute_sql(sql)
        except Exception, ex:
            #self.dbi.rollback()
            self.schema.execute_sql("rollback")            
            print (ex.message)
        
        #print(sql)
        
    def rename_table(self, tablename):
        """ rename table """
        
        sql = """ ALTER TABLE %s RENAME TO %s_1""" % (tablename, tablename)
        #self.dbi.execute(sql)
        #self.dbi.commit()
        self.schema.execute_sql(sql)
        #print(sql)
        self.schema.execute_sql(tablename)
        
    def create_table(self, tablename, ddl):
        """ create table """
        
        print("create table %s" % (tablename))
        self.schema.execute_sql(ddl)
        
    def create_obj(self, ddl):
        """ create fk, unique index, index, etc."""
        try:
            self.schema.execute_sql(ddl)
        except Exception as ex:
            self.schema.execute_sql("rollback")
            print(ddl)
            print(ex.message)

    def create(self, filename):        
        """ execute ddl sql """
        
        ddl = glob.glob("output/*.sql")
        
        #filename =  ddl[0]
        
        #filename = "../templates/pg_new.sql"
        #filename = "../output/pg_ddl_c49eca796ca91ad8d69a965f44141958.sql"

        with open(filename, 'r') as fileh:

            scripts = fileh.read()
            
            scripts = scripts.lower()
            
            scripts = scripts.replace('"', '')

            script_array  = scripts.split(';')

            for line in script_array:
                
                #print line
                
                if len(line) > 10:
                    
                    tablename = get_table_name(line)
                    
                    if not tablename:
                        self.create_obj(line)
                        continue
                    
                    if self.schema.table_exists(tablename.lower()):
                            
                        #self.rename_table(tablename)
                        print "drop %s" %(tablename)                        
                        self.drop_table(tablename) 
                    else:
                        print "new %s" %(tablename)
                            
                    self.create_table(tablename, line)
        
        #fh.close()
        
if __name__ == "__main__":
    
    tab = PgTable()

    file_name = "../../models/pg_new.sql"
    
    with open("ddl_table.txt",'r') as fileh:
        
        file_name = fileh.read()
        print(file_name)
    
    tab.create(file_name)
    
    with open("ddl_fk.txt",'r') as fileh:
        
        file_name = fileh.read()    
        print(file_name)
    
    tab.create(file_name)    
    
    