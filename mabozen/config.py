# -*- coding: utf-8 -*-

"""
mabozen configuration
"""

import os

from flask.config import Config

from mabozen.table_group import TableGroup

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


def get_app_config():
    """
    get app config string
    """
    mabozen_config_file = os.sep.join([HERE, 'conf','mabozen_config.py'])

    zen_cfg = Config('')

    zen_cfg.from_pyfile(mabozen_config_file)
    
    model_file = "../models/table_groups.json"
    
    tgroup = TableGroup(model_file)
    
    #tgroup.groups
    #tgroup.table_groups
    zen_cfg["TABLE_GROUP"] = tgroup
    
    return zen_cfg        
        
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
    
    #modified on 2014-04-29 16:18:40
    #log_root = '..\\logs'
    log_root = r"E:\mabodev\mabozen\logs"
    
    logger = get_logger(app_name, log_root, log_cfg['LOGGING']) 
    
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