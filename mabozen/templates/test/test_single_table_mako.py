

import unittest

import json
import string

from mabozen.lib.pg import Pg

from mabozen.lib.testutils import get_word, get_bpchar

from faker import Factory

class Test${class_name}(unittest.TestCase):

    def setUp(self):
        
        conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        
        self.dbi = Pg(conn_string)
        
        self.fake = Factory.create()

        sql = "select id, rowversion from ${table} where active = 1 order by seq  offset 0 limit 2"

        self.dbi.execute(sql)

        rtn = self.dbi.fetchall()
        
        if len(rtn)<1:
            self.${table}_id = None
            self.rowversion = 1
            #raise Exception("no enough data")
        else:
            self.${table}_id = rtn[0][0]
            #self.${table}_id2 = rtn[1][0]
            self.rowversion = rtn[0][1]
       
    def tearDown(self):
        self.dbi.close()
        
    def test_create_${table}(self):
        
        params= {"table":"${table}", 
            "columns":{
                ${attrs}            
            },
            "context":{"user":self.fake.first_name(), "languageid":"1033", "sessionid":"123" } }
        
        sql = "select mtp_upsert_cf4 as result from mtp_upsert_cf4('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        
        self.dbi.execute(sql)
        rtn = self.dbi.fetchone()

        assert 'id' in rtn[0]['result'][0]
    
    def test_create_${table}2(self):
        
        params= {"table":"${table}", 
            "columns":{
                ${attrs}            
            },
            "context":{"user":self.fake.first_name(), "languageid":"1033", "sessionid":"123" } }
        
        sql = "select mtp_upsert_cf4 as result from mtp_upsert_cf4('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.dbi.execute(sql)
        rtn = self.dbi.fetchone()
        #print(rtn)
        self.dbi.commit()    

        assert 'id' in rtn[0]['result'][0]
 
    def test_find(self):
        """
        [test_find] test function calling
        """
        
        params= {  "table": "${table}",
                        "languageid":"1033",
                        "filter": "active = 1",
                        "cols": ["id", "seq", "createdby"],
                        "orderby": "2",
                        "offset": "0",
                        "limit": "3" }
        
        sql = "select mtp_find_cf1 as result from mtp_find_cf1('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.dbi.execute(sql)
        
        rtn = self.dbi.fetchone()
        
        assert "count" in rtn[0]
        
        assert 'id' in rtn[0]['result'][0]

    #mtp_find_active_cf1
        
    def test_find_active(self):
        """
        [test_find] test function calling
        """
        
        params= {  "table": "${table}",
                       "languageid":"1033",
                        "filter": "active = 1",
                        "cols": ["id", "seq", "createdby"],
                        "orderby": "2",
                        "offset": "0",
                        "limit": "3" }
        
        sql = "select mtp_find_active_cf1 as result from mtp_find_active_cf1('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.dbi.execute(sql)
        
        rtn = self.dbi.fetchone()
        
        assert "count" in rtn[0]
        
        assert 'id' in rtn[0]['result'][0]

    def test_get(self):
        """
        [test_find] test function calling
        """
        params= {  "table": "${table}",
                        "id": self.${table}_id,
                        "languageid": "1033"
                }
        
        sql = "select mtp_get_cf1 as result from mtp_get_cf1('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.dbi.execute(sql)
        
        rtn = self.dbi.fetchone()
        
        #print(rtn)
        assert "id" in rtn[0]["result"][0]
        assert  self.${table}_id ==rtn[0]["result"][0]["id"]
        #assert 'id' in rtn[0]['result'][0]


    def test_update_${table}(self):
            
            if self.${table}_id == None:
                raise(Exception("no data"))

            params= {"table":"${table}", 
                "columns":{
                    ${attrs},
                    "id":self.${table}_id,
                    "rowversion":self.rowversion

                },
                "context":{"user":self.fake.first_name(), "languageid":"1033", "sessionid":"123" } }
            
            json_str = json.dumps(params).replace("'","''")
            sql = "select mtp_upsert_cf4 as result from mtp_upsert_cf4('%s')" %(json_str)
            
            #print(  sql )
            
            self.dbi.execute(sql)
            rtn = self.dbi.fetchone()
            
            #print(rtn)
            self.dbi.commit()    

            assert rtn[0]["result"][0]["id"] == self.${table}_id

if __name__ == "__main__":
    
    unittest.main(verbosity=3)