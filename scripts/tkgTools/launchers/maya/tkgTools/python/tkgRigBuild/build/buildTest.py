# -*- coding: utf-8 -*-

import maya.cmds as cmds

def create_sphere(name="default_name"):
    sph = cmds.polySphere(name=name, constructionHistory=False)[0]
    return sph
