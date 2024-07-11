# -*- coding: utf-8 -*-

"""
Transformノード、Shapeノードをまとめたクラス

"""
try:
    # Maya 2022-
    from past.builtins import basestring
    from builtins import object
except Exception:
    pass

import pymel.core as pm


#-------------------------------------------------
#TkgDagNodeクラス
class TkgDagNode(object):
    def __init__(self, targetNode):
        #ノード名が渡された場合はPyNodeに変換する
        if isinstance(targetNode, basestring):
            targetNode = pm.PyNode(targetNode)

        #TransformノードとShapeノード
        self.transNode = None
        self.shapeNode = None
        if targetNode.type() == "transform":        #transformノードの場合
            self.transNode = targetNode
            self.shapeNode = targetNode.getShape()
        else:                                       #shapeノードの場合
            self.shapeNode = targetNode
            if self.shapeNode.type() == "joint":
                #jointにはTransformノードが存在しない
                self.transNode = None
            else:
                self.transNode = self.shapeNode.getParent()

        #ノードの種類
        self.nodeType = ""
        if self.shapeNode is None:
            #groupにはShapeノードが存在しない
            self.nodeType = "group"
        else:
            self.nodeType = self.shapeNode.type()

        #メインノード
        self.mainNode = None
        self.mainLongName = ""
        self.mainShortName = ""
        if self.nodeType == "joint":
            self.mainNode = self.shapeNode
            self.mainLongName = self.shapeNode.longName()
            self.mainShortName = self.shapeNode.shortName()
        else:
            self.mainNode = self.transNode
            self.mainLongName = self.transNode.longName()
            self.mainShortName = self.transNode.shortName()

        return
