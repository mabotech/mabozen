

import re


# json schema

def match(line):

    # common variables

    rawstr = r"""i_json\.(\w+)"""

    # method 1: using a compile object
    compile_obj = re.compile(rawstr)
    match_obj = compile_obj.search(line)

    # method 2: using search function (w/ external flags)
    #match_obj = re.search(rawstr, line)

    # method 3: using search function (w/ embedded flags)
    #match_obj = re.search(embedded_rawstr, line)

    # Retrieve group(s) from match_obj
    #all_groups = match_obj.groups()

    # Retrieve group(s) by index
    if match_obj:
        group_1 = match_obj.group(1)
        return group_1
    else:
        return None




def main():
    
    
    z = set()

    with open("../../working/add_genealogy_cf1.sql","r") as fileh:
        
        code = fileh.read()
        
        
    #print(code)

    for line in code.split("\n"):
        
        if len(line) == 0:
            continue
        
        if line[0] == '#':
            continue
        else:
            x =match(line)
            if x != None:
                z.add(x)
            
    
    print(z)
        
if __name__ == "__main__":
    main()