

import pg

import json

import time

def test_plv8(db, jsonstr):
    
    sql = "select mt_user_c_cf8 from mt_user_c_cf8('%s')" %(jsonstr)
    db.execute(sql)
    db.commit()    

    
def test_pgsql(db, jsonstr):
    
    sql = "select user_add_pg2 from user_add_pg2('%s')" %(jsonstr)
    db.execute(sql)
    db.commit()    
    
    
def bm(db, n):
    

    
    start = time.time()
    
    for i in range(n):
        
        name = "name%s"%(i)
        user = "plv8_%s"%(i)
        
        obj = {"name": name, "user":user}
        
        jsonstr =  json.dumps(obj)
        
        test_plv8(db, jsonstr)
        
    print "plv8[%s]: %d ms" % (i+1, 1000*(time.time() -start))


    start = time.time()
    
    for i in range(n):
        
        name = "name%s"%(i)
        user = "pgsql_%s"%(i)
        
        obj = {"name": name, "user":user}
        
        jsonstr =  json.dumps(obj)
        
        test_pgsql(db, jsonstr)
    #db.commit()
    print "pgsql[%s]: %d ms" % (i+1, 1000*(time.time() -start))
    print "=="*10

if __name__ == "__main__":
    

    connString = "port=6432 dbname=maboss user=mabotech password=mabouser"
    db = pg.Pg(connString)    
    n = 20
    
    bm(db, n)
    bm(db, n)
    bm(db, n)
    bm(db, n)
    bm(db, n)
    bm(db, n)