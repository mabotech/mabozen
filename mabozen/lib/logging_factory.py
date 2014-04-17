
import os

import logging
import logging.handlers
import logging.config

from mabozen.lib.singleton import Singleton

class LoggingFactory(object):
    
    __metaclass__ = Singleton
    
    def __init__(self):
        """ init """
        pass
        
def get_logger(app, logroot, logging_cfg):
    """
    create all logging files
    """     

    logging_cfg['handlers']['debug']['filename'] = os.sep.join([logroot, app + '_debug.log'])
    logging_cfg['handlers']['info']['filename'] = os.sep.join([logroot, app + '_info.log'])
    logging_cfg['handlers']['warning']['filename'] = os.sep.join([logroot, app + '_warning.log'])
    logging_cfg['handlers']['error']['filename'] = os.sep.join([logroot, app + '_error.log'])
    logging_cfg['handlers']['performance']['filename'] = os.sep.join([logroot, app + '_performance.log'])
    
    logging.config.dictConfig( logging_cfg )

    logger = logging.getLogger(app)

    
    return logger