

import unittest

import json
import pg

class TestCommonFunction(unittest.TestCase):
    """
    Common Postgresql Function for all tables
    """
    def setUp(self):
        
        connString = "port=6432 dbname=maboss user=mabotech password=mabouser"
        
        self.db = pg.Pg(connString)
        
    def tearDown(self):
        pass
        
    def test_create(self):
        """
        test create
        """
        
    def test_update(self):
        """
        test update
        """
        
    def test_delete(self):
        """
        test delete
        """
    
    def test_get(self):
        """
        test get one by id
        """
        
    def test_find(self):
        """
        [test_find] test function calling
        """
        
        params= {  "table": "company",
                        "filter": "seq < 100",
                        "cols": ["id", "seq", "createdby"],
                        "orderby": "2",
                        "offset": "0",
                        "limit": "3" }
        
        sql = "select find_cf1 as result from find_cf1('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.db.execute(sql)
        
        rtn = self.db.fetchone()
        
        assert rtn[0]['count'] == 3
        
        assert 'id' in rtn[0]['result'][0]
        

if __name__ == '__main__':
    unittest.main()