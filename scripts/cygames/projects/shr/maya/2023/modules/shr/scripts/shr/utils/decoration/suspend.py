# -*- coding: utf-8 -*-
u"""decorator"""
import traceback
from functools import wraps

import maya.cmds as cmds

import logging
# from mtku.maya.log import MtkDBLog

# logger = MtkDBLog(__name__)
logger = logging.getLogger(__name__)


def suspend(func):
    u"""リフレッシュ イベントをsuspend"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        cmds.refresh(su=True)
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
        finally:
            cmds.refresh(su=False)
            return result
    return wrapper
