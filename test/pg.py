# -*- coding: utf-8 -*-

import psycopg2

class Pg(object):
    
    def __init__(self, connString):

        self.conn = psycopg2.connect(connString)

        self.cur = self.conn.cursor()
       
    def execute(self, sql):
        try:
            #sql = sql.decode("utf-8", "ignore")
            self.cur.execute(sql)
        except Exception, e:
            print sql
            raise Exception(e.message)

    def commit(self):
        self.conn.commit()
    
    def fetchone(self):

        return self.cur.fetchone()

    def fetchall(self):

        return self.cur.fetchall()

    def __del___(self):
        
        self.cur.close()

        self.conn.close()
        
        
if __name__ == '__main__':
    
    connString = "port=6432 dbname=maboss user=mabotech password=mabouser"
    
    pg = Pg(connString)
    
    rtn = pg.execute("select * from mt_co_test1()")
    print pg.fetchone()[0]

