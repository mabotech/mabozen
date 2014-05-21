# -*- coding: utf-8 -*-

"""
json to code [unittest]
"""
import os
import hashlib
import logging

import json

from mako.template import Template
from mako import exceptions

from mabozen.lib.utils import get_class_name
from mabozen.lib.utils import save_html, save_file

logger = logging.getLogger("web")

def gen_code(conf,  jslib, template_type, table_name, attrs):
    """
    as a function ?
    from json to form? now from schema dict to form.
    """
    file_type = conf["FILE_TYPE"] 
    
    class_name = get_class_name(table_name) 
    
    tpl_path = os.sep.join([conf["TPL_ROOT"], "web",  jslib, "%s_mako.%s" % (template_type, file_type) ])
    
    out_path = os.sep.join([conf["OUT_ROOT"], "web", table_name,  "%s.%s" % (template_type, file_type) ])

    print(tpl_path)
    print(out_path)
    try:
    
        template = Template(filename=tpl_path,   disable_unicode=True, input_encoding='utf-8')

        content = template.render(class_name=class_name, table_name = table_name, attrs = attrs)
        
    except Exception as ex:
        
        print (exceptions.text_error_template().render()  )
        
        raise Exception("render error")

    #save_html(out_path, content)
    dirname =  os.path.dirname(out_path) 
    
    if not os.path.exists( dirname):        
        os.makedirs(dirname)
        
    #modified on 2014-05-03 17:16:18
    #content = content.replace("\n","")
    
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
            print(old_file)
            print(out_path)
            os.rename(out_path, old_file)
            
    
    with open(out_path, 'w') as fileh:
        content = content.replace('\r\n', '\n') #unix CRLF to windows LF
        fileh.write( content )
    

def gen_web(conf, table_name, attrs):
    """
    generate html    
    """
    
    #gen form
    
    print(table_name)
    print(json.dumps(attrs, sort_keys=True, indent=2, separators=(',', ': '))  )
    
    jslib = "angular"
    
    """
    template_type = "form" 
    conf["FILE_TYPE"] = "html"
    
    gen_code(conf, jslib, template_type, table_name, attrs)

    template_type = "list" 
    conf["FILE_TYPE"] = "html"
    
    gen_code(conf,  jslib, template_type, table_name, attrs)

    #gen index
    template_type = "index"
    conf["FILE_TYPE"]  = "html"
    gen_code(conf,  jslib, template_type, table_name, attrs)
    
    #gen app
    template_type = "form"
    conf["FILE_TYPE"]  = "js"
    gen_code(conf,  jslib, template_type, table_name, attrs)
    
    """
    
    #gen app
    template_type = "form2"
    conf["FILE_TYPE"]  = "coffee"
    gen_code(conf,  jslib, template_type, table_name, attrs)
    
    """
    template_type = "list"
    conf["FILE_TYPE"]  = "js"
    gen_code(conf,  jslib, template_type, table_name, attrs)
    
    #gen controller
    template_type = "app"
    conf["FILE_TYPE"]  = "js"
    gen_code(conf,  jslib, template_type, table_name, attrs)
    """
    
    