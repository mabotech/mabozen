

import unittest

import json
import pg

class TestMtpUpsert(unittest.TestCase):
    
    def setUp(self):
        
        connString = "port=6432 dbname=maboss user=mabotech password=mabouser"
        
        self.db = pg.Pg(connString)
        
    def tearDown(self):
        pass
        
    def test_insert(self):
        
        params= {"table":"company", 
            "kv" : { "id":"", "company":"mabo", "texths":"mabo", "createdon":"20140408T010203.456::timestamp"}, 
            "user":"idea", "languageid":"1033", "sessionid":"123" }
        
        sql = "select mtp_upsert_cf1 as result from mtp_upsert_cf1('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.db.execute(sql)
        rtn = self.db.fetchone()
        self.db.commit()
        
        print(rtn)
        assert len(rtn[0]['result']) == 1
        
    def test_find_update_nonstr(self):       

        sql = "select rowversion from company where id = 'f17cbe96-e3f0-44cc-a477-64679fe44c5e'"
        self.db.execute(sql)
        rtn = self.db.fetchone()
        
        rv = rtn[0]
        print("=="*20)
        print(rv)
        params={"table":"company", 
            "kv" : {"id":"f17cbe96-e3f0-44cc-a477-64679fe44c5e", "company":"mabo4", "texths":"mabo4",
                "createdon":"20140408T010203.456::timestamp","rowversion":rv},   # Exception: TypeError: Exception: TypeError: Object 4 has no method 'split'
            "user":"idea", "languageid":"1033", "sessionid":"123" }
        
        sql = "select mtp_upsert_cf1 as result from mtp_upsert_cf1('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.db.execute(sql)
        rtn = self.db.fetchone()
        self.db.commit()
        
        print(rtn)
        assert len(rtn[0]['result']) == 1        
       
    def test_find_update(self):      

        sql = "select rowversion from company where id = 'f17cbe96-e3f0-44cc-a477-64679fe44c5e'"
        self.db.execute(sql)
        rtn = self.db.fetchone()
        
        rv = rtn[0]        
        
        params={"table":"company", 
            "kv" : {"id":"f17cbe96-e3f0-44cc-a477-64679fe44c5e", "company":"mabo4", "texths":"mabo4",
                "createdon":"20140408T010203.456::timestamp","rowversion": str(rv)},
            "user":"idea", "languageid":"1033", "sessionid":"123" }
        
        sql = "select mtp_upsert_cf1 as result from mtp_upsert_cf1('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.db.execute(sql)
        rtn = self.db.fetchone()
        self.db.commit()
        
        print(rtn)
        assert len(rtn[0]['result']) == 1

        
if __name__ == '__main__':
    unittest.main()