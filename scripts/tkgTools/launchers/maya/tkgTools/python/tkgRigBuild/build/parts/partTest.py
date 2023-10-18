# -*- coding: utf-8 -*-

import maya.cmds as cmds

import tkgRigBuild.build.buildTest as tkgBuild

def create_with_offset(translateX=5, scale=2, iterations=10, name="default_name"):
    for i in range(iterations):
        sph = tkgBuild.create_sphere(name="{}_{:03}_GEO".format(name, i + 1))
        cmds.xform(sph, ws=True, t=(translateX * i, 0, 0), s=[(scale * i + 1), (scale * i + 1), (scale * i + 1)])
