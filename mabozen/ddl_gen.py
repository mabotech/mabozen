# -*- coding: utf-8 -*-

"""

"""

import glob

import re

import lib.pg

class DDL(object):
    
    def __init__(self):
        """
        init db
        """
        
        conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        
        self.dbi = pg.Pg(conn_string)

 