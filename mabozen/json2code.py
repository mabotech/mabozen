# -*- coding: utf-8 -*-

"""
json to code [unittest, html]
"""

from time import strftime, localtime

#from jinja2 import Environment, FileSystemLoader

from mako.template import Template
from mako import exceptions

#from faker import Factory

#lib

#from mabozen.lib.pg import Pg

from mabozen.lib.utils import get_class_name
from mabozen.lib.utils import save_html, save_file
from mabozen.lib.utils import save_models

from mabozen.schema2json import JsonModels

from mabozen.lib.build_models import build

#########################################
#
class CodeGen(object):
    """
    pg schema extractor
    """
   
    def __init__(self):
        """
        init db
        """
        
        #conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        #self.dbi = Pg(conn_string)
        
        self.jsonm = JsonModels()
        

    def _gen_html_form(self, table_name, attrs):
        """
        as a function ?
        from json to form? now from schema dict to form.
        """
        
        #table_name = obj["_table"]
        
        class_name = get_class_name(table_name)
        
        #table = {}
        
        """
        attrs = []
        
        for property in attrs:#obj["properties"]:
            v = {}
            v["name"] = property["name"]
            v["type"] = property["type"]
            attrs.append(v)            
        """
        #template = self.env.get_template('html/form.html')

        #v = template.render(class_name=class_name, table = table_name, attrs = attrs)        
        
        try:
        
            template = Template(filename="templates/html/form_mako.html",   disable_unicode=True, input_encoding='utf-8')

            content = template.render(class_name=class_name, table = table_name, attrs = attrs)
            
        except:
            
            print exceptions.text_error_template().render()        
            
            raise Exception("render error")
        #print(v)        
        
        filename = "../output/form_%s.html" % (table_name)
        
        save_html(filename, content)
        

    def _gen_test_case(self, table_name, model):
        """
        change to mako template?
        """
        
        #table_name = obj["_table"]

        #template = self.env.get_template('test/test_single_table_mako.py')
        
        """
        t = table_name.split("_")
        
        xs = []
        for i in t:
            x = i.capitalize()
            xs.append(x)
        """
        class_name = get_class_name(table_name)
        
        #table = {}
        
        attrs = []
        
        #print model
        
        for property in model:#["properties"]:
            #print (property)
            #print (property["name"]),
            #print (property["type"])
            if property["type"] in ["varchar", "bpchar"]:
                if "maximum_length" in property:
                    mlen = property["maximum_length"]
                else:
                    mlen = ""
                v = "get_word(%s)" % (mlen)
                attr = '"%s":%s' %(property["name"], v)          
                """
                elif property["type"] in ["bpchar"]:
                    mlen = property["maximum_length"]
                    v = "self.get_bpchar(%s)" % (mlen)
                    attr = '"%s":%s' %(property["name"], v)                
            """
            elif property["type"] in ['hstore']:
                attr = '"%s":"hstore(\'1033\',%s)"' %(property["name"], "get_word()")  
                
            #elif property["type"] in ['json']:
            #    attr = '"%s":"{}"' %(property["name"])                  
            
            elif property["type"] == 'date':
                attr = '"%s":%s' %(property["name"], "self.fake.date()")  
            
            elif property["type"] in ['datetime']:
                attr = '"%s":%s' %(property["name"], "self.fake.date_time()")  
            elif property["type"] in ['timestamptz']:
                attr = '"%s":"now()"' %(property["name"])                 
            elif property["type"]  in ['int4','numeric']:
                attr = '"%s":%s' %(property["name"], "self.fake.random_int()")           
            elif property["type"]  in ['int2']:
                attr = '"%s":1' %(property["name"])                   
            else:
                v = "self.fake.%s()" % (property["type"] )
                attr = '"%s":%s' %(property["name"], v)  
            
            attrs.append( attr )        
    
        #x = attrs.split("\n")
        z = []
        i = 0
        for y in attrs:
            i = i + 1
            if i >1:
                j = 16
            else:
                j = 0
                
            z.append(" "* j+y.lstrip())
            
        attrs = ",\n".join(z)

        #content = template.render(class_name=class_name, table = table_name, attrs = attrs)
        
        #print(v)
        
        try:
        
            template = Template(filename="templates/test/test_single_table_mako.py",   disable_unicode=True, input_encoding='utf-8')

            content = template.render(class_name=class_name, table = table_name, attrs = attrs)
            
        except:
            
            print exceptions.text_error_template().render()        
            
            raise Exception("render error")
        
        filename = "../test/test_%s.py" % (table_name)
        
        save_file(filename, content)      

        
    def gen_html_list(self, obj):
        """
        
        """
        pass
        
    def gen_js(self, obj):
        """
        
        """
        pass
    
    def run(self):
        """
        run extraxtor
        """ 

        models = self.jsonm.get_json()
        
        #print models
        
        self.gen_code(models)
        
    def gen_code(self, i_models):
        
        for model in i_models:
            
            table_name = model["_table"]
            attrs = model["properties"]
            #print (table_name)            
            self._gen_html_form(table_name, attrs)
            
            self._gen_test_case(table_name, attrs)
            
if __name__ == "__main__":
    
    cgen = CodeGen()
    
    cgen.run()