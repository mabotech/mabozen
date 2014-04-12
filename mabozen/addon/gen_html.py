# -*- coding: utf-8 -*-

"""
json to code [unittest]
"""
import os
import md5

from mako.template import Template
from mako import exceptions

from mabozen.lib.utils import get_class_name
from mabozen.lib.utils import save_html, save_file

def gen_form(conf, template_type, table_name, attrs):
    """
    as a function ?
    from json to form? now from schema dict to form.
    """

    class_name = get_class_name(table_name) 
    
    tpl_path = os.sep.join([conf["tpl_root"], "web", "%s_mako.html" % (template_type) ])
    
    out_path = os.sep.join([conf["out_root"], "web", table_name,  "%s_form.html" % (table_name) ])

    
    try:
    
        template = Template(filename=tpl_path,   disable_unicode=True, input_encoding='utf-8')

        content = template.render(class_name=class_name, table = table_name, attrs = attrs)
        
    except Exception as ex:
        
        print (exceptions.text_error_template().render()  )
        
        raise Exception("render error")

    #save_html(out_path, content)
    dirname =  os.path.dirname(out_path) 
    
    if not os.path.exists( dirname):        
        os.makedirs(dirname)
        
    content = content.replace("\n","")
    
    md5v = md5.new()

    md5v.update(content)

    hexdigest = md5v.hexdigest()
    
    old_hexdigest = hexdigest
    
    if os.path.exists(out_path):
        
        with open(out_path, 'r') as fileh:
            
            md5v = md5.new()
            old_content = fileh.read()
            md5v.update(old_content)

            old_hexdigest = md5v.hexdigest()
    
    if hexdigest != old_hexdigest:
        old_file = ".".join([out_path.replace(".html", ""), old_hexdigest, "html"])
        os.rename(out_path, old_file)
            
    
    with open(out_path, 'w') as fileh:
        fileh.write( content )
    

def gen_html(conf, table_name, attrs):
    """
    generate html    
    """
    
    #gen index
    
    
    template_type = "form"  
    
    gen_form(conf, template_type, table_name, attrs)
    
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
    
    