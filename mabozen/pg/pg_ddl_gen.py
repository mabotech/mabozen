# -*- coding: utf-8 -*-
"""
mabotech web app generator
version: 0.0.1
"""
import os

import json
import md5

#from jinja2 import Environment, FileSystemLoader
from mako.template import Template
from mako import exceptions


class Json2Ddl(object):
    
    """
    TODO: command line args
    """  
    
    def __init__(self):
        
        """

        """
        
        fn = "../../models/backup/models_20140410193633.json"
        fn = "../../models/backup/models_20140425114210.json"
                        
        #"models/organization.json"
        with open(fn,"r") as fileh:
        
            models = fileh.read()

            self.d =  json.loads(models)["models"]
        
        #loader  = FileSystemLoader("../templates")

        #self.env = Environment(loader=loader, trim_blocks=True, lstrip_blocks = True)
        

    
    def create_index(self, index):
        
        """
        
        """
        pass
        
    def create_unique_index(self, index):
        """
        
        """
        
        pass
    
    
    def create_table(self, tables):
            
        """
        render jinja2 templage
        """
        
        print(tables)

        #template = self.env.get_template('pg_create_table4.sql')
        
        tpl_path = os.sep.join([r"E:\mabodev\mabozen\mabozen\templates", "pg_create_table5_mako.sql"])
        template = Template(filename=tpl_path,   disable_unicode=True, input_encoding='utf-8')


        v = template.render(tables=tables)
        
        m = md5.new()
        
        m.update(v)
        
        h = m.hexdigest()
        
        #print tables

        fn = "../../output/pg_ddl_%s.sql" % ( h)
        
        if os.path.exists(fn):
            print (fn)
            print ("ddl exists")
        else:
            print "gen %s" % (h)

            fh = open(fn, 'w')
            v = v.replace("\r\n","\n")
            fh.write(v)

            fh.close()
    

    def ddl_gen(self):                
        """
        create table
        """            
        tables = []

        for m in self.d:
            
            table = {"table":m["_table"]}

            cols = []

            toOne = {}

            unique = []

            sql = "\n"
            sql = sql + "-- Table:  %s\n"  %(m["_table"])
            sql_drop = "DROP TABLE %s;"  %(m["_table"])
            sql = sql +  "CREATE TABLE %s\n(\n" %(m["_table"])
            sql = sql +  "id serial NOT NULL,\n"

            for c in m["properties"]:
            
                col = c["column"].encode('utf8')
                
                if c["column"] == "textid":
                    
                    col = "texths hstore"
                    pass
                    
                elif "type" in c and c["type"] in ["bpchar"]:
                    col = "%s char(%s)"  % (c["column"], c["maximum_length"])  #character / char
                    #character
                    #print c
                elif "type" in c and c["type"] in ["varchar"]:
                    col = "%s varchar(%s)"  % (c["column"], c["maximum_length"])  #character varying / varchar
                    #character
                    #print c                                    
                else:
                    if "type" in c:
                        #sql = sql + 
                        v = " %s" % (c["type"])
                        col = col + v.encode('utf8')
                    else:
                        col = col + " %s"%("int4") # FK
                        
                        toOne[c["toOne"]] = c["column"].encode('utf8')

                    if "required" in c:
                        col = col + " NOT NULL"
                    else:
                        pass #col = col + ""
                    if "isUnique" in c:
                        if c["isUnique"] == True:
                            unique.append(c["column"])
                
                
                cols.append(col)
            table["column_defs"] = cols
            
            tables.append(table)

        self.create_table(tables)

        for u in unique:
            #print "CREATE UNIQUE INDEX idx_%s_%s ON %s (%s)" % (u, m["table"], u, u)
            pass
        pass

        for t in toOne:
            sql =  """ALTER TABLE %s 
        ADD CONSTRAINT fk_%s_%s FOREIGN KEY  (%s) REFERENCES %s (id);\n""" %(m["_table"], m["_table"],  t,toOne[t],t)
        #print sql
        #print "COMMENT ON COLUMN area.site_id IS 'site';"
    
    """
    procedure generator
    """
    def pl_gen(self):
        pass
    
    """
    form
    """
    def form_gen(self):
        tpl = """<form>
{{}}</form>"""
        
        for m in self.d:
            print(m)
        pass

if __name__ == '__main__':
        
        gen = Json2Ddl()
        
        gen.ddl_gen()
        
        #gen.form_gen()