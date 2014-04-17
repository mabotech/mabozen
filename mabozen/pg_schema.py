# -*- coding: utf-8 -*-


"""
PostgreSQL Schema infomation
"""

from mabozen.lib.pg import Pg


class PgSchema(object):
    """ class """
    
    def __init__(self):
        """  init db connection """
        
        conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        self.dbi = Pg(conn_string)
        
        
    def function_exists(self, function_name):
        """ check function exists """
        
    def function_info(self, function_name):
        """ get function information: args, return datatype, body, language """
        
    def table_exists(self, table_name):
        """ check table exists """
        
    def query_table_schema(self):
        """ query table schema information """
        
    