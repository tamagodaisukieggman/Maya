# -*- coding: utf-8 -*-
u"""decorator"""
import traceback
from functools import wraps

import maya.cmds as cmds

def autokeyoff(func):
    u"""処理中にautokeyをOFF"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        autokey_stat = cmds.autoKeyframe(q=True, st=True)
        cmds.autoKeyframe(st=False)
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(traceback.format_exc())
        finally:
            cmds.autoKeyframe(st=autokey_stat)
            return result
    return wrapper
