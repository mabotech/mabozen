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
from mabozen.config import get_db_config
from mabozen.config import logging

logger = logging("zen_db2json")

from mabozen.pg_schema import PgSchema

#from mabozen.lib.pg import Pg

from mabozen.lib.utils import save_models

from mabozen.lib.build_models import build

#########################################
#
class PgJsonModel(object):
    """
    schema extractor
    add ora schema to json?
    """
   
    def __init__(self):
        """
        init db
        """
        
        #conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        #self.dbi = Pg(conn_string)
        
        ZEN_CFG = get_db_config()
        
        self.pgs = PgSchema(ZEN_CFG['PORT'],ZEN_CFG['DATABASE'], ZEN_CFG['USERNAME'], ZEN_CFG['PASSWORD'])
        
        logger.debug("init")
        
        #loader  = FileSystemLoader("templates")

        #self.env = Environment(loader=loader, trim_blocks=True, lstrip_blocks = True)           
       
    def _get_tables_from_csv(self):
        """
        get table list form csv
        """
        
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
        
        #table_names =self.pgs.get_tables() # self._get_tables_pg()
        
        for tabname in table_names:
            
            if type(tabname) == str:
                
                table_name = tabname
                
            else:            
                table_name = tabname[0]
            
            tab_dict = self.pgs.query_table_schema(table_name)   #self._get_schema(table_name)
            
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
    
    json_m = PgJsonModel()
    
    json_m.run()