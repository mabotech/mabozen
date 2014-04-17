# -*- coding: utf-8 -*-

import os
import glob

import re

class Loader(object):
    
    def __init__(self):
        """  init db  """
        
    
    def exists(self, funcaion_name):
        """ check if function exists"""
        
        
        return False

    def load(self, obj):
        """ load pg functoin"""
        
        spname = obj[0]
        filename = obj[1]
        digest = obj[2]
        
        if digest != 0:
            print digest
        with open(filename, 'r') as fileh:
            sql = fileh.read()

    def run(self):
        """run load"""
        
        funcs_dict = {}

        functions = glob.glob(r"E:\mabodev\maboss\database\functions\*.sql")

        for func in functions:
            
            v = os.stat(func)
            ctime =  v.st_ctime
            
            c = re.split("\@|\.", func)
            
            function_name =  c[0]
            
            if function_name in funcs_dict:
                if ctime > funcs_dict[function_name][0]:
                    funcs_dict[function_name] = [ctime, func, c[1]]
                else:
                    print (func)
            else:
                funcs_dict[function_name] = [ctime, func, 0]
                
        for i in funcs_dict:
            
            filename = funcs_dict[i][1]
            
            self.load(funcs_dict[i])
           
def main():
    
    loader = Loader()
    loader.run()
    
    
if __name__ == "__main__":
    main()