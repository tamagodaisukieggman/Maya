import maya.cmds as mc
import pymel.core as pm


def undo(func):
    def wrapper(*args, **kwargs):
        pm.undoInfo(openChunk=True)
        try:
            ret = func(*args, **kwargs)
        finally:
            pm.undoInfo(closeChunk=True)
        return ret

    return wrapper


def undo_pm(func):
    def wrapper(*args, **kwargs):
        pm.undoInfo(openChunk=True)
        try:
            ret = func(*args, **kwargs)
        finally:
            pm.undoInfo(closeChunk=True)
        return ret

    return wrapper


def refresh(func):
    def wrapper(*args, **kwargs):
        pm.refresh(su=True)
        try:
            ret = func(*args, **kwargs)
        finally:
            pm.refresh(su=False)
        return ret

    return wrapper
