# -*- coding: utf-8 -*-
"""
generate DDL (CREATE TABLE)
version: 0.0.1
"""
import os

import json
import hashlib

from time import strftime, localtime

from jinja2 import Environment, FileSystemLoader

from mako.template import Template
from mako import exceptions

#from mabozen.lib.model_helpers import get_foreign_table

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
        
        self.fk_constraints = []
    
    
    def _save_ddl(self, tables):
            
        """
        render jinja2/mako templage
        """
        
        #print(tables)

        
        if self.tpl_type == "jinja":
            
            tpl_path = 'pg_create_table5_jinja.sql'
            template = self.env.get_template(tpl_path)
            ddl = template.render(tables=tables)
        else:
            
            tpl_path = os.sep.join([r"E:\mabodev\mabozen\mabozen\templates",
                                    "pg_create_table7_mako.sql"])
                   
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
        
        print (ddl_fn)
        
        if os.path.exists(ddl_fn):
            
            print ("ddl exists")
        else:
            print "gen %s" % (digest)
            
            #save ddl
            with open(ddl_fn, 'w') as fileh:
                ddl = ddl.replace("\r\n","\n")
                fileh.write(ddl)
                
        with open("ddl_table.txt",'w') as fileh:
            #logger.debug(ddl_fn)
            fileh.write(ddl_fn) 
                
    @classmethod
    def _create_type(cls, prop):
        """ varchar(32) """
        if prop["type"] in ["bpchar", "char", "varchar"]:
            return "%s(%s)" % (prop["type"], prop["maximum_length"])
        else:
            return prop["type"]        

    def _create_table(self, model):
        """ create table from model """
        
        table = {"table":model["_table"]}

        cols = []

        foreign_tables = {}

        unique_tables = []

        for prop in model["properties"]:
        
            col = prop["column"].encode('utf8')
            
            #fktab = get_foreign_table(prop["column"])
            
            if "pk" in prop:
                pkval = prop["pk"]
            else:
                pkval = False
            
            if pkval or prop["column"] =='id':
                col = "%s %s" % (prop["column"], self._create_type(prop))
                table["pk_column"] = prop["column"]
            #foreign key / serial / int4
            elif "fk" in prop:
                #print prop
                
                self.fk_constraints.append({"table":model["_table"], \
                    "column":prop["column"], "f_tab":prop["ref"]["table"], \
                    "f_col":prop["ref"]["column"]})
                
                col = "%s %s /* %s.%s */" % (prop["column"], \
                    self._create_type(prop), \
                    prop["ref"]["table"],prop["ref"]["column"])
            
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
            if model["_table"] == "not a table":
                continue
            else:
                #print model
                #print ( json.dumps(model, sort_keys=True, indent=2, separators=(',', ': '))  )
                try:
                    table = self._create_table(model)
                
                    tables.append(table)
                except Exception as ex:
                    #print model
                    print ( json.dumps(model, sort_keys=True, indent=2, separators=(',', ': '))  )
                    print ex.message
                    raise Exception("error")

        self._save_ddl(tables)

    @classmethod
    def create_index(cls, unique_tables):
        """create unique index """
        for unique in unique_tables:
            #print "CREATE UNIQUE INDEX idx_%s_%s ON %s (%s)" 
            # % (u, m["table"], u, u)
            print unique

    def create_fk(self):
        """ create foreign key"""
        i = 0
        scripts = []
        
        fk_tables = {}
        
        for cons in self.fk_constraints:
            
            # drop constraint firstly?
            
            if cons["table"] in fk_tables:
                fk_tables[cons["table"]] = fk_tables[cons["table"]] +1
                seq = fk_tables[cons["table"]]
            else:
                fk_tables[cons["table"]] = 0
                seq = 0
            
            sql =  """ALTER TABLE %s ADD CONSTRAINT fk_%s_%02d FOREIGN KEY  (%s) REFERENCES %s (%s)""" \
            % (cons["table"], cons["table"], seq, cons["column"], \
                cons["f_tab"], cons["f_col"])
            
            scripts.append(sql)
            
            i = i +1
        
        
        fn = "../../output/pg_fk_%s.sql" % (strftime("%Y%m%d%H%M%S", localtime()))

        with open(fn, 'w') as fileh:
            fileh.write(";\n\n".join(scripts))
            
        with open("ddl_fk.txt",'w') as fileh:
            #logger.debug(fn)
            fileh.write(fn)             
        #print "COMMENT ON COLUMN area.site_id IS 'site';"
        
def main():
    """ main """
    template_type = "mako"

    #file_name = "../../models/models_20140506172541.json"
    #file_name ="../../models/models_all.json"
    
    with open("../models_last.txt",'r') as fileh:
        file_name = os.sep.join(["..",fileh.read()])
    
    gen = Json2Ddl(file_name, template_type)
    
    gen.create_ddl()
    
    gen.create_fk()
        
if __name__ == '__main__':
    main()