# -*- coding: utf-8 -*-
"""
generate DDL (CREATE TABLE)
version: 0.0.1
"""
import os

import json
import hashlib

from jinja2 import Environment, FileSystemLoader

from mako.template import Template
from mako import exceptions

from mabozen.lib.model_helpers import get_foreign_table

class Json2Ddl(object):
    
    """
    Generate DDL(create table) from JSON using mako template
    """  
    
    def __init__(self, model_file_name, tpl_type):
        
        """
        read models.json and init jinja2 template
        """
        self.file_name = model_file_name
        self.tpl_type = tpl_type
        
        #"models/organization.json"
        with open(self.file_name,"r") as fileh:
        
            models_str = fileh.read()

            self.models =  json.loads(models_str)["models"]
        
        loader  = FileSystemLoader("../templates")

        self.env = Environment(loader=loader, trim_blocks=True, 
                                lstrip_blocks= True)     

    
    
    def save_ddl(self, tables):
            
        """
        render jinja2 templage
        """
        
        #print(tables)

        
        if self.tpl_type == "jinja":
            
            tpl_path = 'pg_create_table5_jinja.sql'
            template = self.env.get_template(tpl_path)
            ddl = template.render(tables=tables)
        else:
            
            tpl_path = os.sep.join([r"E:\mabodev\mabozen\mabozen\templates",
                                    "pg_create_table5_mako.sql"])
                   
            try:
                template = Template(filename=tpl_path,   disable_unicode=True, 
                                    input_encoding='utf-8')


                ddl = template.render(tables=tables)
            
            except Exception as ex:
                print (ex)
                print (exceptions.text_error_template().render())
        
        md5 = hashlib.md5()
        
        md5.update(ddl)
        
        digest = md5.hexdigest()
        
        #print tables

        ddl_fn = "../../output/pg_ddl_%s.sql" % ( digest)
        
        if os.path.exists(ddl_fn):
            print (ddl_fn)
            print ("ddl exists")
        else:
            print "gen %s" % (digest)
            
            #save ddl
            with open(ddl_fn, 'w') as fileh:
                ddl = ddl.replace("\r\n","\n")
                fileh.write(ddl)
                
    @classmethod
    def create_table(cls, model):
        """ create table from model """
        
        table = {"table":model["_table"]}

        cols = []

        foreign_tables = {}

        unique_tables = []

        for prop in model["properties"]:
        
            col = prop["column"].encode('utf8')
            
            fktab = get_foreign_table(prop["column"])
            
            #foreign key / serial / int4
            if fktab:
                col = "%s int4 /* %s */" % (prop["column"], fktab)
            
            # description / texths / hstore
            elif prop["column"] == "textid":
                
                col = "texths hstore"

            # char
            elif "type" in prop and prop["type"] in ["bpchar"]:
                #character / char
                col = "%s char(%s)" \
                    % (prop["column"], prop["maximum_length"])
                #character
                #print c
            #varchar
            elif "type" in prop and prop["type"] in ["varchar"]:
                #character varying / varchar
                col = "%s varchar(%s)"  \
                    % (prop["column"], prop["maximum_length"])
                #character
                #print c                                    
            else:
                if "type" in prop:
                    #sql = sql + 
                    ctype = " %s" % (prop["type"])
                    col = col + ctype.encode('utf8')
                else:
                    col = col + " %s" % ("int4") # FK
                    
                    foreign_tables[prop["toOne"]] = \
                            prop["column"].encode('utf8')

                if "required" in prop:
                    col = col + " NOT NULL"
                else:
                    pass #col = col + ""
                if "isUnique" in prop:
                    if prop["isUnique"] == True:
                        unique_tables.append(prop["column"])
            cols.append(col)
    
        table["column_defs"] = cols

        return table
    
    def create_ddl(self):                
        """
        create table
        """            
        tables = []

        for model in self.models:
            
            table = self.create_table(model)
            
            tables.append(table)

        self.save_ddl(tables)

    @classmethod
    def create_index(cls, unique_tables):
        """create unique index """
        for unique in unique_tables:
            #print "CREATE UNIQUE INDEX idx_%s_%s ON %s (%s)" 
            # % (u, m["table"], u, u)
            print unique
    @classmethod
    def create_fk(cls, foreign_tables):
        """ create foreign key"""
        
        for f_table in foreign_tables:
            sql =  """ALTER TABLE %s 
        ADD CONSTRAINT fk_%s_%s FOREIGN KEY  (%s) REFERENCES %s (id);
        """ % (f_table, f_table, f_table, foreign_tables[f_table], f_table)
            
            print sql
        #print "COMMENT ON COLUMN area.site_id IS 'site';"
        
def main():
    """ main """
    template_type = "jinja"

    file_name = "../../models/models_20140505211102.json"
    
    gen = Json2Ddl(file_name, template_type)
    
    gen.create_ddl()
        
if __name__ == '__main__':
    main()