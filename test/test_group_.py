

import unittest

import json
import string

from lib.pg import Pg

from faker import Factory

class TestGroup(unittest.TestCase):

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
        
    def test_create_group_(self):
        
        params= {"table":"group_", 
            "kv":{
                "group_":self.get_word(40),
                "grouptype":self.get_word(10),
                "groupclassid":self.fake.random_int(),
                "parentgroup":self.get_word(40),
                "parentgrouptype":self.get_word(10),
                "parentgroupclassid":self.fake.random_int(),
                "texths":"hstore('1033',self.get_word())",
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