

import unittest

import json
import string

from lib.pg import Pg

from faker import Factory

class TestGenealogy(unittest.TestCase):

    def setUp(self):
        
        conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        
        self.dbi = Pg(conn_string)
        
        self.fake = Factory.create()
       
    def tearDown(self):
        self.dbi.close()
        
    def get_word(self, maxlen=100):
        
        word = self.fake.word()
        
        if len(word)>maxlen:
            return word[:maxlen]
        else:
            return word

    def get_bpchar(self, maxlen):
        
        word = self.fake.word()
        
        if len(word)>maxlen:
            return word[:maxlen]
        else:
            s = string.ljust(word,maxlen)
            print s
            return s
        
    def test_create_genealogy(self):
        
        params= {"table":"genealogy", 
            "kv":{
                "parentproductid":self.fake.random_int(),
                "parentgradeid":self.fake.random_int(),
                "parentlotno":self.get_word(40),
                "parentserialno":self.get_word(40),
                "productid":self.fake.random_int(),
                "productgradeid":self.fake.random_int(),
                "lotno":self.get_word(40),
                "serialno":self.get_word(40),
                "quantity":self.get_word(10),
                "uomcode":self.get_word(10),
                "ecoid":self.fake.random_int(),
                "workcenter":self.get_word(40),
                "reasoncode":self.get_word(20),
                "cost":self.get_word(10),
                "unitid":self.fake.random_int()            
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