# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : nodeSelecter
# Author  : toi
# Version : 0.1.0
# Update  : 2022/6/13
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
#import maya.mel as mm
import pymel.core as pm
import os
import sys
#import stat
from collections import OrderedDict
#from rigSupportTools import ui as rstui
from dccUserMayaSharePythonLib import ui


try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__


def nodeSelecter(nodes):
    itb_name = 'itb_node_selecter'
    css_base = '''
        QPushButton{{
            border-radius: 3px;
            font-size: 20px;
            text-align: left;
            background-color: {0};
        }}
        QPushButton:hover{{
            background-color: {1};
        }}
    '''
    css_sel = css_base.format('steelblue', 'dodgerblue')
    css_desel = css_base.format('#696969', 'darkgray')

    def select(node):
        cmds.select(node, add=cmds.getModifiers() == 4)

    def sj_work(*args):
        sels = cmds.ls(sl=True)
        ignore_reset_col_itb_list = []
        for sel in sels:
            if sel in itb_dict:
                ignore_reset_col_itb_list.append(sel)
                itb_dict[sel].setStyleSheet(css_sel)

        for node, itb in itb_dict.items():
            if node not in ignore_reset_col_itb_list:
                itb.setStyleSheet(css_desel)

    def allSelect():
        cmds.select(cl=True)
        for node, _ in itb_dict.items():
            cmds.select(node, add=True)

    def allVis(onoff):
        for node, _ in itb_dict.items():
            # セットの場合はmelで対処
            if cmds.nodeType(node) == 'objectSet':
                sels = cmds.ls(sl=True)
                cmds.select(node)
                if onoff:
                    pm.mel.ShowSelectedObjects()
                else:
                    pm.mel.HideSelectedObjects()
                cmds.select(sels)
            else:
                cmds.setAttr(node + '.v', onoff)

    def addSelectedNodes(current_window):
        w_pos = pm.window(current_window, q=True, topLeftCorner=True)
        w_size = pm.window(current_window, q=True, widthHeight=True)
        new_nodes = cmds.ls(sl=True)
        if new_nodes:
            pm.evalDeferred(pm.Callback(pm.deleteUI, current_window))
            allSelect()
            pm.select(new_nodes, add=True)
            new_window = nodeSelecter(cmds.ls(sl=True))
            pm.window(new_window, e=True, topLeftCorner=w_pos)
            pm.window(new_window, e=True, widthHeight=w_size)
            pm.select(new_nodes)

    w = pm.window(t='{0}...[{1}]'.format(nodes[0], len(nodes)), w=500, mb=True)
    pm.menu(l='Add')
    pm.menuItem(l='Add selected nodes', c=pm.Callback(addSelectedNodes, w))
    pm.menu(l='Select All', tearOff=True)
    mi_all_on = pm.menuItem(l='On', c=pm.Callback(pm.select, nodes))
    pm.menuItem(l='Off', c=pm.Callback(pm.select, cl=True))
    pm.menu(l='Vis All', tearOff=True)
    pm.menuItem(l='On', c=pm.Callback(allVis, True))
    pm.menuItem(l='Off', c=pm.Callback(allVis, False))
    pm.menu(l='Help')
    pm.menuItem(l='Tool help', c=pm.Callback(os.startfile, 'https://wisdom.cygames.jp/x/_SpsCw'))

    pm.scrollLayout()
    pm.popupMenu(b=3, mm=True)
    pm.menuItem(l='Select All', c=pm.Callback(allSelect), rp='N')
    pm.menuItem(l='Deselect All', c=pm.Callback(pm.select, cl=True), rp='S')
    pm.menuItem(l='Vis All', c=pm.Callback(allVis, True), rp='W')
    pm.menuItem(l='Hide All', c=pm.Callback(allVis, False), rp='E')

    itb_dict = OrderedDict()
    for node in nodes:
        try:
            pm.rowLayout(nc=2, adj=True)
            # セットの場合はアトリビュートが存在しないので、ポップアップメニューで対処
            if cmds.nodeType(node) == 'objectSet':
                pm.text(l='', w=218, al='right')
            else:
                pm.attrControlGrp(a=node + '.v')
            itb = ui.qtbutton(
                l=node, h=30, c=pm.Callback(select, node),
                i='out_{0}.png'.format(cmds.nodeType(node)))
            itb.setText(node)
            # itb.doubleClicked.connect(ui.expandOutlinerSelected)
            pm.setParent('..')
            itb_dict[node] = itb
        except Exception as e:
            print(e)
            print(sys.exc_info()[2].tb_lineno)

    pm.scriptJob(e=['SelectionChanged', pm.Callback(sj_work)], p=w)
    w.show()
    sj_work()

    width_list = []
    for node, itb in itb_dict.items():
        width_list.append(itb.width())
    for node, itb in itb_dict.items():
        itb.setFixedWidth(max(width_list) * 2)

    return w


def main():
    sels = cmds.ls(sl=True)
    if sels:
        nodeSelecter(sels)

