# -*- coding: utf-8 -*-


class SchemaFactory(object):
    
    def __init__(self, port, dbname, username, password):
        self.port = port
        self.dbname = dbname
        self.username = username
        self.password = password        
    
    def get_schema(self, dbtype="pg"):
        
        if dbtype == 'ora':
            return Exception("ora not implemented yes")
        else:
            from mabozen.pg.pg_schema import PgSchema
            return PgSchema(self.port, self.dbname, self.username, self.password)
            
        