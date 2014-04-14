# -*- coding: utf-8 -*-

"""
json to code [unittest]
"""
import os
import hashlib

from mako.template import Template
from mako import exceptions

from mabozen.lib.utils import get_class_name
from mabozen.lib.utils import save_html, save_file

def gen_code(conf, template_type, table_name, attrs):
    """
    as a function ?
    from json to form? now from schema dict to form.
    """
    file_type = conf["file_type"] 
    
    class_name = get_class_name(table_name) 
    
    tpl_path = os.sep.join([conf["tpl_root"], "web", "%s_mako.%s" % (template_type, file_type) ])
    
    out_path = os.sep.join([conf["out_root"], "web", table_name,  "%s.%s" % (template_type, file_type) ])

    print(tpl_path)
    print(out_path)
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
    
    md5 = hashlib.md5()

    md5.update(content)

    hexdigest = md5.hexdigest()
    
    old_hexdigest = hexdigest
    
    if os.path.exists(out_path):
        
        with open(out_path, 'r') as fileh:
            
            md5 = hashlib.md5()
            old_content = fileh.read()
            md5.update(old_content)

            old_hexdigest = md5.hexdigest()
            
    
    
    if hexdigest != old_hexdigest:
        old_file = ".".join([out_path.replace("."+file_type, ""), old_hexdigest, file_type])
        os.rename(out_path, old_file)
            
    
    with open(out_path, 'w') as fileh:
        fileh.write( content )
    

def gen_web(conf, table_name, attrs):
    """
    generate html    
    """
    
    #gen form
    
    
    template_type = "form" 
    conf["file_type"] = "html"
    
    gen_code(conf, template_type, table_name, attrs)

    template_type = "list" 
    conf["file_type"] = "html"
    
    gen_code(conf, template_type, table_name, attrs)

    #gen index
    template_type = "index"
    conf["file_type"]  = "html"
    gen_code(conf, template_type, table_name, attrs)
    
    #gen app
    template_type = "form_ctrl"
    conf["file_type"]  = "js"
    gen_code(conf, template_type, table_name, attrs)

    template_type = "list_ctrl"
    conf["file_type"]  = "js"
    gen_code(conf, template_type, table_name, attrs)
    
    #gen controller
    template_type = "app"
    conf["file_type"]  = "js"
    gen_code(conf, template_type, table_name, attrs)
    