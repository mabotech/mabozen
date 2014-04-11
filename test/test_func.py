

import unittest

import json
import string

from lib.pg import Pg

from faker import Factory

class TestFunc(unittest.TestCase):

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
        
    def test_create_func(self):
        
        params= {"table":"func", 
            "kv":{
                "table_name":self.get_word(60),
                "type":1,
                "func_name":self.get_word(60),
                "params":"hstore('1033',self.get_word())",
                "func_body":self.fake.json(),
                "version":self.get_word(60),
                "default_ver":1            
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