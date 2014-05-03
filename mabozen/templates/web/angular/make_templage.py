
import os
import hashlib

from time import strftime, localtime
from datetime import datetime

def compare(content, file_name):

    md5 = hashlib.md5()

    md5.update(content)

    hexdigest = md5.hexdigest()
    
    with open(file_name, "r") as fileh:
        content_o = fileh.read()
    
    md5_o = hashlib.md5()
    md5_o.update(content_o)
    hexdigest_o = md5_o.hexdigest()
    
    if hexdigest == hexdigest_o:
        return True
    else:
        return False
        
def save(content, filename):
    
    with open(filename, "w") as fileh:
        fileh.write(content)   
    
    
def make_template():
    
    src_file = "list.js"
    
    with open(src_file, "r") as src:
        content = src.read()
        
    content = content.replace("Company", "${class_name}")
    content = content.replace("company", "${table_name}")
    
    # replace model, etc.    
    
    dst_file = "list_mako.js"
    
    if not os.path.exists(dst_file):
        
        save(content, dst_file)
    
    else:        
        
        if compare(content, dst_file):
            #same content
            pass
        else:
            #backup and create new file
            statinfo = os.stat(dst_file)
            
            #rename will keep the old st_ctime on winfows
            dt = strftime("%Y%m%d_%H%M%S", localtime(statinfo.st_atime))
            
            new_name = "list_mako_%s.js" % (dt)
            
            #print dst_file
            #print new_name
            
            os.rename(dst_file, new_name)
            
            save(content, dst_file)
            
        
if __name__ == '__main__':
    
    make_template()
