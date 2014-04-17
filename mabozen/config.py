



from flask.config import Config

from mabozen.lib.logging_factory import get_logger

from mabozen.lib.singleton import Singleton

class ZenConfig(object):
    
    __metaclass__ = Singleton
        
    def __init__(self):
        pass
        
def get_db_config():
    MABOZEN_CONFIG_FILE = 'conf/mabozen_config.py'

    ZEN_CFG = Config('')

    ZEN_CFG.from_pyfile(MABOZEN_CONFIG_FILE)
    
    return ZEN_CFG
    

def logging(APP):
    #APP = "mabozen"

    LOGGING_CONFIG_FILE = 'conf/logging_config.py'

    LOG_CFG = Config('')

    LOG_CFG.from_pyfile(LOGGING_CONFIG_FILE)
    
    #lf = LoggingFactory()

    logger = get_logger(APP, '..\\logs', LOG_CFG['LOGGING']) 
    
    return logger
    
if __name__ == '__main__':
    
    a = get_db_config()
    print a['PORT']
    print a['PASSWORD']
    print a['DATABASE']
    print a['USERNAME']