

import unittest

import json
from lib.pg import Pg

from faker import Factory

class TestCompany(unittest.TestCase):

    def setUp(self):
        
        conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        
        self.dbi = Pg(conn_string)
        
        self.fake = Factory.create()
        
    def get_word(self, maxlen=100):
        
        word = self.fake.word()
        
        if len(word)>maxlen:
            return (word[:maxlen], word)
        else:
            return (word, word)

    def test_create_company(self):
        
        name = self.get_word(4)
        params= {"table":"company", 
            "kv" : { "id":"", "company": name[0], 
            "texths":name[1], "createdon":"20140408T010203.456::timestamp"}, 
            "context":{"user":self.fake.first_name(), "languageid":"1033", "sessionid":"123" } }
        
        sql = "select mtp_upsert_cf2 as result from mtp_upsert_cf2('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.dbi.execute(sql)
        rtn = self.dbi.fetchone()
        if 'error' in rtn[0]:
            self.dbi.rollback()
        else:
            self.dbi.commit()
        
        print(rtn)

    def test_update_company(self):

        params= {  "table": "company",
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

    def test_get_company(self):
        
        params= {  "table": "company",
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
    
    def test_search_company(self):        
        params= {  "table": "company",
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

    def test_delete_company(self):        
        params= {  "table": "company",
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


if __name__ == "__main__":
    
    unittest.main()