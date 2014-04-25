# -*- coding: utf-8 -*-

"""
helpers & utils
"""

import json



def get_class_name(table_name):
    """
    construct class name from table name with underscore(_) inside
    """
    
    wordlist = table_name.split("_")
    
    parts = []
    
    for word in wordlist:
        
        cap_word = word.capitalize()
        
        parts.append(cap_word)
    
    class_name = "".join(parts)
    
    return class_name


def save_html(filename, content):
    """
    save content
    TODO: file compare (md5.digest)
    """
    
    with open(filename, 'w') as fileh:
        fileh.write(content.replace("\n","") )
  
def save_file(filename, content):
    """
    save file
    TODO: file compare (md5.digest)
    """
    
    with open(filename, 'w') as fileh:
        fileh.write(content.replace("\n\n","\n"))        

## obsolete
def save_models(filename, models):
    """
    save models to json file
    """   
    
    info = {"version":"0.1", "by":"mabo"}
    
    models_def = {"info":info, "models":models}
    
    with open(filename, 'w') as fileh:
        
        json_str = json.dumps(models_def, sort_keys=True, indent=4, separators=(',', ': '))
        
        fileh.write(json_str)        