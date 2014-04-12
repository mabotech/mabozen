

import unittest

import json
import string

from mabozen.lib.pg import Pg

from mabozen.lib.testutils import get_word, get_bpchar

from faker import Factory

class TestDeploys(unittest.TestCase):

    def setUp(self):
        
        conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        
        self.dbi = Pg(conn_string)
        
        self.fake = Factory.create()
       
    def tearDown(self):
        self.dbi.close()
        
    def test_create_deploys(self):
        
        params= {"table":"deploys", 
            "kv":{
                "deployid":self.fake.random_int(),
                "sql":self.fake.text(),
                "md5":get_word(32),
                "diff":self.fake.text(),
                "datestamp":"now()"            
            },
            "context":{"user":self.fake.first_name(), "languageid":"1033", "sessionid":"123" } }
        
        sql = "select mtp_upsert_cf3 as result from mtp_upsert_cf3('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        try:
            self.dbi.execute(sql)
            rtn = self.dbi.fetchone()
            print(rtn)
            self.dbi.commit()    
        except Exception, ex:
        
            self.dbi.rollback()            
            print(ex.message)                  
    


if __name__ == "__main__":
    
    unittest.main()