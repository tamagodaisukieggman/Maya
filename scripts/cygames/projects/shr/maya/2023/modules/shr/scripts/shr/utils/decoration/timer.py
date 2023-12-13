# -*- coding: utf-8 -*-
u"""decorator"""
import time
from functools import wraps

import logging
# from mtku.maya.log import MtkDBLog


# logger = MtkDBLog(__name__)
logger = logging.getLogger(__name__)


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        exec_time = time.time() - start
        logger.info(u'[実行時間]')
        logger.info('{0:-<79}'.format(''))
        logger.info('module: {0}'.format(func.__module__))
        logger.info('function: {0}'.format(func.__name__))
        logger.info('time: {0}'.format(exec_time))
        logger.info('{0:-<79}\n'.format(''))

        return result
    return wrapper
