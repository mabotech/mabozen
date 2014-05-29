# -*- coding: utf-8 -*-

"""
drawing ERD(table relationships) by graphviz dot
"""
import os
import re
import json

from time import strftime, localtime

import logging

import subprocess
from mako.template import Template
from random import randint

from mabozen.config import get_db_config
from mabozen.lib.pg import parse_url
from mabozen.lib.pg import Pg

LOGGER = logging.getLogger("tools")

COLORS = ['darkgreen', 'red', 'navy', 'green', 'yellow', 'blue',
    'violet', 'darksalmon', 'black', 'orangered', 'cyan', 'darkorange',
    'yellowgreen', 'black']
    
class RelationMap(object):
    """ class for query PostgreSQL schema information"""

    def __init__(self, table_list, rtype, etype):
        """  init """
        
        if rtype not in ['c','p']:
            raise
            
        self.rtype = rtype
        
        if etype not in [1, 2, 3]:
            raise
            
        self.etype = etype
        
        self.table_list = table_list
          
        self.max_level = 10
        
        cfg = get_db_config()
        
        url = cfg['DB_URL']
        
        #catalog == dbname
        #schema == username
        components = parse_url(url)
        
        self.catalog = components["database"]        
        self.schema = components["username"]     
        
        self.dbi = Pg(components)
        
        self.edges = []        
   
        self.nodes_single = set()        
        self.tables = set()        
        self.edge_list = set()
    
    @classmethod
    def get_keys(cls, line):
        """ match foreign key """
        
        rawstr = r"""FOREIGN KEY \((.*)\) REFERENCES (.*)\((.*)\)"""
    
        compile_obj = re.compile(rawstr)        

        match_obj = compile_obj.search(line)

        fkey = match_obj.group(1)
        tab = match_obj.group(2)
        pkey = match_obj.group(3)

        return(fkey, tab, pkey)
        
    def dot(self):
        """ graphviz dot """
        dot_template = Template(filename="graphviz_mako.dot",   \
                    disable_unicode=True, input_encoding='utf-8')
        
        dotstr =  dot_template.render(nodes = self.nodes_single, \
                                        edges = self.edges)            
        #print(dotstr)
        
        #here = os.path.dirname(os.path.abspath(__file__) )
        stamp = (strftime("%Y%m%d%H%M%S", localtime()))
        
        dot_file = os.sep.join(["..\\..\\working", "graph", \
                                "maboss%s_%s.dot" % (self.etype, stamp)])
        with open(dot_file,'w') as fileh:
            fileh.write(dotstr.replace("\r\n","\n"))
            
        out_file = os.sep.join(["..\\..\\working", "graph", \
                            "maboss%s_%s.svg" %(self.etype, stamp)]) 
        cmd = r'''C:\Tools\Graphviz2.30\bin\dot -Tsvg -o %s %s''' \
                    % (out_file, dot_file   )
        #print (cmd)
        subprocess.Popen(cmd, shell=True)      
    
    def _make_edge(self, rel):
        """ edge defination """
        
        color = COLORS[randint(0, len(COLORS)-1)]
        
        if self.etype == 1:
        
            edge = """%s -> %s [label="%s", color="%s"]""" \
                % (rel["ctable"], rel["ptable"], \
                self.get_keys(rel["ppkey"])[2] , color)
        
        elif self.etype == 2:
            edge = """%s -> %s [label="%s"]""" % (rel["ctable"], \
                rel["ptable"], self.get_keys(rel["ppkey"])[2] )
            
        elif self.etype == 3:
            
            edge = """%s -> %s[color="%s"]""" \
                % (rel["ctable"], rel["ptable"], color)
        else:
            raise
            
        return edge
        
    def one(self, table_name, level):
        """ relationships of one table"""
        if len(self.table_list) != 0:
            if table_name not in self.table_list:
                return
        
        if table_name in self.tables:
            return
        else:
            self.tables.add(table_name)
            
        if level > self.max_level:
            return
        
        i_json = {"schema":self.schema, "table_name":table_name, "type":"p"}
        
        func_map = {'c':"mtp_get_ctable_pg1", 'p':"mtp_get_ptable_pg2"}

        self.dbi.execute("select * from %s ('%s')" \
                        % (func_map[self.rtype], json.dumps(i_json)))
        
        result = self.dbi.fetchone()
        
        #print(json.dumps(result[0], sort_keys=True, 
        #indent=2, separators=(',', ': ')) )
    
        if result[0] == None:
            self.nodes_single.add(table_name)
            return
        
        comment = "\n/* %s [%d] */" % (table_name, len(result[0]))
        self.edges.append(comment)
        
        for rel in result[0]:
            
            if len(self.table_list) != 0:
                if rel["ptable"] not in self.table_list:
                    continue
            
            edge = self._make_edge(rel)
            
            edge_s = """%s -> %s""" % (rel["ctable"], rel["ptable"])
            
            if edge_s in self.edge_list:
                continue
            else:
                self.edge_list.add(edge_s)
                self.edges.append(edge)   

            #print(rel["ctable"])
            self.one(rel["ctable"], level+1)
    
    def prepare_all(self):
        """ prepare all relatonships  """
        
        sql = """select table_name from information_schema.tables 
                where table_catalog = '%s' 
                and table_schema = '%s' 
                and table_type = 'BASE TABLE'
                order by table_name
        """ % (self.catalog, self.schema)
        
        self.dbi.execute(sql)
        
        tabs = self.dbi.fetchall()
        
        for tab in tabs:
            #print(tab[0])           
            self.one(tab[0], 1)        
    
    def prepare_root(self, table_name, max_level):
        """ fetch children """
        self.max_level = max_level
        self.one(table_name, 1)

        
def process(table_list):
    """ main """
    
    rmap = RelationMap(table_list, 'p', 3)
    
    table_name =  None#"wip_order"
    
    rmap.prepare_all()
    
    max_level = 3
    
    rmap.prepare_root(table_name, max_level)
    
    rmap.dot()
    
def main():
    """ main """
    with open("relation_group.json",'r') as fileh:
        groups = json.loads(fileh.read())
        
    for table_group in groups:
        print table_group["tables"]
        
        process(table_group["tables"])
    
if __name__ == '__main__':
    main()
    