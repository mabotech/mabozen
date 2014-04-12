# -*- coding: utf-8 -*-

"""
json to code [unittest]
"""

import os

from mako.template import Template
from mako import exceptions

from mabozen.lib.utils import get_class_name
from mabozen.lib.utils import save_file


def make_attrs(table_name, model):
       
   
    attrs = []
    
    for column in model:

        if column["type"] in ["varchar", "bpchar"]:
            
            if "maximum_length" in column:
                mlen = column["maximum_length"]
            else:
                mlen = ""
            fake_func = "get_word(%s)" % (mlen)
            attr = '"%s":%s' % (column["name"], fake_func)          

        elif column["type"] in ['hstore']:
            attr = '"%s":"hstore(\'1033\',%s)"'  % (column["name"], "get_word()")  
            
        #elif column["type"] in ['json']:
        #    attr = '"%s":"{}"' %(column["name"])                  
        
        elif column["type"] == 'date':
            attr = '"%s":%s' % (column["name"], "self.fake.date()")  
        
        elif column["type"] in ['datetime']:
            attr = '"%s":%s' % (column["name"], "self.fake.date_time()")  
        elif column["type"] in ['timestamptz']:
            attr = '"%s":"now()"' % (column["name"])                 
        elif column["type"]  in ['int4','numeric']:
            attr = '"%s":%s' % (column["name"], "self.fake.random_int()")           
        elif column["type"]  in ['int2']:
            attr = '"%s":1' % (column["name"])                   
        else:
            fake_func = "self.fake.%s()" % (column["type"] )
            attr = '"%s":%s' % (column["name"], fake_func)  
        
        attrs.append( attr )    
        
        return attrs
        
def gen_unittest(conf, table_name, model):
    """
    change to mako template?
    """
    
    class_name = get_class_name(table_name) 
    
    attrs = make_attrs(table_name, model)
    
    just_line = []
    i = 0
    for attr in attrs:
        i = i + 1
        if i > 1:
            j = 16
        else:
            j = 0
            
        just_line.append(" "* j + attr.lstrip())
        
    attrs = ",\n".join(just_line)
    
    try:
        
        template_file = os.sep.join([conf["tpl_root"], "test", "test_single_table_mako.py"])
        
        template = Template(filename=template_file,   \
                                        disable_unicode=True, input_encoding='utf-8')

        content = template.render(class_name=class_name,  \
                                        table = table_name, attrs = attrs)
        
    except Exception as ex:
        
        print exceptions.text_error_template().render()        
        
        raise Exception("render error")
    
    filename = os.sep.join( [ conf["test_root"], "tables","test_%s.py" % (table_name) ] )
    
    save_file(filename, content)   