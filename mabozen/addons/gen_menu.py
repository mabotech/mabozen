
"""

gen menu page for testing

"""
import os
import hashlib

from mako.template import Template
from mako import exceptions


def gen_menu(conf, tables):
    
    file_type = conf["file_type"] 
    template_type =conf["template_type"]
    
    tpl_path = os.sep.join([conf["tpl_root"], "web", "%s_mako.%s" % (template_type, file_type) ])
    
    out_path = os.sep.join([conf["out_root"], "web",  "%s.%s" % (template_type, file_type) ])

    print(tpl_path)
    print(out_path)
    try:
    
        template = Template(filename=tpl_path,   disable_unicode=True, input_encoding='utf-8')

        content = template.render(tables = tables)
        
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
    