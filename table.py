# -*- coding: utf-8 -*-

"""
DDL for Table create, drop

"""
import glob

import re


import pg


def get_tablename(line):
    """
    get table name from ddl scripts(sql)
    """
    
    rawstr = r"""CREATE TABLE\s(.*)\s?"""

    compile_obj = re.compile(rawstr,   re.MULTILINE)
    
    match_obj = compile_obj.search(line)
    
    return match_obj.group(1)


class Table(object):
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
                where table_name = '%s' """ % (tablename)
        
        self.dbi.execute(sql)
        
        rtn = self.dbi.fetchone()

        if rtn[0] == 1:        
            print("%s exists" %(tablename))
            return True
        else:
            print("%s not exists" %(tablename))
            return False
        #return True

    def drop(self, tablename):
        """
        drop table
        """
        
        sql = "drop table %s cascade" % (tablename)
        
        self.dbi.execute(sql)
        self.dbi.commit()
        
        print(sql)
        
    def rename(self, tablename):
        """
        rename table
        """
        
        sql = """ ALTER TABLE %s RENAME TO %s_1""" % (tablename, tablename)
        self.dbi.execute(sql)
        self.dbi.commit()
        print(sql)
        
    def create(self, tablename, ddl):
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

        filename =  ddl[0]

        with open(filename, 'r') as fileh:

            scripts = fileh.read()

            script_array  = scripts.split(';')

            for line in script_array:
                
                if len(line) > 10:
                    
                    tablename = get_tablename(line)
                    
                    if self.exists(tablename):
                            
                        #self.rename(tablename)                        
                        self.drop(tablename) 
                            
                    self.create(tablename, line)
        
        #fh.close()