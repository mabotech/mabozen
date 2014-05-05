# -*- coding: utf-8 -*-

"""
model helpers
"""

import re

def make_class_name(table_name):
    """
    construct class name from table name, underscore(_) split and capitalize.
    """
    
    wordlist = table_name.split("_")
    
    parts = []
    
    for word in wordlist:
        
        cap_word = word.capitalize()
        
        parts.append(cap_word)
    
    class_name = "".join(parts)
    
    return class_name
    
def get_foreign_table(column_name):
    """ get foreign table name from column name """
    rawstr = r"""(.*)_id\d?"""
    compile_obj = re.compile(rawstr,  re.IGNORECASE| re.MULTILINE| re.DOTALL)
    match_obj = compile_obj.search(column_name)

    if match_obj:

        # Retrieve group(s) by index
        return match_obj.group(1)
    else:
        return None 