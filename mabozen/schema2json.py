# -*- coding: utf-8 -*-


"""
pg schema to json [model]
"""

from time import strftime, localtime

#from jinja2 import Environment, FileSystemLoader

#from mako.template import Template
#from mako import exceptions

#from faker import Factory

#lib

from mabozen.lib.pg import Pg

from mabozen.lib.utils import save_models

from mabozen.lib.build_models import build

#########################################
#
class JsonModels(object):
    """
    schema extractor
    add ora schema to json?
    """
   
    def __init__(self):
        """
        init db
        """
        
        conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        self.dbi = Pg(conn_string)
        
        #loader  = FileSystemLoader("templates")

        #self.env = Environment(loader=loader, trim_blocks=True, lstrip_blocks = True)           
    
    def _get_tables_pg(self):
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
        
    def _get_tables_from_csv(self):
        """
        get table list form csv
        """

    def _get_schema(self, table_name):
        """
        call pg function to get schema info of a table
        """
        
        json_str = '{"catalog":"maboss", "schema":"mabotech","table_name":"%s"}' % (table_name)
        
        sql = """ select get_schema2('%s') """ % (json_str)

        self.dbi.execute(sql)
        
        data = self.dbi.fetchone()
        
        if "data" in data[0]:
            cols = data[0]['data']     
        
            return build(table_name, cols)
        
        else:
        
            return None
            
        #for col in cols:
        #    pprint( col )#['column_name']
        
    def _save_json(self, models):
        """
        save models in json file
        """
        filename = "../models/models_%s.json" % (strftime("%Y%m%d%H%M%S", localtime()))
        save_models(filename, models)       
        
    def get_json(self):
        """
        run extraxtor
        """ 
        models = []
        
        table_names = ["address","company", "deploys"]
        
        #table_names = self._get_tables_pg()
        
        for tabname in table_names:
            
            if type(tabname) == str:
                
                table_name = tabname
                
            else:            
                table_name = tabname[0]
            
            tab_dict = self._get_schema(table_name)
            
            if tab_dict != None:
                models.append(tab_dict)
            else:
                msg = "not table: [%s]" % (table_name)
                raise Exception(msg)
        
        return models
        
    def run(self):
        models = self.get_json()
        self._save_json(models)     

            
if __name__ == "__main__":
    
    jsonm = JsonModels()
    
    jsonm.run()