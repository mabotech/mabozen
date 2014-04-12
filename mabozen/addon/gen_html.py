# -*- coding: utf-8 -*-

"""
json to code [unittest]
"""

from mako.template import Template
from mako import exceptions

from mabozen.lib.utils import get_class_name
from mabozen.lib.utils import save_html, save_file

def gen_form(path_tpl, table_name, attrs):
    """
    as a function ?
    from json to form? now from schema dict to form.
    """

    class_name = get_class_name(table_name) 
    
    try:
    
        template = Template(filename=path_tpl,   disable_unicode=True, input_encoding='utf-8')

        content = template.render(class_name=class_name, table = table_name, attrs = attrs)
        
    except Exception as ex:
        
        print (exceptions.text_error_template().render()  )
        
        raise Exception("render error")

    filename = "../output/form_%s.html" % (table_name)
    
    save_html(filename, content)
    

def gen_html():
    """
    generate html    
    """
    
    #gen index
    filename_tpl = ""
    filename_out = ""
    
    #gen app
    filename_tpl = ""
    filename_out = ""
        
    #gen form
    filename_tpl = ""
    filename_out = ""
        
    #gen controller
    filename_tpl = ""
    filename_out = ""
        
    pass
    
    