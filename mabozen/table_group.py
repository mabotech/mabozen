# -*- coding: utf-8 -*-

"""
group menu in data administration
to be loaded in config.py?
"""

import json

class TableGroup(object):
    """menu group"""
    
    def __init__(self, filename):
        """ load group from json file """
        
        # menu / output path
        self.groups = {}
        
        # url /path
        self.table_groups = {}
        
        with open(filename, 'r') as fileh:
            self.groups = json.loads(fileh.read())
        
        self._reverse()
        #print json.dumps(self.groups, sort_keys=True, \
        #indent=4, separators=(',', ': '))
        
    def read(self):
        """ read json file? """
        pass
        
    def _reverse(self):
        """ reverse table - group """
        for key in self.groups:
            #print(key)
            for item in self.groups[key]:
                #print item
                if item in self.table_groups:
                    
                    msg = "%s in %s,%s" % (item, key, self.table_groups[item] )
                    raise Exception(msg)
                    
                else:
                    self.table_groups[item] = key
        
        #print self.table_group
        print json.dumps(self.table_groups, sort_keys=True, \
                indent=4, separators=(',', ': '))
        
if __name__ == '__main__':
    tableg = TableGroup()
    tableg.reverse()