# -*- coding: utf-8 -*-


"""
PostgreSQL Schema infomation
"""

import logging

import json

from mabozen.lib.pg import Pg

logger = logging.getLogger("schema")

class PgSchema(object):
    """ class postgresql schema"""

    def __init__(self, port, dbname, username, password):
        """  init db connection """
                
        logger.debug("init PgSchema")
        
        #catalog == dbname
        #schema == username
        
        self.catalog = dbname # "maboss"
        
        self.schema = username #"mabotech"
        
        conn_string = "port=%s dbname=%s user=%s password=%s" % (port, dbname, username, password)
        
        self.dbi = Pg(conn_string)

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
        
        sql = """ select mtp_get_schema('%s') """ % (json_str)
        logger.debug(sql)
        self.dbi.execute(sql)
        
        data = self.dbi.fetchone()
        
        return data        
        
    def execute_sql(self, sql):
        """ execute sql """
        
        self.dbi.execute(sql)
        self.dbi.commit()
        
        
    
        
    