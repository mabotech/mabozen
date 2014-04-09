
from nose.tools import with_setup

import json

import pg

db = None

def setup_func():
    connString = "port=6432 dbname=maboss user=mabotech password=mabouser"
        
    global db 
    
    db = pg.Pg(connString)

def teardown_func():
    pass

@with_setup(setup_func, teardown_func)
def test_find():  
    
    params= {  "table": "company",
                    "filter": "seq > 100",
                    "cols": ["id", "seq", "createdby"],
                    "orderby": "2",
                    "offset": "0",
                    "limit": "3" }
    
    sql = "select mtp_find_cf1 as result from mtp_find_cf1('%s')" %(json.dumps(params) )
    
    print(  sql )
    
    db.execute(sql)
    
    rtn = db.fetchone()
    
    print(rtn)
    
    assert rtn[0]['count'] == 3
    
    assert 'id' in rtn[0]['result'][0]
