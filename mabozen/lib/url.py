
"""
copy from sqlalchemy\engine\url.py
""" 
import re
import urllib

def parse_rfc1738_args(name):
    pattern = re.compile(r'''
            (?P<name>[\w\+]+)://
            (?:
                (?P<username>[^:/]*)
                (?::(?P<password>[^/]*))?
            @)?
            (?:
                (?P<host>[^/:]*)
                (?::(?P<port>[^/]*))?
            )?
            (?:/(?P<database>.*))?
            ''', re.X)

    m = pattern.match(name)
    if m is not None:
        components = m.groupdict()
        if components['database'] is not None:
            tokens = components['database'].split('?', 2)
            components['database'] = tokens[0]
            #query = (len(tokens) > 1 and dict(util.parse_qsl(tokens[1]))) or None
            # Py2K
            #if query is not None:
            #    query = dict((k.encode('ascii'), query[k]) for k in query)
            # end Py2K
        else:
            #query = None
            pass
        #components['query'] = query

        if components['password'] is not None:
            components['password'] = \
                urllib.unquote_plus(components['password'])

        #name = components.pop('name')
        return components
    else:
        #raise exc.ArgumentError(
        #    "Could not parse rfc1738 URL from string '%s'" % name)
        raise Exception(name)
        

if __name__ == '__main__':
    url = "postgresql://mabotech:mabouser@localhost:6432/maboss?encode=utf8"
    print parse_rfc1738_args(url)
    