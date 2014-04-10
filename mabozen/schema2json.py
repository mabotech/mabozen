# -*- coding: utf-8 -*-

"""
pg schema to json [model]
"""

import json

from lib.pg import Pg

from pprint import pprint

import time

from time import strftime, localtime

from jinja2 import Environment, FileSystemLoader

from faker import Factory


"""
pg schema extractor
"""

class Extractor(object):
   
    def __init__(self):
        """
        init db
        """
        
        conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        self.dbi = Pg(conn_string)
        
        loader  = FileSystemLoader("../templates")

        self.env = Environment(loader=loader, trim_blocks=True, lstrip_blocks = True)

    def save(self, models):
        """
        save to json file
        """
        filename = "../models/models_%s.json" % (strftime("%Y%m%d%H%M%S", localtime()))
        
        info = {"version":"0.1", "by":"mabo"}
        
        mdef = {"info":info, "models":models}
        
        with open(filename, 'w') as fileh:
            
            json_str = json.dumps(mdef, sort_keys=True, indent=4, separators=(',', ': '))
            
            fileh.write(json_str)


    def build(self, table_name, cols):
        """
        build dict
        """
    
        """
        {"table":"company",
"properties":[
	{"name":"company", "column":"company", "type":"varchar(10)", "required":true, "isUnique":true},
	{"name":"text", "column":"texths",  "type":"hstore"}
	]
}
        """
        
        tab = {"_table":table_name}
        tab["comment"] = table_name
        tab["properties"] = []
        
        for col in cols:
            
            #filter fuid column
            if col["column_name"] == 'fuid':
                continue
            
            # convert
                        
            attr = {}
            
            attr["name"] = col["column_name"]
            
            attr["column"] = col["column_name"]
            
            attr["comment"] = col["column_name"]
            
            if col["udt_name"] in [ "varchar", "bpchar"]:
                #attr["type"] = "%s(%s)" % ( col["udt_name"], col["character_maximum_length"]  )
                attr["type"] = col["udt_name"]
                if col["character_maximum_length"] == None:
                    attr["maximum_length"] = 30
                else:
                    attr["maximum_length"] = col["character_maximum_length"]
                
            else:
                attr["type"] = col["udt_name"]
                
            #if col["isUnique"] == "NO":
            #     attr["unique"] = True
                 
            if col["is_nullable"] == "NO":
                 attr["required"] = True
            
            tab["properties"].append(attr)           
        
        return tab            
    
    def get_tables_from_schema(self):
        """
        get tables from schema
        """
        
        sql = """select table_name from information_schema.tables 
                where table_catalog = 'maboss' 
                and table_schema = 'mabotech' 
                and table_type = 'BASE TABLE'
                order by table_name
        """
        
        self.dbi.execute(sql)
        
        return self.dbi.fetchall()
        
    def get_tables_from_csv(self):
        """
        get table list form csv
        """

    def run(self):
        """
        run extraxtor
        """ 
        models = []
        
        table_names = ["company", "company_address"]
        
        #table_names = self.get_tables_from_schema()
        
        for tabname in table_names:
            
            if type(tabname) == str:
                
                table_name = tabname
                
            else:
            
                table_name = tabname[0]
            
            tab_dict = self.get_schema(table_name)
            
            if tab_dict != None:
                print "get table: %s" % (table_name)
                
                #print (tab_dict)
                
                self.gen_test_case(tab_dict)
                
                models.append(tab_dict)
            else:
                print "not table: [%s]" % (table_name)
        
        #save models
        #self.save(models)
        
    
    def gen_test_case(self, obj):

        table_name = obj["_table"]

        template = self.env.get_template('test_single_table.py')
        
        t = table_name.split("_")
        
        xs = []
        for i in t:
            x = i.capitalize()
            xs.append(x)
        
        class_name = "".join(xs)
        
        table = {}

        v = template.render(class_name=class_name, table = table_name)
        
        #print(v)
        
        with open("../test/test_%s.py" % (table_name), 'w') as fileh:
            fileh.write(v)
        
        for property in obj["properties"]:
            print (property["name"])
        pass
        
    def gen_html(self, obj):
        
        pass
        
    def gen_js(self, obj):
        
        pass
    
    def get_schema(self, table_name):
        """
        call pg function to get schema info of a table
        """
        
        json_str = '{"catalog":"maboss", "schema":"mabotech","table_name":"%s"}' % (table_name)
        
        sql = """ select get_schema2('%s') """ % (json_str)

        self.dbi.execute(sql)
        
        data = self.dbi.fetchone()
        
        if "data" in data[0]:
            cols = data[0]['data']
        
        
        
            return self.build(table_name, cols)
        
        else:
        
            return None
        

        
        #for col in cols:
        #    pprint( col )#['column_name']
        

if __name__ == "__main__":
    
    ext = Extractor()
    
    ext.run()