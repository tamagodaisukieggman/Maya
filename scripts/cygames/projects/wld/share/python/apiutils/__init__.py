import re
import pymel.core as pm
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds

from . import uiutils

class ToolOpt():
    def __init__(self, toolname):
        self.toolname = toolname
    def getvalue(self, name, default):
        optname = self.toolname + '__' + name
        if pm.optionVar(ex=optname):
            return pm.optionVar(q=optname)
        else:
            return default
    def savevalue(self, name, value):
        optname = self.toolname + '__' + name
        if type(value) == str:
            pm.optionVar(sv=(optname, value))
        elif type(value) == int:
            pm.optionVar(iv=(optname, value))
        elif type(value) == bool:
            pm.optionVar(iv=(optname, 1 if value else 0))
        else:
            raise Exception('Invalid type:', name, value)

def get_typenodes(types=None, target=None):
    if not types:
        return []
    res = []
    if target:
        res = pm.ls(target, type=types, ni=True)
        res += pm.listRelatives(target, ad=True, type=types, ni=True)
    else:
        res = pm.ls(sl=True, type=types, ni=True)
        res += pm.listRelatives(ad=True, type=types, ni=True)
    return res


def copy_hierarchy(types=None, target=None, parent=None):
    if not target:
        if types:
            target = pm.selected(type=types)
        else:
            target = pm.selected()

    if type(target) is not list:
        target = [target]
    res = []
    _res = []
    for n in target:
        cp = pm.duplicate(n, po=True)[0]
        res.append((n, cp))
        if parent:
            pm.parent(cp, parent.shortName())
            pm.rename(cp, n.nodeName())
        chs = []
        if types:
            chs = pm.listRelatives(n, c=True, type=types)
        else:
            chs = pm.listRelatives(n, c=True)
        for c in chs:
            _res += copyHierarchy(types, c, parent=cp)

    return res + _res
    

def find_typenode_root(node, noderoots, type):
    if pm.objectType(node) != 'joint':
        return None
    if node in noderoots:
        return noderoots[node]

    if node.root() != node:
        p = node.firstParent()
        if p and pm.objectType(p) == 'joint':
            root = find_typenode_root(p, noderoots, type)
            noderoots[p] = root
            return root
        
    noderoots[node] = node
    return node    
    

def get_typenode_roots(sel=None, type=None):
    if not sel:
        sel = get_typenodes(types='joint')
    noderoots = {}
    roots = []
    for n in sel:
        root = find_typenode_root(n, noderoots, type=type)
        if root not in roots:
            roots.append(root)
    #for r in roots:
    #    print 'root:', r
    return roots
        

def captureViewport(mPanel, filename, extension, w=-1, h=-1, aspect=True):
    img = om.MImage()
    view = omui.M3dView()
    omui.M3dView.getM3dViewFromModelPanel(mPanel, view)
    view.refresh(False, True)
    view.readColorBuffer(img, True)
    img.writeToFile(filename, extension)

# for compatibility.
def getTypeNodes(nodeTypes=None, target=None):
    return get_typenodes(types=nodeTypes, target=target)


def copyHierarchy(nodeTypes=None, target=None, parent=None):
    return copy_hierarchy(types=nodeTypes, target=target, parent=parent)


