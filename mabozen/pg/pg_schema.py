# -*- coding: utf-8 -*-


"""
get PostgreSQL schema information from db information schema
"""

import logging

import json

from mabozen.lib.pg import Pg

logger = logging.getLogger("schema")

class PgSchema(object):
    """ class for query PostgreSQL schema information"""

    def __init__(self, components):
        """  init db connection """
                
        logger.debug("init PgSchema")
        
        #catalog == dbname
        #schema == username
        
        self.catalog = components["database"]
        
        self.schema = components["username"]
        
        #conn_string = "port=%s dbname=%s user=%s password=%s" % (port, dbname, username, password)
        
        self.dbi = Pg(components)

    def get_functions(self):
        """
        get functions name from schema.
        """
        
        sql = """  select p.proname 
from pg_proc p 
LEFT JOIN pg_type t1 ON p.prorettype=t1.oid
LEFT JOIN pg_authid a ON p.proowner=a.oid
left join pg_catalog.pg_namespace ns on  p.pronamespace = ns.oid
where ns.nspname = '%(schema)s'  and proname not like 'uuid%%'
        """ % {"schema":self.schema}
        
        self.dbi.execute(sql)
        
        rows = self.dbi.fetchall()
        
        proc_list = []
        
        for row in rows:
            proc_list.append(row[0])
        
        return  proc_list        
        
    def function_exists(self, function_name):
        """ check function exists """
        
        sql = """select count(1) from pg_proc p
LEFT JOIN pg_authid a ON p.proowner=a.oid
where proname = '%s' """ % (function_name)
        # and a.rolname = '%s', self.schema)

        self.dbi.execute(sql)

        #logger.debug(sql)
        
        row = self.dbi.fetchone()
      
        if row[0] == 1: #exists
            return True
        else:  #not exists
            return False    
        
    def function_info(self, function_name):
        """ get function information: args, return datatype, body, language """
        
        sql = """SELECT p.proname AS procedure_name,
          p.pronargs AS num_args,
          -- t1.typname AS return_type,          
          pg_catalog.pg_get_function_result(p.oid) as result_data_type,
          pg_catalog.pg_get_function_arguments(p.oid) as args_data_types,
          a.rolname AS procedure_owner,
          l.lanname AS language_type,
          p.proargtypes AS argument_types_oids,
          prosrc AS body
FROM pg_proc p
LEFT JOIN pg_type t1 ON p.prorettype=t1.oid
LEFT JOIN pg_authid a ON p.proowner=a.oid
LEFT JOIN pg_language l ON p.prolang=l.oid
    WHERE p.proname ='%s' """ % (function_name)
    
        self.dbi.execute(sql)
        
        #print(sql)
        
        rtn = self.dbi.fetchone()
        
        if not rtn:
            raise Exception("no function:%s" % (function_name))
            
        name = rtn[0]
        result_dtype = rtn[2]
        args_dtype = rtn[3]
        language = rtn[5]
        body =  rtn[7]
        
        return {"name" : name, "result_dtype" : result_dtype,  
                        "args_dtype" : args_dtype, "language" : language, "body" : body }
        
    def get_foreign_keys(self, table_name):
        """ get foreign keys """
        
        sql = """SELECT
    tc.constraint_name, tc.table_name, kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM 
    information_schema.table_constraints AS tc 
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='%s'""" % (table_name)

        self.dbi.execute(sql)
        return self.dbi.fetchall()

        
    def get_tables(self):
        """get table list by schema name"""
        
        sql = """select table_name from information_schema.tables 
                where table_catalog = '%s' 
                and table_schema = '%s' 
                and table_type = 'BASE TABLE'
                order by table_name
        """ % (self.catalog, self.schema)
        
        self.dbi.execute(sql)
        
        return self.dbi.fetchall()
        
    def drop_cs(self, table_name):
        
        sql = """SELECT table_name, constraint_name
FROM information_schema.constraint_table_usage
WHERE table_name = '%s_1'""" %(table_name)
        
        self.dbi.execute(sql)
        rows = self.dbi.fetchall()
        
        for row in rows:
            sql_alter = """ALTER TABLE %s DROP CONSTRAINT %s""" % (row[0], row[1])
            self.dbi.execute_sql(sql_alter)
            self.dbi.commit()
        
        sql_drop_seq = "DROP SEQUENCE %s_seq_seq CASCADE" % (table_name)
        self.dbi.execute_sql(sql_drop_seq)
        self.dbi.commit()
        
    def table_exists(self, table_name):
        """ check table exists """
        
        sql = """select count(1) from information_schema.tables 
                where table_name = '%s'
                and table_catalog = '%s' 
                and table_schema = '%s' 
                and table_type = 'BASE TABLE'
        """ % (table_name, self.catalog, self.schema)
        
        self.dbi.execute(sql)
        
        row = self.dbi.fetchone()
      
        if row[0] == 1: #exists
            return True
        else:  #not exists
            return False
        
    def query_table_schema(self, table_name):
        """ query table schema information """
        
        params = {"catalog":self.catalog, "schema":self.schema, "table_name":table_name}
        
        json_str = json.dumps(params)
        
        sql = """ select mtp_get_schema_cs4('%s') """ % (json_str)
        logger.debug(sql)
        
        self.dbi.execute(sql)
        
        data = self.dbi.fetchone()
        
        return data[0]["data"]
        
    def execute_sql(self, sql):
        """ execute sql """
        
        self.dbi.execute(sql)
        self.dbi.commit()
        
    @classmethod    
    def build_model(cls, table_name, cols):
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
                #continue
                pass
            
            # convert
                        
            attr = {}
            
            attr["_pos"] = col["ordinal_position"]
            
            #attr["name"] = col["column_name"]   

            if col["column_name"] == "textid":
                attr["column"] = "texths"
                attr["type"] = "hstore"
                tab["properties"].append(attr)
                continue
                
            attr["column"] = col["column_name"]            
            #attr["comment"] = col["column_name"]
            
            if col["constraint_type"] == "F":
                attr["fk"] = True
                attr["ref"] = {}
                attr["ref"]["table"] = col["co_table_name"]
                attr["ref"]["column"] = col["co_column_name"]
            elif col["constraint_type"] == "P":
                attr["pk"] = True

                
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
        
    
        
    