

import unittest

import json

from mabozen.lib.pg import Pg

class TestGetSchema2(unittest.TestCase):
    
    def setUp(self):
        
        conn_string = "port=6432 dbname=maboss user=mabotech password=mabouser"
        
        self.db = Pg(conn_string)
        
    def tearDown(self):
        pass
        
    def test_call_func(self):
        """
        [test_find] test function calling
        """
        
        params={"catalog":"maboss", "schema":"mabotech","table_name":"company"}
        
        sql = "select get_schema2 as result from get_schema2('%s')" %(json.dumps(params) )
        
        #print(  sql )
        
        self.db.execute(sql)
        
        rtn = self.db.fetchone()
        
        json_str = json.dumps(rtn[0], sort_keys=True, indent=4, separators=(',', ': '))
        
        #print(json_str)
        
        assert "data" in rtn[0]
        
        
if __name__ == '__main__':
    unittest.main()