# -*- coding: utf-8 -*-

"""
json to code:

- testcase
- html
- js

"""

import os
import logging
import traceback

from mabozen.config import get_app_config

from mabozen.json_model import JsonModel

from mabozen.addons.gen_pytest import gen_unittest 

from mabozen.addons.gen_web import gen_web

from mabozen.addons.gen_menu import gen_menu

logger = logging.getLogger("code")
#########################################
#
class CodeGen(object):
    """
    pg schema extractor
    """
   
    def __init__(self, addons):
        """init
        """        

        self.jsonm = JsonModel()  
        
        self.conf = {}
        
        #configurating addons
        self.conf["addons"] = addons
        
        #template root path
        
        #self.conf["app_root"] = os.getcwd()
        
        app_cfg = get_app_config()
        
        self.conf["TPL_ROOT"] = os.sep.join([os.getcwd(), "templates"])
        
        self.conf["OUTPUT_WEB_ROOT"] = app_cfg["OUTPUT_WEB_ROOT"]
        
        print(self.conf)
        
        self.conf["OUT_ROOT"] = os.sep.join([ os.path.dirname(os.getcwd()), "output"])
        
        self.conf["TEST_ROOT"] = os.sep.join([ os.path.dirname(os.getcwd()), "test"])
        
        self.conf["TEST_TPL"] = [
                                    ("test_single_table_mako.py", "cru", "py"),
                                    ("test_item_delete_mako.py", "d","py"),
                                    ("test_item_delete_mako.py", "req","js")                                    
                                ]         
        #self.conf["pytest"] = ""

        #template file for web form
        #self.conf["form"] = "form_mako.html" 
        
        self.tpl_web = os.sep.join([os.getcwd(), "templates", "web", "angular"]) #, self.conf["form"] ])
 
        self._print_info()
    
    def _print_info(self):
        """print app info
        
        
        :param
        
        .. versionadded:: 0.0.1
        
        
        """
        
        print (self.conf)

    def run(self, filename):
        """
        run code generator
        """
               
        models = self.jsonm.get_json(filename)         
        #print(models)
        tables = []
        
        for model in models["models"]:
            
            #logger.debug(model)
            table_name = model["_table"]
            
            pkey = model["_pkey"]
            
            tables.append(table_name)
            
            print (">>:%s" % (table_name) )
            
            attrs = model["properties"]
            
            try:
                
                if "web" in self.conf["addons"]:
                    #generate html file [form]
                    print("- gen web")
                    table_meta = {"table":table_name, "pkey":pkey, "attrs":attrs}
                    gen_web(self.conf, table_meta)
                
                if "pytest" in self.conf["addons"]:
                    
                    #generate unit test py file
                    print("- gen pytest")
                    gen_unittest(self.conf, table_name, attrs)
                
            except Exception as ex:
                
                print (ex.message)
                
                traceback.print_exc()
        
        if "menu" in self.conf["addons"]:
            
            self.conf["template_type"]  = "menu"
            self.conf["file_type"]  = "html"
            
            gen_menu(self.conf, tables)
        
if __name__ == "__main__":
    
    addons = ["web","menu"]# [,"web", "pytest"]
    
    gen = CodeGen(addons)
    
    #filename = "../models/backup/models_20140425114210.json"
    #filename = "../models/organization.json"
    filename = "../working/models/models_20140529132918.json"
    filename = "../working/models/models_20140527145553.json"
    gen.run(filename)