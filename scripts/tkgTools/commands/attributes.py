# -*- coding: utf-8 -*-
import maya.cmds as cmds

def get_enums(obj_attr=None):
    if cmds.objExists(obj_attr):
        enums = cmds.addAttr(obj_attr, q=True, en=True)
        if enums:
            return enums.split(':')

def reset_transform(obj, func):
    wt = cmds.xform(obj, q=True, t=True, ws=True)
    wr = cmds.xform(obj, q=True, ro=True, ws=True)

    func()

    cmds.xform(obj, t=wt, ro=wr, ws=True, a=True)

def round_attrs(obj=None, attrs=None):
    for at in attrs:
        set_at = '{}.{}'.format(obj, at)
        val = cmds.getAttr(set_at)
        if not val == 0.0:
            if 'e' in str(val):
                cmds.setAttr(set_at, 0.0)
                continue

            try:
                cmds.setAttr(set_at, truncate(round(val, 3), 3))
            except Exception as e:
                print(traceback.format_exc())
