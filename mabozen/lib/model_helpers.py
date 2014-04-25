# -*- coding: utf-8 -*-

"""
model helpers
"""

import json

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