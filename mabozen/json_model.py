# -*- coding: utf-8 -*-

"""
pg schema to json [model]
"""
import json
from time import strftime, localtime

#lib
from mabozen.config import get_db_config
from mabozen.config import logging

logger = logging("zen_db2json")

from mabozen.zen_factory import ZenFactory

class JsonModel(object):
    """
    schema extractor
    add ora schema to json?
    """
   
    def __init__(self):
        """init schema instance"""
        logger.debug("init")
        
        ZEN_CFG = get_db_config()
        
        zenfactoy = ZenFactory(ZEN_CFG['DB_URL'])
        
        self.schema = zenfactoy.get_schema()
       
    def _get_tables_from_csv(self):
        """
        get table list form csv
        """
    
    
    @classmethod    
    def _build_model(cls, table_name, cols):
        
        #print ( json.dumps(cols, sort_keys=True, indent=2, separators=(',', ': '))  )
        print(table_name)
        """
        build dict
        """
       
        tab = {"_table":table_name}
        tab["comment"] = table_name
        tab["properties"] = []
        
        #original pk
        tab["o_pk"] = []
        
        pos_set = set()
        
        
        column_names = set()
        constraint_names = set()
        
        
        has_pk = 0
        for col in cols:
            
            #print(col)
            #print ( json.dumps(col, sort_keys=True, indent=2, separators=(',', ': '))  )
            #filter fuid column
            if col["column_name"] == 'fuid':
                #continue
                pass
            
            # convert
                        
            attr = {}
            
            o_pos = col["ordinal_position"]
            
            
            
            if o_pos not in pos_set:
                pos_set.add(o_pos)
            else:
                #continue         
                pass
                
            #attr["name"] = col["column_name"]   
            
            #convert
            if col["column_name"] == "textid":                
                
                if "texths" in column_names:
                    #attr["column"] = "texths2"
                    continue
                else:
                    attr["_pos"] = col["ordinal_position"]   
                    attr["column"] = "texths"
                    
                    #not null?
                    #attr["required"] = True
                    column_names.add("texths")
                    
                attr["type"] = "hstore"
                
                
                
                tab["properties"].append(attr)
                continue
            
            if not col["not_composite"]:
                col["not_composite"] = 0
            
            if col["not_composite"] > 1:
                if col["constraint_type"] == 'f':
                    if col["constraint_name"] in constraint_names:
                        pass
                    else:
                        
                        #if attr["column"] in column_names:
                        constraint_names.add( col["constraint_name"])
                        
                        attr["_pos"] = col["ordinal_position"]
                        
                        if col["rel_table_name"] in column_names:
                            if  col["rel_table_name"] +"_id2" in column_names:
                                attr["column"] = col["rel_table_name"] +"_id3"
                            else:
                                attr["column"] = col["rel_table_name"] +"_id2"
                        else:
                            attr["column"] = col["rel_table_name"]
                        column_names.add(attr["column"])
                        attr["comment"] ="composite"
                        attr["fk"] = True
                        attr["ref"] = {}
                        attr["ref"]["table"] = col["rel_table_name"]
                        attr["ref"]["column"] = "id"# col["rel_column_name"]
                        attr["type"] = "int4"
                        tab["properties"].append(attr) 

                elif col["constraint_type"] == 'p':
                    
                    if col["column_name"] in column_names:
                        pass                    
                    elif has_pk == 1:
                        #
                        print("->"*20)
                        attr["_pos"] = col["ordinal_position"]
                        attr["column"] = col["column_name"]
                        attr["comment"] = "original composite pk2"
                        attr["type"] = col["data_type"]
                        
                        if col["data_type"] in [ "varchar", "bpchar"]:
                            #attr["type"] = "%s(%s)" % ( col["udt_name"], col["character_maximum_length"]  )
                            if col["character_maximum_length"] == None:
                                attr["maximum_length"] = 30
                            else:
                                attr["maximum_length"] = col["character_maximum_length"]                        
                        
                        attr["required"] = True                        
                        tab["properties"].insert(1, attr)                             
                    else:
                        #add new pk
                        pk =  {
                          "_pos": "0",
                          "column": "id",
                          "comment":"new id",
                          "pk": True,
                          "required": True,
                          "type": "int4"
                        }
                        tab["properties"].insert(0, pk)
                        column_names.add("id")
                        
                        has_pk = 1
                        
                        #
                        
                        attr["_pos"] = col["ordinal_position"]
                        attr["column"] = col["column_name"] 
                        attr["comment"] = "original composite pk"
                        attr["type"] = col["data_type"]
                        attr["required"] = True       


                        if col["data_type"] in [ "varchar", "bpchar"]:
                            #attr["type"] = "%s(%s)" % ( col["udt_name"], col["character_maximum_length"]  )
                            if col["character_maximum_length"] == None:
                                attr["maximum_length"] = 30
                            else:
                                attr["maximum_length"] = col["character_maximum_length"]
                        
                        tab["properties"].insert(1, attr)
                        column_names.add(attr["column"])
                        
                #next loop        
                continue
                        

            #start                 
            attr["column"] = col["column_name"]   
            
            attr["_pos"] = col["ordinal_position"]            
            #attr["comment"] = col["column_name"]
            
            if col["constraint_type"] == "f":
                attr["fk"] = True
                if col["column_name"] in column_names:
                    attr["column"] = col["rel_table_name"]+"_id2"
                attr["ref"] = {}
                attr["ref"]["table"] = col["rel_table_name"]
                attr["ref"]["column"] = col["rel_column_name"]
            elif col["constraint_type"] == "p":
                has_pk = 1
                if col["column_name"] in column_names:
                    
                    pk =  {
                      "_pos": "0",
                      "column": "id",
                      "comment":"new id(single)",
                      "pk": True,
                      "required": True,
                      "type": "int4"
                    }
                    tab["properties"].insert(0, pk)
                    column_names.add("id")
                    continue
                else:
                
                    attr["pk"] = True
                    
                    tab["o_pk"].append(col["column_name"] )

            column_names.add(attr["column"])
            if col["data_type"] in [ "varchar", "bpchar"]:
                #attr["type"] = "%s(%s)" % ( col["udt_name"], col["character_maximum_length"]  )
                attr["type"] = col["data_type"]
                if col["character_maximum_length"] == None:
                    attr["maximum_length"] = 30
                else:
                    attr["maximum_length"] = col["character_maximum_length"]
                
            else:
                attr["type"] = col["data_type"]
                
            #if col["isUnique"] == "NO":
            #     attr["unique"] = True
            
            if col["not_null"] == True:
                attr["required"] = True
            
            tab["properties"].append(attr)           
        
        pkcount = len(tab["o_pk"])
        
        if has_pk == 0:
        
            #for i in range(0, pkcount):
            #    tab["properties"][i]["pk"]=False
            
            pk =  {
              "_pos": "0",
              "column": "id",
              "pk": True,
              "required": True,
              "type": "int4"
            }
            tab["properties"].insert(0, pk)
            
        return tab 

        
    def _save_json(self, table_names, models):
        """
        save models in json file
        """
        
        #save_models(filename, models) 
        
        if type(table_names[0]) != str:
            table_names = map(lambda tab : tab[0], table_names)
        
        info = {"_version":"0.2", "by":"mabozen","tables":table_names}    
        models_def = {"info":info,"models":models}
        
        filename = "../models/models_%s.json" % (strftime("%Y%m%d%H%M%S", localtime()))
        
        with open("models_last.txt",'w') as fileh:
            logger.debug(filename)
            fileh.write(filename)   
        
        
        #md5 check?
        
        with open(filename, 'w') as fileh:
        
            json_str = json.dumps(models_def, sort_keys=True, indent=2, separators=(',', ': '))        
            fileh.write(json_str) 
        
        
    def _get_models(self, table_names):
        """run extraxtor""" 
        models = []
        
        for tabname in table_names:
            
            #from []
            if type(tabname) == str:                
                table_name = tabname                
            #from sql query
            else:            
                table_name = tabname[0]
                
            tab_dict = self.schema.query_table_schema(table_name)   #self._get_schema(table_name)

            if tab_dict != None:
                #build model as json.
                model = self._build_model(table_name, tab_dict)
                models.append(model)
            else:
                msg = "not table: [%s]" % (table_name)
                raise Exception(msg)
        
        return models
        
    def get_json(self, filename):
        
        with open(filename, 'r') as fileh:
            
            json_model = fileh.read()
        
        return json.loads(json_model)
        
    def run(self, table_names):
        """run model dumps"""
        
        if len(table_names) == 0:
            table_names =self.schema.get_tables()
            
        models = self._get_models(table_names)

        self._save_json(table_names, models)     

            
if __name__ == "__main__":
    
    json_m = JsonModel()
    table_names = [] # ["company","facility","text_translation","work_shift"]
    json_m.run(table_names)