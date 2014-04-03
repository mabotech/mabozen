# -*- coding: utf-8 -*-
"""
mabotech web app generator
version: 0.0.1
"""
import os

import json
import md5

from jinja2 import Environment, FileSystemLoader

"""

"""
class Gen(object):
        
        """
        TODO: command line args
        """
        def __init__(self):
                
                fh = open("models/organization.json","r")
                
                models = fh.read()

                self.d =  json.loads(models)
            
        """
        render jinja2 templage
        """
        def render(self, tables):
                
                loader  = FileSystemLoader("templates")

                env = Environment(loader=loader, trim_blocks=True, lstrip_blocks = True)

                template = env.get_template('pg_create_table.sql')

                v = template.render(tables=tables)
                
                m = md5.new()
                
                m.update(v)
                
                h = m.hexdigest()
                
                #print tables

                fn = "output/pg_ddl_%s.sql" % ( h)
                
                if os.path.exists(fn):
                    print "ddl exists"
                else:
                    print "gen %s" % (h)

                    fh = open(fn, 'w')
                     
                    fh.write(v)

                    fh.close()
        
        """
        create table
        """
        def ddl_gen(self):                
                
                tables = []

                for m in self.d:
                    
                        table = {"table":m["table"]}

                        cols = []

                        toOne = {}

                        unique = []

                        sql = "\n"
                        sql = sql + "-- Table:  %s\n"  %(m["table"])
                        sql_drop = "DROP TABLE %s;"  %(m["table"])
                        sql = sql +  "CREATE TABLE %s\n(\n" %(m["table"])
                        sql = sql +  "id serial NOT NULL,\n"

                        for c in m["properties"]:
                                col = c["column"].encode('utf8')
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
 
                self.render(tables)

                for u in unique:
                        #print "CREATE UNIQUE INDEX idx_%s_%s ON %s (%s)" % (u, m["table"], u, u)
                        pass
                pass

                for t in toOne:
                        sql =  """ALTER TABLE %s 
                ADD CONSTRAINT fk_%s_%s FOREIGN KEY  (%s) REFERENCES %s (id);\n""" %(m["table"], m["table"],  t,toOne[t],t)
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
        
        gen = Gen()
        
        gen.ddl_gen()
        
        #gen.form_gen()