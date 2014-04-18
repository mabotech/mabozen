# -*- coding: utf-8 -*-

"""
mabozen configuration
"""

import os

from flask.config import Config

from mabozen.lib.singleton import Singleton
from mabozen.lib.logging_factory import get_logger

HERE = os.path.dirname(os.path.abspath(__file__) )

class ZenConfig(object):
    """
    singleton
    """
    __metaclass__ = Singleton
        
    def __init__(self):
        pass
        
    def get_db_params(self):
        """ return db params """
        pass
        
    def get_logger(self):
        """ return logger """
        pass
        
    def get_template_path(self):
        """ return template base path """
        pass
        
        
def get_db_config():
    """
    get db config string
    """
    mabozen_config_file = os.sep.join([HERE, 'conf','mabozen_config.py'])

    zen_cfg = Config('')

    zen_cfg.from_pyfile(mabozen_config_file)
    
    return zen_cfg
    

def logging(app_name):
    """
    init logger and return
    """
    #APP = "mabozen"

    logging_config_file = os.sep.join([HERE, 'conf','logging_config.py'])

    log_cfg = Config('')

    log_cfg.from_pyfile(logging_config_file)
    
    logger = get_logger(app_name, '..\\logs', log_cfg['LOGGING']) 
    
    return logger
    
def test():
    """ test function"""
    db_cfg = get_db_config()
    print db_cfg['PORT']
    print db_cfg['PASSWORD']
    print db_cfg['DATABASE']
    print db_cfg['USERNAME']
    
if __name__ == '__main__':
    test()