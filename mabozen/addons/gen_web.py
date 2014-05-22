# -*- coding: utf-8 -*-

"""
json to code [unittest]
"""
import os
import hashlib
import logging

import re

#import json

from mako.template import Template
from mako import exceptions

from mabozen.lib.utils import get_class_name
#from mabozen.lib.utils import save_html, save_file

logger = logging.getLogger("web")

def coffee_preprocessor(source):
    """
    keep coffee comment in mako template.
    """
    
    # redefine mako inline mark.
    #source = re.sub(r"\${(.+?)}", r"${'${'}\1${'}'}", source)
    #source = re.sub(r"\@\[(.+?)\]", r"${\1}", source)
    
    source = re.sub(r"##", r"${'##'}", source)
    return source

def save_code(out_path, content):
    """real save"""
    with open(out_path, 'w') as fileh:
        content = content.replace('\r\n', '\n') #unix CRLF to windows LF
        fileh.write( content ) 

def save(out_path, file_type, content):
    """
    save code, archive if exist file has different content
    """
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
            old_file = ".".join([out_path.replace("."+file_type, ""), \
                old_hexdigest, file_type])
            print(old_file)
            print(out_path)
            os.rename(out_path, old_file)
            save_code(out_path, content)
        else:
            print("generated")
            
    else:
        save_code(out_path, content)
    
    
def gen_code(conf,  tpl_group, tpl_name, table_meta):
    """
    as a function ?
    from json to form? now from schema dict to form.
    """
    
    table_name = table_meta["table"]
    pkey = table_meta["pkey"]
    attrs = table_meta["attrs"]
    
    file_type = conf["FILE_TYPE"] 
    
    class_name = get_class_name(table_name) 
    
    tpl_path = os.sep.join([conf["TPL_ROOT"], "web",  tpl_group, \
        "%s_mako.%s" % (tpl_name, file_type) ])
    
    out_path = os.sep.join([conf["OUT_ROOT"], "web", table_name, \
        "%s.%s" % (tpl_name, file_type) ])

    #print(tpl_path)
    #print(out_path)
    try:
        # mako template
        template = Template(filename=tpl_path, disable_unicode=True, \
            input_encoding='utf-8', preprocessor = coffee_preprocessor)

        content = template.render(class_name=class_name, \
            table_name = table_name, pkey=pkey, attrs = attrs)
        
    except Exception as ex:
        
        print (exceptions.text_error_template().render()  )
        print(ex.message)
        raise Exception("render error")

    save(out_path, file_type, content)
    

def gen_web(conf, table_meta):
    """
    generate web app    
    """
    
    #gen form
    
    #print(table_name)
    #print(json.dumps(attrs, sort_keys=True, indent=2, separators=(',', ': ')))
    
    tpl_group = "angular"    

    
    templates = [
                    #("html","index"),
                    ("coffee", "form2"),  
                    ("coffee","table"),
                    ("coffee","app"),
                    #("html","list"),
                    #("js","list"),
                    #("html","form"),
                    #("js","form")
                ]
    
    for item in templates:        
        #print(item) 
        conf["FILE_TYPE"]  = item[0]
        tpl_name = item[1]
        gen_code(conf, tpl_group, tpl_name, table_meta)
    

    
    