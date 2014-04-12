# -*- coding: utf-8 -*-

"""
json to code [unittest, html]
"""

import os

from mabozen.schema2json import JsonModels

from mabozen.addon.gen_pytest import gen_unittest 
from mabozen.addon.gen_html import gen_form

#########################################
#
class CodeGen(object):
    """
    pg schema extractor
    """
   
    def __init__(self):
        """init
        """        

        self.jsonm = JsonModels()  
        
        self.conf = {}
        
        #configurating addons
        self.conf["addons"] = ["web", "pytest"]
        
        #template root path
        self.conf["tpl_root"] = os.sep.join([os.getcwd(), "templates"])
        
        self.conf["pytest"] = ""

        #template file for web form
        self.conf["form"] = "form_mako.html"
 
        self.tpl_form = os.sep.join([os.getcwd(), "templates", "web", self.conf["form"] ])
 
        self._print_info()
    
    def _print_info(self):
        """print app info"""
        
        print (self.conf)

    def run(self):
        """
        run code generator
        """
        
        models = self.jsonm.get_json()
        
        
        for model in models:
            
            table_name = model["_table"]
            print (">>:%s" % (table_name) )
            
            attrs = model["properties"]
            
            try:
            
                if "web" in self.conf["addons"]:
                    #generate html file [form]
                    print("- gen web")
                    gen_form(self.tpl_form, table_name, attrs)
                
                if "pytest" in self.conf["addons"]:
                    
                    #generate unit test py file
                    print("- gen pytest")
                    gen_unittest(table_name, attrs)
                
            except Exception as ex:
                print (ex.message)
            
if __name__ == "__main__":
    
    cgen = CodeGen()
    
    cgen.run()