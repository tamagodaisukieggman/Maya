# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

#-------------------------------------------------------------------------------------------
#   Author: Hideyo Isayama
#-------------------------------------------------------------------------------------------

import maya.cmds as cmds
import maya.mel as mel

scriptPrefix="TkgSelectJoint."
uiPrefix="TkgSelectJoint"

#-------------------------------------------------------------------------------------------
#   実行
#-------------------------------------------------------------------------------------------
def Execute():

    cmds.select(hierarchy=True)
    selectList = cmds.ls(sl=True)

    if selectList == None:
        return

    if len(selectList) == 0:
        return

    jointList = []
    for i in range(len(selectList)):

        thisSelect = selectList[i]

        if cmds.objectType(thisSelect) != "joint":
            continue

        jointList.append(thisSelect)

    cmds.select(jointList,r=True)
