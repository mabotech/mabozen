# -*- coding: utf-8 -*-

"""factory for database manipulate objects"""

from mabozen.lib.url import parse_rfc1738_args

class ZenFactory(object):
    """factory class"""
    
    def __init__(self, db_url):
        """
        factory initialize, 
        """
        
        self.components = parse_rfc1738_args(db_url)

        self.dbtype = self.components["name"]
    
    def get_schema(self):
        """db schema extractor"""
        
        if self.dbtype == 'oracle':
            return Exception("ora not implemented yes")
        else:
            from mabozen.pg.pg_schema import PgSchema
            return PgSchema(self.components)
            
    def get_backup(self):
        """db objects backup"""
        
        if self.dbtype == 'oracle':
            return None
        else:
            pass
            
    def get_deployer(self):
        """db objects deployer"""
        
        if self.dbtype == 'oracle':
            return None
        else:
            pass
            
    def get_ddl_gen(self):
        """stored procedure generator"""
        
        if self.dbtype == 'oracle':
            return None
        else:
            pass 

    def get_create_table(self):
        "merge with ddl gen? "
        
        if self.dbtype == 'oracle':
            return None
        else:
            pass