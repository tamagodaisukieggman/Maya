# -*- coding: utf-8 -*-
u"""decorator"""
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        exec_time = time.time() - start
        print(u'[実行時間]')
        print('{0:-<79}'.format(''))
        print('module: {0}'.format(func.__module__))
        print('function: {0}'.format(func.__name__))
        print('time: {0}'.format(exec_time))
        print('{0:-<79}\n'.format(''))

        return result
    return wrapper
