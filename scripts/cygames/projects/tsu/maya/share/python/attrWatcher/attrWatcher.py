# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : attrWatcher
# Author  : toi
# Version : 0.1.1
# Update  : 2020/11/30
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import pymel.core as pm
import os
from collections import OrderedDict
from dccUserMayaSharePythonLib import common as cm
from dccUserMayaSharePythonLib import pyCommon as pcm
#from dccUserMayaSharePythonLib import ui

#reload(cm)
#reload(pcm)


def getAttrContainingWord(words, attrs, case_sensitive=True):

    if case_sensitive:
        attrs = [x for x in attrs if pcm.isContainingAllWordsInString(words, x)]
    else:
        words = [x.upper() for x in words]
        attrs = [x for x in attrs if pcm.isContainingAllWordsInString(words, x.upper())]
    return attrs


class Ui(object):
    def __init__(self):
        self.window_name = os.path.basename(os.path.dirname(__file__))
        self.attr_trs = ['translate', 'rotate', 'scale']

    def delOverwrapWindow(self):
        if cmds.window(self.window_name, ex=True):
            pm.deleteUI(self.window_name)

    def initUi(self):
        self.delOverwrapWindow()
        pm.window(self.window_name, t=self.window_name, w=400, mb=True)

        pm.menu(l='Help')
        pm.menuItem(l='Tool help', c=pm.Callback(os.startfile, 'https://wisdom.cygames.jp/x/FABsCw'))

        #---------------------------------
        self.fl = pm.formLayout()

        top_cl = pm.columnLayout(adj=True)
        pm.separator()
        with pm.horizontalLayout(ratios=[0, 1]) as hl:
            pm.text(l='Target Node : ', ann='選択ノードが対象になります')
            self.tx_target_node = pm.text(l='', al='left')
            hl.redistribute()

        with pm.horizontalLayout(ratios=[0, 1]) as hl:
            pm.text(l='Search Word : ', ann='絞り込む文字を入力します（スペース区切りで複数文字を検索対象にします）')
            self.tf_word = pm.textField(tcc=pm.Callback(self.start_search), aie=True)
            hl.redistribute()

        self.cb_cs = pm.checkBox(
            l='Case Sensitive', ann='大文字小文字を区別する', v=False,
            cc=pm.Callback(self.start_search))
        self.cb_sn = pm.checkBox(
            l='Show Short Name', ann='ショートネームで表示します（検索結果には影響しません）', v=False,
            cc=pm.Callback(self.start_search))

        pm.separator(h=12)

        with pm.horizontalLayout():
            self.bt_cc = pm.iconTextButton(
                l='Copy Clipboard', c=pm.Callback(self.copyCbAttr), st='iconAndTextHorizontal',
                ann='選択アトリビュートの文字列をクリップボードにコピーします', i='polyCopyUV.png', bgc=(0.33, 0.33, 0.33))
            pm.iconTextButton(
                l='Select TRS', c=pm.Callback(self.selectTrs), st='iconAndTextHorizontal',
                i='out_transform.png', bgc=(0.33, 0.33, 0.33), ann='強制的にTRSのみを選択します')
        with pm.horizontalLayout():
            self.bt_lacg = pm.iconTextButton(
                l='Show Channel Box', c=pm.Callback(self.showChannelBox), st='iconAndTextHorizontal',
                ann='選択アトリビュートをチャンネルボックスに表示します', i='channelBox.png', bgc=(0.33, 0.33, 0.33))
            self.bt_lacg = pm.iconTextButton(
                l='Launch attrControlGrp', c=pm.Callback(self.startAcg), st='iconAndTextHorizontal',
                ann='選択アトリビュートのattrControlGrpを作成します', i='refEdFileList.png', bgc=(0.33, 0.33, 0.33))

        pm.setParent(self.fl)
        self.tsl = pm.textScrollList(ams=True)

        #レイアウト調整
        pm.formLayout(self.fl, e=True, af=[(top_cl, 'top', 0), (top_cl, 'left', 10), (top_cl, 'right', 10)])
        pm.formLayout(self.fl, e=True, af=[(self.tsl, 'top', 150), (self.tsl, 'right', 10), (self.tsl, 'left', 10), (self.tsl, 'bottom', 10)])
        #---------------------------------

        pm.scriptJob(p=self.window_name, e=['SelectionChanged', pm.Callback(self.sjWork)])
        pm.showWindow(self.window_name)
        self.sjWork()

    def sjWork(self):
        self.fl.setEnable(False)
        self.tx_target_node.setLabel('')

        sel = cmds.ls(sl=True)
        if sel:
            pm.textScrollList(self.tsl, e=True, removeAll=True)
            node_label = sel[0] if len(sel) == 1 else sel[0] + ' ..... Multi Select'
            self.tx_target_node.setLabel('<font color=yellow>' + node_label)
            self.fl.setEnable(True)
            self.start_search()

    def start_search(self):
        self.nodes = cmds.ls(sl=True)
        pm.textScrollList(self.tsl, e=True, removeAll=True)

        attrs = sorted(list(set(cmds.listAttr(self.nodes))))
        attrs_dict = OrderedDict()
        for ln, sn in zip(attrs, cmds.listAttr(self.nodes, sn=True)):
            attrs_dict[ln] = sn

        result_attrs = []
        word = self.tf_word.getText()
        if not word:
            result_attrs = attrs
        else:
            words = word.split(' ')
            result_attrs = getAttrContainingWord(words, attrs, self.cb_cs.getValue())

        if result_attrs:
            if self.cb_sn.getValue():
                result_attrs = [v for k, v in attrs_dict.items() if k in result_attrs]
            pm.textScrollList(self.tsl, e=True, append=result_attrs)

    def copyCbAttr(self):
        attrs = pm.textScrollList(self.tsl, q=True, selectItem=True)
        str_ = ''
        for at in attrs:
            str_ += at + ' \n\r'
        cm.toClip(str_.rstrip(' \n\r'))

    def selectTrs(self):
        self.tf_word.setText('')
        self.start_search()
        set_attrs = cmds.textScrollList(self.tsl, q=True, allItems=True)
        for trs in self.attr_trs:
            if trs in set_attrs:
                cmds.textScrollList(self.tsl, e=True, si=trs)

    def showChannelBox(self):
        attrs = cmds.textScrollList(self.tsl, q=True, selectItem=True)
        if not attrs:
            return

        warning_list = []
        for node in self.nodes:
            for at in attrs:
                try:
                    pm.setAttr(node + '.' + at, cb=True)
                except:
                    warning_list.append(node + '.' + at)
        if warning_list:
            pm.warning('These could not be displayed.', warning_list)

    def startAcg(self):
        """選択アトリビュートのattrControlGrpを作成"""

        set_attrs = cmds.textScrollList(self.tsl, q=True, selectItem=True)
        if not set_attrs:
            return

        self.initAcg(set_attrs)

    def initAcg(self, set_attrs):
        #self.nodes = cmds.ls(sl=True)

        #ウィンドウ名作成（すでにある場合は番号を付ける）
        w = '__{0}___{1}nodes'.format(self.nodes[0], len(self.nodes))
        if cmds.window(w, ex=True):
            w_list = cmds.lsUI(type='window')
            w_len = 0
            for w_ in w_list:
                if w in w_:
                    w_len += 1
            w = w + '_' + str(w_len)

        cmds.window(w, t=w, w=500, h=300)
        cmds.scrollLayout(cr=True)
        cl = cmds.columnLayout(adj=True, rs=2, co=['both', 2])

        return_at_list = []
        for node in self.nodes:
            cmds.iconTextButton(
                l=node, i='out_{0}.png'.format(cmds.nodeType(node)),
                bgc=(0.4, 0.4, 0.4), st='iconAndTextHorizontal',
                c=pm.Callback(cmds.select, node), ann='{0} を選択します'.format(node))
            for at in set_attrs:
                rl = cmds.rowLayout(nc=3, adj=True)
                try:
                    node_at = node + '.' + at

                    cmds.attrControlGrp(a=node_at)
                    return_at_list.append([node_at, rl])

                    cmds.iconTextButton(
                        st='iconOnly', i='popupMenuIcon.png', bgc=(0.4, 0.4, 0.4), w=50, h=25)

                    pm.popupMenu(b=1)
                    pm.menuItem(
                        l='Set all node', c=pm.Callback(self.set_all, node, at), rp='N',
                        ann='全てのノードの {0} を同じこの項目の値と同じにします'.format(at))
                    pm.menuItem(d=True)
                    pm.menuItem(
                        l='Key all node', c=pm.Callback(self.key_all, node, at), rp='W',
                        ann='全てのノードの {0} にキーを打ちます（現在フレーム）'.format(at))
                    pm.menuItem(
                        l='Cutkey all node', c=pm.Callback(self.cutkey_all, node, at), rp='SW',
                        ann='全てのノードの {0} に存在するキーを全て削除します'.format(at))
                    pm.menuItem(d=True)
                    pm.menuItem(
                        l='Lock all node', c=pm.Callback(self.lock_all, node, at), rp='E',
                        ann='全てのノードの {0} をロックします'.format(at))
                    pm.menuItem(
                        l='Unlock all node', c=pm.Callback(self.lock_all, node, at, False), rp='SE',
                        ann='全てのノードの {0} をアンロックします'.format(at))

                    pm.popupMenu(b=3, mm=True)
                    pm.menuItem(l='Set all node', c=pm.Callback(self.set_all, node, at), rp='N')
                    pm.menuItem(l='Key all node', c=pm.Callback(self.key_all, node, at), rp='W')
                    pm.menuItem(l='Cutkey all node', c=pm.Callback(self.cutkey_all, node, at), rp='SW')
                    pm.menuItem(l='Lock all node', c=pm.Callback(self.lock_all, node, at), rp='E')
                    pm.menuItem(l='Unlock all node', c=pm.Callback(self.lock_all, node, at, False), rp='SE')
                    '''
                    cmds.button(
                        l='Set all', c=pm.Callback(self.set_all, node, at),
                        ann='全てのノードの {0} を同じこの項目の値と同じにします'.format(at))
                    cmds.button(
                        l='Key all', c=pm.Callback(self.key_all, node, at),
                        ann='全てのノードの {0} にキーを打ちます'.format(at))
                    '''
                except:
                    pass
                cmds.setParent('..')
        cmds.showWindow(w)
        return return_at_list

    def set_all(self, node, at):
        val = pm.getAttr(node + '.' + at)
        for n in self.nodes:
            try:
                if isinstance(val, list):
                    pm.setAttr(n + '.' + at, *val)
                else:
                    pm.setAttr(n + '.' + at, val)
            except:
                pass

    def key_all(self, node, at):
        for n in self.nodes:
            try:
                pm.setKeyframe(n, at=at)
            except:
                pass

    def cutkey_all(self, node, at):
        for n in self.nodes:
            try:
                pm.cutKey(n, at=at)
            except:
                pass

    def lock_all(self, node, at, do_lock=True):
        for n in self.nodes:
            try:
                pm.setAttr(n + '.' + at, l=do_lock)
            except:
                pass

def main():
    Ui().initUi()
