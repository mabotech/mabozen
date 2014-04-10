

import unittest

import json

from mabozen import table


class TestFind(unittest.TestCase):
    
        
    def test_re_table(self):
        
        line = """
        -- Table site
CREATE TABLE site
(
        """
        
        table_name = table.get_tablename(line)
        
        assert table_name == "site"
        
        
        line = """-- 
-- TABLE: "ADDRESS" 
--

CREATE TABLE "ADDRESS"(
    "ID"                    serial,
    "ADDRESSTYPECODE"       varchar(60),
        """
        
        line = line.replace('"','')
        
        table_name = table.get_tablename(line)
        
        print(table_name)
        
        assert table_name == "ADDRESS"
        

if __name__ == '__main__':
    unittest.main()