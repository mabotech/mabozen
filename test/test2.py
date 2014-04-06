

import json

import pg


def test_find():  

    connString = "port=6432 dbname=maboss user=mabotech password=mabouser"
    
    db = pg.Pg(connString)
    
    params= {
                    "table": "company",
                    "filter": "seq < 100",
                    "cols": ["id", "seq", "createdby"],
                    "orderby": "2",
                    "offset": "0",
                    "limit": "3"
                }
    
    sql = "select find_cf1 as result from find_cf1('%s')" %(json.dumps(params) )
    
    #print(  sql )
    
    db.execute(sql)
    
    rtn = db.fetchone()
    
    assert rtn[0]['count'] == 3
    
    assert 'id' in rtn[0]['result'][0]
