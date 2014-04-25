# -*- coding: utf-8 -*-

"""
pg schema to json [model]
"""
import json
from time import strftime, localtime

#lib
from mabozen.config import get_db_config
from mabozen.config import logging

logger = logging("zen_db2json")

from mabozen.pg_schema import PgSchema

from mabozen.lib.model_helpers import build_model

#########################################
#
class PgJsonModel(object):
    """
    schema extractor
    add ora schema to json?
    """
   
    def __init__(self):
        """init schema instance"""
        
        ZEN_CFG = get_db_config()
        
        self.schema = PgSchema(ZEN_CFG['PORT'],ZEN_CFG['DATABASE'], ZEN_CFG['USERNAME'], ZEN_CFG['PASSWORD'])
        
        logger.debug("init")
       
    def _get_tables_from_csv(self):
        """
        get table list form csv
        """
        
    def _save_json(self, models):
        """
        save models in json file
        """
        
        #save_models(filename, models)       
        
        info = {"version":"0.2", "by":"mabozen"}    
        models_def = {"info":info, "models":models}
        
        filename = "../models/models_%s.json" % (strftime("%Y%m%d%H%M%S", localtime()))
        logger.debug(filename)
        
        #md5 check?
        
        with open(filename, 'w') as fileh:
        
            json_str = json.dumps(models_def, sort_keys=True, indent=4, separators=(',', ': '))        
            fileh.write(json_str) 
        
        
    def get_json(self, table_names):
        """run extraxtor""" 
        models = []
        
        for tabname in table_names:
            
            if type(tabname) == str:                
                table_name = tabname                
            else:            
                table_name = tabname[0]
                
            tab_dict = self.schema.query_table_schema(table_name)   #self._get_schema(table_name)
            print(tab_dict)
            if tab_dict != None:
                #build model as json.
                model = build_model(table_name, tab_dict)
                models.append(model)
            else:
                msg = "not table: [%s]" % (table_name)
                raise Exception(msg)
        
        return models
        
    def run(self, table_names):
        """run model dumps"""
        
        if len(table_names) == 0:
            table_names =self.schema.get_tables()
            
        models = self.get_json(table_names)
        self._save_json(models)     

            
if __name__ == "__main__":
    
    json_m = PgJsonModel()
    table_names = ["address","company"]
    json_m.run(table_names)