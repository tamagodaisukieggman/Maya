# -*- coding: utf-8 -*-

"""
Transformノード、Shapeノードをまとめたクラス

"""

try:
    # Maya 2022-
    from past.builtins import basestring
except Exception:
    pass

import pymel.core as pm

#-------------------------------------------------
#CyNodeクラス
class CyNode:
    def __init__(self, targetNode):
        if isinstance(targetNode, basestring):
            targetNode = pm.PyNode(targetNode)

        #TransformノードとShapeノード
        self.transformNode = None
        self.shapeNode = None
        if targetNode.type() == "transform":
            self.transformNode = targetNode
            self.shapeNode = targetNode.getShape()
        else:
            if targetNode.type() == "joint":
                #jointにはTransformノードが存在しない
                self.transformNode = None
            else:
                self.transformNode = targetNode.getParent()
            self.shapeNode = targetNode

        #ノード名
        self.name = ""
        if self.transformNode is None:
            self.name = self.shapeNode.name()
        else:
            self.name = self.transformNode.name()

        #ノードの種類
        self.nodeType = ""
        if self.shapeNode is None:
            #groupにはShapeノードが存在しない
            self.nodeType = "group"
        else:
            self.nodeType = self.shapeNode.type()

        return
