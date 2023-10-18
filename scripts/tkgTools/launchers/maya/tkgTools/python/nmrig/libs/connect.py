# -*- coding: utf-8 -*-
import maya.cmds as cmds
from imp import reload

def triple_connect(source, destination, attribute_list, triple='XYZ',
                   force=True):
    for attr in attribute_list:
        for axis in triple:
            attr_name = attr + axis
            cmds.connectAttr(source + '.' + attr_name,
                             destination + '.' + attr_name,
                             force=force)
