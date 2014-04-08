

import unittest

import json
import pg

class TestMtpFind(unittest.TestCase):
    
    def setUp(self):
        
        connString = "port=6432 dbname=maboss user=mabotech password=mabouser"
        
        self.db = pg.Pg(connString)
        
    def tearDown(self):
        pass
        
    def test_find_no_data(self):
        """
        [test_find] test function calling
        """
        
        params= {  "table": "company",
                        "filter": "seq > 1",
                        "cols": ["id", "seq", "createdby"],
                        "orderby": "2",
                        "offset": "0",
                        "limit": "3" ,
                        "languageid":"1033"}
        
        sql = "select mtp_find_active_cf1 as result from mtp_find_active_cf1('%s')" %(json.dumps(params) )
        
        print(  sql )
        
        self.db.execute(sql)
        
        rtn = self.db.fetchone()
        
        print(rtn)
        
        assert 'error' in rtn[0]#['error'] == 'no data'        
        
    def test_find_without_languageid(self):
        """
        [test_find] test function calling
        """
        
        params= {  "table": "company",
                        "filter": "seq > 100",
                        "cols": ["id", "seq", "createdby"],
                        "orderby": "2",
                        "offset": "0",
                        "limit": "3" }
        
        sql = "select mtp_find_active_cf1 as result from mtp_find_active_cf1('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.db.execute(sql)
        
        rtn = self.db.fetchone()
        
        #print(rtn)
        assert rtn[0]['error'] 
        assert rtn[0]['error'] == 'please provide languageid'
        
       
    def test_find_with_languageid(self):
        """
        [test_find] test function calling
        """
        
        params= {  "table": "company",
                        "filter": "seq > 100",
                        "cols": ["seq","texths", "createdby"],
                        "orderby": "2",
                        "offset": "0",
                        "limit": "3" ,
                        "languageid":"1033"
                        }
        
        sql = "select mtp_find_active_cf1 as result from mtp_find_active_cf1('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.db.execute(sql)
        
        rtn = self.db.fetchone()
        
        #print(rtn)
        
        assert rtn[0]['count'] == 3
        
        #assert 'id' in rtn[0]['result'][0]
        
        
if __name__ == '__main__':
    unittest.main()