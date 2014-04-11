

import unittest

import json
import string

from lib.pg import Pg

from faker import Factory

class TestGenealogyDetail(unittest.TestCase):

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
        
    def test_create_genealogy_detail(self):
        
        params= {"table":"genealogy_detail", 
            "kv":{
                "genealogyid":self.fake.random_int(),
                "reasoncode":self.get_word(20),
                "quantity":self.get_word(10),
                "uomcode":self.get_word(20),
                "cost":self.get_word(10),
                "wiporderno":self.get_word(40),
                "wipordertype":self.fake.random_int(),
                "oprsequenceno":self.get_word(20),
                "stepsequenceno":self.get_word(10),
                "workcenter":self.get_word(40),
                "originalwiporderno":self.get_word(40),
                "originalwipordertype":self.fake.random_int(),
                "originaloprsequenceno":self.get_word(20)            
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