# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

#-------------------------------------------------------------------------------------------
#   Author: 
#-------------------------------------------------------------------------------------------

import maya.cmds as cmds
import maya.mel as mel

#--------------------------------------
# デフォルトネームスペース名かを判別
#--------------------------------------
def IsDefaultNamespace( nmName ):
    return ( ( nmName == "UI" ) or ( nmName == "shared" ) )
 
#--------------------------------------
# シーン内のネームスペース名のリストを取得
#--------------------------------------
def GetNamespaceList():
    userNamespace = set()
    cmds.namespace( setNamespace=':' )
     
    for subNamespace in (cmds.namespaceInfo( listOnlyNamespaces=True, recurse=True )):
        if not IsDefaultNamespace( subNamespace ):
            userNamespace.add( subNamespace )
    return ( list( userNamespace ) )
 
#--------------------------------------
# 実行
#--------------------------------------
def Execute():

    # シーン内のネームスペース名リストを取得
    namespaceList = GetNamespaceList()
    namespaceList.sort()
    namespaceList.reverse()
   
    # 一括してすべてを削除
    for subNamespace in namespaceList:
        cmds.namespace(removeNamespace=subNamespace ,mergeNamespaceWithRoot = True)
