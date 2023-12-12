# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : nodeFinder
# Author  : toi
# ReleaseData : 2022/6/15
# LastUpdate  : 2023/1/16
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
#import maya.mel as mm
import pymel.core as pm
import os
#import stat
#import datetime
from dccUserMayaSharePythonLib import common as cm
from dccUserMayaSharePythonLib import pyCommon as pcm
from dccUserMayaSharePythonLib import ui


def getNodeContainingWord(words, case_sensitive=True, node_types=None, start_end=0):
    if node_types:
        target_nodes = cmds.ls(exactType=node_types)
    else:
        target_nodes = cmds.ls()

    if case_sensitive:
        target_nodes = [x for x in target_nodes if pcm.isContainingAllWordsInString(words, x)]
    else:
        words = [x.upper() for x in words]
        target_nodes = [x for x in target_nodes if pcm.isContainingAllWordsInString(words, x.upper())]

    if start_end:
        target_nodes_strings = target_nodes
        if not case_sensitive:
            target_nodes_strings = [x.upper() for x in target_nodes]

        tmp_list = []
        if start_end == 1:
            for i in range(len(target_nodes_strings)):
                for w in words:
                    if target_nodes_strings[i].startswith(w):
                        tmp_list.append(target_nodes[i])
        elif start_end == 2:
            for i in range(len(target_nodes_strings)):
                for w in words:
                    if target_nodes_strings[i].endswith(w):
                        tmp_list.append(target_nodes[i])
        target_nodes = tmp_list

    return target_nodes


class Ui(object):
    def __init__(self):
        self.window_name = os.path.basename(os.path.dirname(__file__))
        self.main_attr_list = ('transform', 'joint', 'mesh', 'camera', 'locator')
        self.label_type = 'Type : '
        self.label_num = 'NodeNum : '
        self.rb_list = ['rb_none_nodefinder', 'rb_start_nodefinder', 'rb_end_nodefinder']
        self.rb_dict = {self.rb_list[0]: 0, self.rb_list[1]: 1, self.rb_list[2]: 2}

    def delOverwrapWindow(self):
        if cmds.window(self.window_name, ex=True):
            pm.deleteUI(self.window_name)

    def initUi(self):
        self.delOverwrapWindow()
        pm.window(self.window_name, t=self.window_name, mb=True)
        pm.menu(l='Help')
        pm.menuItem(l='Tool help', c=pm.Callback(os.startfile, 'https://wisdom.cygames.jp/x/ddkrCw'))

        fl = pm.formLayout()
        sp = pm.separator()

        with pm.horizontalLayout(ratios=[0, 1]) as hl:
            pm.text(l='Search Word : ')
            self.tf_word = pm.textField(ec=pm.Callback(self.start_search), aie=True)
            hl.redistribute()

        self.cb_cs = pm.checkBox(l='Case Sensitive', ann='大文字小文字を区別する', v=False)
        self.rc_se = pm.radioCollection()
        with pm.horizontalLayout(ratios=[0, 1, 1, 1]) as hl2:
            pm.text(l='StartEnd : ')
            pm.radioButton(self.rb_list[0], l='None', sl=True)
            pm.radioButton(self.rb_list[1], l='Start')
            pm.radioButton(self.rb_list[2], l='End')

        with pm.horizontalLayout(ratios=[0, 0, 0, 1]) as hl3:
            pm.text(l='Node Type : ')
            pm.radioCollection()
            pm.radioButton(l='All', sl=True, cc=pm.Callback(self.change_rb))
            self.rb_sp = pm.radioButton(l='')
            self.tf_sp = pm.textField(ec=pm.Callback(self.start_search), aie=True)
            pm.popupMenu(b=3)
            for at in self.main_attr_list:
                pm.menuItem(l=at, c=pm.Callback(self.tf_sp.setText, at))
            hl.redistribute()

        sp2 = pm.separator()

        self.bt_start = pm.button('Search', c=pm.Callback(self.start_search))
        with pm.horizontalLayout() as hl4:
            self.tx_type = pm.text(al='left')
            self.tx_num = pm.text(l='NodeNum : ', al='right')

        self.tsl = pm.textScrollList(
            ams=True, ekf=True,
            sc=pm.Callback(self.select_node),
            deleteKeyCommand=pm.Callback(self.delete_nodes),
            dcc=pm.Callback(ui.expandOutlinerSelected))
        pm.popupMenu(b=3)
        pm.menuItem(
            l='Expand outliner', ann='アウトライナーを展開します',
            c=pm.Callback(ui.expandOutlinerSelected), i='Tree_Expanded_Down.png')
        pm.menuItem(d=True)
        pm.menuItem(
            l='Delete', ann='選択中のノードを削除します',
            c=pm.Callback(self.delete_nodes), i='SP_MessageBoxCritical.png')

        #レイアウト調整
        pm.formLayout(fl, e=True, af=[(sp, 'top', 0), (sp, 'left', 10), (sp, 'right', 10)])
        pm.formLayout(fl, e=True, af=[(hl, 'top', 10), (hl, 'right', 10), (hl, 'left', 10)])
        pm.formLayout(fl, e=True, af=[(self.cb_cs, 'top', 40), (self.cb_cs, 'left', 10)])
        pm.formLayout(fl, e=True, af=[(hl2, 'top', 60), (hl2, 'left', 10), (hl2, 'right', 10)])
        pm.formLayout(fl, e=True, af=[(hl3, 'top', 80), (hl3, 'left', 10), (hl3, 'right', 10)])
        pm.formLayout(fl, e=True, af=[(sp2, 'top', 110), (sp2, 'left', 10), (sp2, 'right', 10)])
        pm.formLayout(fl, e=True, af=[(self.bt_start, 'top', 120), (self.bt_start, 'left', 10), (self.bt_start, 'right', 10)])
        pm.formLayout(fl, e=True, af=[(hl4, 'top', 145), (hl4, 'right', 10), (hl4, 'left', 10)])
        pm.formLayout(fl, e=True, af=[(self.tsl, 'top', 165), (self.tsl, 'left', 10), (self.tsl, 'right', 10), (self.tsl, 'bottom', 10)])

        #---------------------------------

        #pm.scriptJob(p=self.window_name, e=['SceneOpened', pm.Callback(self.sjWork)])
        pm.showWindow(self.window_name)
        self.change_rb()
        self.reset_text()
        #self.sjWork()

    def change_rb(self):
        enable = pm.radioButton(self.rb_sp, q=True, sl=True)
        pm.textField(self.tf_sp, e=True, en=enable)

    def reset_text(self):
        pm.text(self.tx_type, e=True, l=self.label_type)
        pm.text(self.tx_num, e=True, l=self.label_num)

    def start_search(self):
        pm.textScrollList(self.tsl, e=True, removeAll=True)
        self.reset_text()

        node_types = None
        if pm.radioButton(self.rb_sp, q=True, sl=True):
            text_ = self.tf_sp.getText()
            if text_:
                node_types = text_.split(' ')

        start_end = pm.radioCollection(self.rc_se, q=True, sl=True)
        start_end = self.rb_dict[start_end]

        input_words = self.tf_word.getText()
        if not input_words and node_types is None:
            mes = 'シーン内全てのノードを表示します。'
            response = cmds.confirmDialog(
                title='Confirm', message=mes,
                button=['実行', '中止'], defaultButton='実行', cancelButton='中止', dismissString='中止',
                p=self.window_name, icon='question')
            if response == '中止':
                return

        pm.button(self.bt_start, e=True, l='Searching...')
        pm.refresh()

        if input_words:
            words = input_words.split(' ')
            result_nodes = getNodeContainingWord(words, self.cb_cs.getValue(), node_types, start_end)
        else:
            if node_types:
                result_nodes = cmds.ls(exactType=node_types)
            else:
                result_nodes = cmds.ls()

        if result_nodes:
            self.show_result(result_nodes)

        pm.text(self.tx_num, e=True, l=self.label_num + str(len(result_nodes)))
        pm.button(self.bt_start, e=True, l='Search')

    def show_result(self, nodes):
        pm.textScrollList(self.tsl, e=True, append=nodes)

    def select_node(self):
        nodes = pm.textScrollList(self.tsl, q=True, selectItem=True)
        pm.select(nodes)
        pm.text(self.tx_type, e=True, l=self.label_type + pm.nodeType(nodes[0]))

    def delete_nodes(self):
        nodes = pm.textScrollList(self.tsl, q=True, selectItem=True)
        sel_top_index = pm.textScrollList(self.tsl, q=True, selectIndexedItem=True)[0]
        for node in nodes:
            try:
                pm.delete(node)
            except:
                pass

        self.after_del()

        try:
            pm.textScrollList(self.tsl, e=True, showIndexedItem=sel_top_index - 1)
        except:
            pass

    def after_del(self):
        no_exists_list = [x for x in pm.textScrollList(self.tsl, q=True, allItems=True) if not pm.objExists(x)]
        pm.textScrollList(self.tsl, e=True, removeItem=no_exists_list)

    #---------------------------------------------------------------------------------
    #def sjWork(self):
    #	pass


def main():
    Ui().initUi()
