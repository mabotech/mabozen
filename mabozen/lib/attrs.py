# -*- coding: utf-8 -*-

""" frontend helper """

import json
from collections import OrderedDict

#from itertools import imap

class AttrsHelper(object):
    """ form / list attributes helper """
    
    def __init__(self, indent):
        """ init """
        
        #datatype mapping
        self.type_mapping = {
            "varchar":"text",
            "char":"text",
            "datetime":"datetime",
            "date":"date",
            "time":"time"
            }
            
        self.common = ["modifiedon", "modifiedby",
                "createdon", "createdby", "rowversion"]
        
        self.indent = indent
        
        self.model_def = None
        
        self.attr_list = []        
    
    def prepare(self, table_name, attrs):
        """ prepare data """
        
        for attr in attrs:
            
            col = attr["column"]
            
            if col == "company":#"default_value" in attr:
                default = "%s" % (attr["type"])
            else:
                default = None
                
            self.attr_list.append((col, default))
        
        common_list = [(x, None) for x in self.common]
        self.attr_list.extend(common_list)       
        
        return self.make_model_def(table_name)
        #default_list.extend(['null' for i in range(0, len(common))])
        
        #z = imap(pairs, attr_list, default_list)
        # add datatype comment:  facility:null, /* text(5) */
        #print ",\n".join(z)
        
    def make_model_def(self, table_name):
        """ make model defination """
        
        obj = OrderedDict(self.attr_list)
        
        obj_str = "".join([table_name, " = \n", json.dumps(obj, \
            sort_keys=False, indent=4, separators=(',', ': ')) ])
            
        lines = [" " * self.indent +line for line in obj_str.split("\n")] 
        
        self.model_def = "\n".join(lines)
        
    def make_select2_load(self):
        """ for html select2 """
       
    def make_table_head(self):
        """ column limit defination? """
        
    def make_table_body(self):
        """ from html table body """
        
    def make_form(self):
        """ 
        datatype -> html input type 
        foreign key -> select2
        """
        
    
def main():    
    """ main """
    
if __name__ == '__main__':
    
    main()
