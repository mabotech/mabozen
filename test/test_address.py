

import unittest

import json
import string

from mabozen.lib.pg import Pg

from mabozen.lib.testutils import get_word, get_bpchar

from faker import Factory

class TestAddress(unittest.TestCase):

    def setUp(self):
        
        conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        
        self.dbi = Pg(conn_string)
        
        self.fake = Factory.create()
       
    def tearDown(self):
        self.dbi.close()
        
    def test_create_address(self):
        
        params= {"table":"address", 
            "kv":{
                "addresstypecode":get_word(60),
                "agency":get_word(80),
                "geographiclocationid":self.fake.random_int(),
                "externaladdressid":get_word(50),
                "pobox":get_word(16),
                "housenumber":get_word(8),
                "floor":get_word(8),
                "roomnumber":get_word(8),
                "inhousemail":get_word(8),
                "postalcode":get_word(20),
                "regioncode":get_word(10),
                "countrycode":get_word(3),
                "timezoneid":self.fake.random_int(),
                "calendarsystemtypeid":self.fake.random_int(),
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