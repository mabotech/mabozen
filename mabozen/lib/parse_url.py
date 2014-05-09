

from mabozen.lib.url import parse_rfc1738_args

def parse_url(db_url):
    """parse url"""
    components = parse_rfc1738_args(db_url)
    
    return components