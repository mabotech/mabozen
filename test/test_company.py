

import unittest

import json
import string

from mabozen.lib.pg import Pg

from mabozen.lib.testutils import get_word, get_bpchar

from faker import Factory

class TestCompany(unittest.TestCase):

    def setUp(self):
        
        conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        
        self.dbi = Pg(conn_string)
        
        self.fake = Factory.create()
       
    def tearDown(self):
        self.dbi.close()
        
    def test_create_company(self):
        
        params= {"table":"company", 
            "kv":{
                "company":get_word(4),
                "texths":"hstore('1033',get_word())",
                "currencycode":get_word(3),
                "codesystemtype":get_word(10),
                "formattype":get_word(10),
                "domainmanagerid":self.fake.random_int(),
                "objectclass":get_word(40)            
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