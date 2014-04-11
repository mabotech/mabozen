

import unittest

import json
import string

from lib.pg import Pg

from faker import Factory

class Test{{class_name}}(unittest.TestCase):

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
        
    def test_create_{{table}}(self):
        
        params= {"table":"{{table}}", 
            "kv":{
                {{attrs}}            
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
    {#
    def test_update_{{table}}(self):

        params= {  "table": "{{table}}",
                        "filter": "active = 1",
                        "cols": ["id", "seq", "createdby"],
                        "orderby": "2",
                        "offset": "0",
                        "limit": "3" }
        
        sql = "select mtp_find_cf1 as result from mtp_find_cf1('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.dbi.execute(sql)
        
        rtn = self.dbi.fetchone()

        print(rtn)

    def test_get_{{table}}(self):
        
        params= {  "table": "{{table}}",
                        "filter": "active = 1",
                        "cols": ["id", "seq", "createdby"],
                        "orderby": "2",
                        "offset": "0",
                        "limit": "3" }
        
        sql = "select mtp_find_cf1 as result from mtp_find_cf1('%s')" % (json.dumps(params) )
        
        #print(  sql )
        
        self.dbi.execute(sql)
        
        rtn = self.dbi.fetchone()

        print(rtn)
    
    def test_search_{{table}}(self):        
        params= {  "table": "{{table}}",
                        "filter": "active = 1",
                        "cols": ["id", "seq", "createdby"],
                        "orderby": "2",
                        "offset": "0",
                        "limit": "3" }
        
        sql = "select mtp_find_cf1 as result from mtp_find_cf1('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.dbi.execute(sql)
        
        rtn = self.dbi.fetchone()

        print(rtn)

    def test_delete_{{table}}(self):        
        params= {  "table": "{{table}}",
                        "filter": "active = 1",
                        "cols": ["id", "seq", "createdby"],
                        "orderby": "2",
                        "offset": "0",
                        "limit": "3" }
        
        sql = "select mtp_find_cf1 as result from mtp_find_cf1('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.dbi.execute(sql)
        
        rtn = self.dbi.fetchone()

        print(rtn)
    #}


if __name__ == "__main__":
    
    unittest.main()