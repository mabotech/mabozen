# -*- coding: utf-8 -*-

""" PostgreSQL proxy class """

import psycopg2

from mabozen.lib.url import parse_rfc1738_args

def parse_url(db_url):
    """parse url"""
    components = parse_rfc1738_args(db_url)
    
    return components

class Pg(object):
    """ PostgreSQL proxy """
    def __init__(self, components):
        """
        initialize
        libpg: http://www.postgresql.org/docs/current/static/libpq-connect.html
        """
        
        #components = parse_url(db_url)
        
        host = components["host"]
        port = components["port"]
        database = components["database"]

        username = components["username"]
        password = components["password"]
        
        self.conn = psycopg2.connect(database=database, user = username, \
            password = password, host = host, port = port)

        self.cur = self.conn.cursor()
       
    def execute(self, sql):
        """ execute with exception handling """
        try:
            #sql = sql.decode("utf-8", "ignore")
            self.cur.execute(sql)
        except Exception, e:
            print sql
            raise Exception(e.message)

    def commit(self):
        """commit"""
        self.conn.commit()

    def rollback(self):
        """rollback"""
        self.conn.rollback()
    
    def fetchone(self):
        """fetchone"""
        return self.cur.fetchone()

    def fetchall(self):
        """fetchall"""
        return self.cur.fetchall()

    def close(self):  
        """ close connection manually """
        self.cur.close()
        self.conn.close()
        self.closed = True
        
    def __del___(self):
        """ close connection when   obj destoried """
        if not self.closed:
            
            self.cur.close()
            
            self.conn.close()
        
        
if __name__ == '__main__':
    
    conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
    
    pg = Pg(conn_string)
    
    rtn = pg.execute("select * from mt_co_test1()")
    print pg.fetchone()[0]

