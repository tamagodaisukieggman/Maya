# -*- coding: utf-8 -*-
u"""decorator"""
import traceback
from functools import wraps

import maya.cmds as cmds

def suspend(func):
    u"""リフレッシュ イベントをsuspend"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        cmds.refresh(su=True)
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        finally:
            cmds.refresh(su=False)
            return result
    return wrapper
