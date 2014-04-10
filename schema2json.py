# -*- coding: utf-8 -*-

"""
pg schema to json [model]
"""

import json

from pg import Pg

from pprint import pprint

import time

from time import strftime, localtime

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
        

    def save(self, models):
        """
        save to json file
        """
        filename = "models/models_%s.json" % (strftime("%Y%m%d%H%M%S", localtime()))
        
        with open(filename, 'w') as fileh:
            
            json_str = json.dumps(models)
            
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
        
        tab = {"table":table_name}
        
        tab["properties"] = []
        
        for col in cols:
            
            # convert
                        
            attr = {}
            
            attr["name"] = col["column_name"]
            
            attr["column"] = col["column_name"]
            
            if col["udt_name"] == "varchar":
                attr["type"] = "%s(%s)" % ( col["udt_name"], col["character_maximum_length"]  )
            else:
                attr["type"] = col["udt_name"]
                
            if col["is_nullable"] == "NO":
                 attr["required"] = True
            
            tab["properties"].append(attr)           
        
        return tab            
    
    def get_tables_from_schema(self):
        """
        get tables from schema
        """
        
        sql = """ select now()
        
        """
        
        self.dbi.execute(sql)
        
    def get_tables_from_csv(self):
        """
        get table list form csv
        """

    def run(self):
        """
        run extraxtor
        """ 
        models = []
        
        table_names = ["site", "company", "area"]
        
        for table_name in table_names:
            
            tab_dict = self.get_schema(table_name)
            
            if tab_dict != None:
                print "get table: %s" % (table_name)
                models.append(tab_dict)
            else:
                print "not table: [%s]" % (table_name)
                
        self.save(models)
    
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