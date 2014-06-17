

from lxml import etree

class Singleton(type):
  def __call__(cls, *args):
    if not hasattr(cls, 'instance'):
      cls.instance = super(Singleton, cls).__call__(*args)
    return cls.instance


class Counter(object):
    
    __metaclass__ = Singleton
    
    def __init__(self):
        self.i = 0
        
    def inc(self):
        self.i =  self.i + 1
        return self.i



def dbdt_insert(dbdt_dict):
        
        
        sql = """insert into mt_t_db_datatype( id, fk_datatype,fk_db,name,alias,shortname,identity,Undefined,scale,width,showscale,showtype,showwidth,ordering,active,createdon,createdby,rowversionstamp)
  values (%(id)s, %(fk_datatype)s, %(fk_db)s, '%(name)s', '%(alias)s', '%(shortname)s', '%(identity)s', %(undefined)s, %(scale)s, %(width)s, %(showscale)s, %(showtype)s, %(showwidth)s, %(ordering)s,1, now(), 'MT', 1 );\n""" % dbdt_dict
        return sql
      
def db_insert(vt):
    sql = """ insert into mt_t_db_platform(id,name,ordering,active,createdon,createdby,rowversionstamp)
  values ( %s,  '%s', %s, 1,  now(),  'MT',  1);\n """ % vt
    return sql
    
def dt_insert(vd):
    print "dt_insert", vd['name']
    sql =""" insert into mt_t_datatype(id,name, alias, shortname, ordering,active,createdon,createdby,rowversionstamp)
  values ( %(fk_datatype)s,  '%(name)s',  '%(name)s',   '%(shortname)s', %(ordering)s,  1, now(),  'MT', 1 ) ;\n""" % vd
    return sql

def convert(val):
    if val == 'false':
        return 0
    elif val == 'true':
        return 1
    else:
        raise Exception('val not false or true')
       
def dt_extract(pid, node):
    i = 0
    sql = ""

    for dt in node.xpath('DataType'):
        i = i + 1
        dt_dict = {}
        dt_dict['ordering'] = i
        dt_dict['fk_db'] = pid
        dt_dict['fk_datatype'] =  dt.xpath('@DatatypeId')[0]
        dt_dict['name'] =  dt.xpath('@DatatypeName')[0]
        dt_dict['alias'] =  dt.xpath('@DatatypeName')[0]
        dt_dict['identity'] =  dt.xpath('@Identity')[0]
        dt_dict['scale'] =  dt.xpath('@Scale')[0]
        dt_dict['shortname'] =  dt.xpath('@ShortName')[0]
        dt_dict['showscale'] =  convert ( dt.xpath('@ShowScale')[0] )
        dt_dict['showtype'] =  convert ( dt.xpath('@ShowType')[0] )
        dt_dict['showwidth'] = convert ( dt.xpath('@ShowWidth')[0] )
        dt_dict['undefined'] =   convert( dt.xpath('@Undefined')[0] )
        dt_dict['width'] =  dt.xpath('@Width')[0]
        

        sql = sql + dt_insert(dt_dict)

    return sql        
            
def extract(pid, node):
    i = 0
    sql = ""
    ct = Counter()
    for dt in node.xpath('DataType'):
        i = i + 1
        dt_dict = {}
        dt_dict['ordering'] = i
        dt_dict['fk_db'] = pid
        dt_dict['id'] = ct.inc()
        dt_dict['fk_datatype'] =  dt.xpath('@DatatypeId')[0]
        dt_dict['name'] =  dt.xpath('@DatatypeName')[0]
        dt_dict['alias'] =  dt.xpath('@DatatypeName')[0]
        dt_dict['identity'] =  dt.xpath('@Identity')[0]
        dt_dict['scale'] =  dt.xpath('@Scale')[0]
        dt_dict['shortname'] =  dt.xpath('@ShortName')[0]
        dt_dict['showscale'] =  convert ( dt.xpath('@ShowScale')[0] )
        dt_dict['showtype'] =  convert ( dt.xpath('@ShowType')[0] )
        dt_dict['showwidth'] = convert ( dt.xpath('@ShowWidth')[0] )
        dt_dict['undefined'] =   convert( dt.xpath('@Undefined')[0] )
        dt_dict['width'] =  dt.xpath('@Width')[0]        

        sql = sql +  dbdt_insert(dt_dict)
    return sql
  
def main():    

    sqlfile = "../../../output/mapping/dt03.sql"
    
    fh = open(sqlfile, 'w')
    
    fn = "DatatypeMappings_SystemDefault.xml"
    tree = etree.parse(fn)

    DBPlatform = tree.xpath('/DataTypeMapping/DBPlatform')
    
    ordering = 0
    for node in DBPlatform:
        ordering = ordering + 1
        #print node.xpath('@MappingName')
        pid = node.xpath('@PlatformId')
        
        pname = node.xpath('@MappingName')
        
        print(pname)
        
        vt = (pid[0], pname[0], ordering)
        
        sql = db_insert(vt)
        #fh.write(sql)
        
        
        if pid == ['0']:
            print "Logical (system)"
            #sql = dt_extract(pid[0], node)
            #fh.write(sql)
        if pname[0] == "PostgreSQL 8.0 (system)":
            sql = extract(pid[0], node)
            fh.write(sql)

    fh.close()

if __name__ == '__main__':
    main()