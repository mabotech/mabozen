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

from mabozen.pg_json_model import PgJsonModel

from mabozen.addon.gen_pytest import gen_unittest 

from mabozen.addon.gen_web import gen_web

from mabozen.addon.gen_menu import gen_menu

logger = logging.getLogger("code")
#########################################
#
class CodeGen(object):
    """
    pg schema extractor
    """
   
    def __init__(self):
        """init
        """        

        self.jsonm = PgJsonModel()  
        
        self.conf = {}
        
        #configurating addons
        self.conf["addons"] = ["pytest"]# ["menu","web", "pytest"]
        
        #template root path
        
        #self.conf["app_root"] = os.getcwd()
        
        self.conf["tpl_root"] = os.sep.join([os.getcwd(), "templates"])
        
        self.conf["out_root"] = os.sep.join([ os.path.dirname(os.getcwd()), "output"])
        
        self.conf["test_root"] = os.sep.join([ os.path.dirname(os.getcwd()), "test"])
        
        self.conf["test_tpl"] = [
                                    ("test_single_table_mako.py", "cru", "py"),
                                    ("test_item_delete_mako.py", "d","py"),
                                    ("test_item_delete_mako.py", "req","js")                                    
                                ]         
        #self.conf["pytest"] = ""

        #template file for web form
        #self.conf["form"] = "form_mako.html" 
        
        self.tpl_web = os.sep.join([os.getcwd(), "templates", "web"]) #, self.conf["form"] ])
 
        self._print_info()
    
    def _print_info(self):
        """print app info"""
        
        print (self.conf)

    def run(self):
        """
        run code generator
        """
        
        models = self.jsonm.get_json() 
        
        
        tables = []
        
        for model in models:
            logger.debug(model)
            table_name = model["_table"]
            
            tables.append(table_name)
            
            print (">>:%s" % (table_name) )
            
            attrs = model["data"]
            
            try:
                
                    
                    
                    
                if "web" in self.conf["addons"]:
                    #generate html file [form]
                    print("- gen web")
                    gen_web(self.conf, table_name, attrs)
                
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
    
    gen = CodeGen()
    
    gen.run()