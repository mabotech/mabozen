
import json

from pg import Pg

from pprint import pprint

import time

from time import strftime, localtime

"""
pg schema extractor
"""

class Extractor(object):
   
    """
    init db
    """
    def __init__(self):
        
        connString = "port=6432 dbname=maboss user=mabotech password=mabouser"
        self.db = Pg(connString)
        
    """
    save to json file
    """
    def save(self, models):
        
        fn = "models/models_%s.json" % (strftime("%Y%m%d%H%M%S", localtime()))
        fh = open(fn, 'w')
        json_str = json.dumps(models)
        
        fh.write(json_str)
        
        fh.close()
       
    """
    build dict
    """
    def build(self, table_name, cols):
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
            v = {}
            v["name"] = col["column_name"]
            v["column"] = col["column_name"]
            if col["udt_name"] == "varchar":
                v["type"] = "%s(%s)" % ( col["udt_name"], col["character_maximum_length"]  )
            else:
                v["type"] = col["udt_name"]
                
            if col["is_nullable"] == "NO":
                 v["required"] = True
            
            tab["properties"].append(v)
            
        
        return tab
        
            
    """
    run extraxtor
    """
    def run(self):
        
        models = []
        
        table_names = ["site", "company", "area"]
        
        for table_name in table_names:
            
            tab_dict = self.get_info(table_name)
            
            if tab_dict != None:
                print "get table: %s" % (table_name)
                models.append(tab_dict)
            else:
                print "not table: [%s]" % (table_name)
                
        self.save(models)
    
    def get_info(self, table_name):
        
        json_str = '{"catalog":"maboss", "schema":"mabotech","table_name":"%s"}' % (table_name)
        
        sql = """ select get_schema2('%s') """ %(json_str)

        self.db.execute(sql)
        
        data = self.db.fetchone()
        
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