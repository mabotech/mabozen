
"""

construct json module

"""
def build(table_name, cols):
    """
    build dict
    """

    """
    {"table":"company",
"properties":[
{"name":"company", "column":"company", "type":"varchar(10)", "required":true, "isUnique":true},
{"name":"text", "column":"texths",  "type":"hstore"}
]
}
    """
    
    tab = {"_table":table_name}
    tab["comment"] = table_name
    tab["properties"] = []
    
    for col in cols:
        
        #filter fuid column
        if col["column_name"] == 'fuid':
            continue
        
        # convert
                    
        attr = {}
        
        attr["name"] = col["column_name"]
        
        attr["column"] = col["column_name"]
        
        attr["comment"] = col["column_name"]
        
        if col["udt_name"] in [ "varchar", "bpchar"]:
            #attr["type"] = "%s(%s)" % ( col["udt_name"], col["character_maximum_length"]  )
            attr["type"] = col["udt_name"]
            if col["character_maximum_length"] == None:
                attr["maximum_length"] = 30
            else:
                attr["maximum_length"] = col["character_maximum_length"]
            
        else:
            attr["type"] = col["udt_name"]
            
        #if col["isUnique"] == "NO":
        #     attr["unique"] = True
             
        if col["is_nullable"] == "NO":
            attr["required"] = True
        
        tab["properties"].append(attr)           
    
    return tab 