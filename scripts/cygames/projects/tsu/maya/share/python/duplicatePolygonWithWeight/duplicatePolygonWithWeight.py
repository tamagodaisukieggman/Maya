# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : duplicatePolygonWithWeight
# Author  : toi
# ReleaseDate : 2023/2/06
# LastUpdate  : 2023/2/15
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mm
import os
from functools import partial
from dccUserMayaSharePythonLib import common as cm
from dccUserMayaSharePythonLib import pyCommon as pcm
from dccUserMayaSharePythonLib import file_dumspl as f
from dccUserMayaSharePythonLib import skinning as sk


class Ui(object):
    def __init__(self):
        self.window_name = os.path.basename(os.path.dirname(__file__))

        self.duplicate_node_name = 'duplicateWithWeightNode'
        self.add_attr_name = 'original_poly_list'

        self.buttonCol = (0.3, 0.3, 0.3)
        self.frame_col = (0.2, 0.2, 0.8)
        self.row_ratios = (1, 0.5, 0.7, 0.3)

        self.setting_dict = f.createSettingFile('duplicatePolygonWithWeight')
        self.weight_folder = os.path.join(f.getSettingFilePath('duplicatePolygonWithWeight'), 'weight')
        if not os.path.isdir(self.weight_folder):
            os.makedirs(self.weight_folder)

    def delOverwrapWindow(self):
        if cmds.window(self.window_name, ex=True):
            cmds.deleteUI(self.window_name)

    def initUi(self):
        self.delOverwrapWindow()
        cmds.window(self.window_name, t=self.window_name, mb=True)
        cmds.menu(l='Help')
        cmds.menuItem(l='Tool help', c="os.startfile('https://wisdom.cygames.jp/x/Ntv4IQ')")
        cl_top = cmds.columnLayout(adj=True)

        cmds.frameLayout(l='選択モード', mw=2, mh=2, bgc=self.frame_col)
        with pm.horizontalLayout():
            cmds.button(l='オブジェクトモード', c=partial(self.objectMode))
            cmds.button(l='ポリゴン選択モード', c=partial(self.polySelectMode))
        cmds.setParent(cl_top)

        cmds.frameLayout(l='作成', mw=2, mh=2, bgc=self.frame_col)
        cmds.columnLayout(adj=True, rs=3)
        self.clg = cmds.colorSliderGrp(l='メッシュカラー ', rgb=self.setting_dict.get('clg_col', (0, 0, 0.5)))
        cmds.separator(h=10)
        self.cb_merge_vtx = cmds.checkBox(
            l='同位置の頂点をマージ', v=self.setting_dict.get('cb_merge_vtx', False),
            cc=partial(self._changeCBMerge))
        with pm.horizontalLayout(ratios=[0, 0, 0, 1]) as hl_amount:
            cmds.text(l='閾値: ', al='right')
            cmds.radioCollection()
            self.rb_auto = cmds.radioButton(
                l='auto', sl=self.setting_dict.get('rb_auto', True),
                cc=partial(self._changeRBMerge))
            cmds.radioButton(l='指定')
            self.ff_amount = cmds.floatField(v=self.setting_dict.get('ff_amount', 0.01))
        self.hl_amount = hl_amount

        cmds.separator(h=10)
        cmds.button(l='選択ポリゴンを Weight 付きで [ 複製 ]', c=partial(self.startDup), h=30, bgc=[0.1, 0.2, 0.4])
        cmds.setParent(cl_top)

        cmds.frameLayout(l='管理', bgc=self.frame_col)
        with pm.horizontalLayout(ratios=self.row_ratios):
            pm.text(l='複製ノード（選択）')
            pm.text(l='元メッシュ表示')
            pm.text(l='Weightペースト')
            pm.text(l='削除')
        self.cl_sedond = cmds.columnLayout(adj=True, co=['both', 3], bgc=(0.2, 0.2, 0.2), rs=3)

        cmds.showWindow(self.window_name)
        cmds.scriptJob(p=self.window_name, e=['SceneOpened', pm.Callback(self._updateUi)])
        self._updateUi()

    def _updateUi(self):
        self._changeCBMerge()
        self._changeRBMerge()
        children_layouts = cmds.columnLayout(self.cl_sedond, q=True, ca=True)
        if children_layouts:
            cmds.deleteUI(children_layouts)
        cmds.evalDeferred(self._createTargetNodeButtons)

    def _changeCBMerge(self, *args):
        val = cmds.checkBox(self.cb_merge_vtx, q=True, v=True)
        cmds.formLayout(self.hl_amount, e=True, en=val)

    def _changeRBMerge(self, *args):
        val = cmds.radioButton(self.rb_auto, q=True, sl=True)
        cmds.floatField(self.ff_amount, e=True, en=not val)

    def _createTargetNodeButtons(self):
        dup_nodes = self._getDuplicateNodes()
        if dup_nodes:
            cmds.setParent(self.cl_sedond)
            for dup_node in dup_nodes:
                with pm.horizontalLayout(ratios=self.row_ratios):
                    cmds.button(l=dup_node, bgc=self.buttonCol, c='cmds.select("{}")'.format(dup_node))
                    with pm.horizontalLayout(ratios=[1, 1]):
                        cmds.button(
                            l='ON', bgc=self.buttonCol,
                            c=partial(self.originalNodeOnOff, dup_node, True))
                        cmds.button(
                            l='OFF', bgc=self.buttonCol,
                            c=partial(self.originalNodeOnOff, dup_node, False))
                    cmds.button(
                        l='実行',
                        bgc=self.buttonCol,
                        c=partial(self.startPaste, dup_node)
                    )
                    cmds.button(l='実行', bgc=self.buttonCol, c=partial(self.delete, dup_node))

    def _getAddAttrs(self, node):
        all_attrs = cmds.listAttr(node, userDefined=True)
        result = []
        if all_attrs is not None:
            for attr in all_attrs:
                if self.add_attr_name in attr:
                    result.append(attr)
        return result

    def _getDuplicateNodes(self):
        result = []
        for node in cmds.ls(transforms=True):
            if self._getAddAttrs(node):
                result.append(node)
        return result

    def startDup(self, *args):
        cm.hum()
        component_selection = cmds.ls(sl=True, fl=True)
        if not component_selection:
            return

        if '.f[' not in component_selection[0] or cmds.nodeType(component_selection[0]) != 'mesh':
            return

        # マージ関連オプション取得
        do_merge = cmds.checkBox(self.cb_merge_vtx, q=True, v=True)
        self.setting_dict.set('cb_merge_vtx', do_merge)
        merge_distance = None
        if not cmds.radioButton(self.rb_auto, q=True, sl=True):
            merge_distance = cmds.floatField(self.ff_amount, q=True, v=True)
            self.setting_dict.set('ff_amount', merge_distance)

        cmds.undoInfo(openChunk=True)
        # 複製実行
        dup_node = self.dup(component_selection, do_merge, merge_distance)

        # メッシュの見た目調整
        col = cmds.colorSliderGrp(self.clg, q=True, rgb=True)
        self.setting_dict.set('clg_col', col)
        cmds.setAttr(dup_node + '.overrideEnabled', True)
        cmds.setAttr(dup_node + '.overrideColorRGB', *col)
        cmds.setAttr(dup_node + '.overrideRGBColors', 1)
        shape = cm.getShape([dup_node])
        cmds.setAttr(shape[0] + '.displayBorders', 1)

        cmds.select(dup_node)
        self.objectMode()

        cmds.undoInfo(closeChunk=True)
        self._updateUi()

    def dup(self, component_selection, do_merge, merge_distance=None):
        result_list = sk.duplicateSelPolygon2(component_selection)
        dup_nodes = []
        for dup_node, original_node, polys in result_list:
            dup_nodes.append(dup_node)
            sk.bindPairModel(original_node, dup_node)
            sk.copySkinWeight(original_node, dup_node)

        # 複製したノード同士をコンバイン
        if len(result_list) == 1:
            last_node = dup_node
        else:
            last_node, _ = cmds.polyUniteSkinned(dup_nodes, constructionHistory=False)
        last_node = cmds.rename(last_node, self.duplicate_node_name + '#')

        at_num = 1
        for dup_node, original_node, polys in result_list:
            cm.addAt(last_node, self.add_attr_name + str(at_num), [original_node, polys])
            at_num += 1
        if len(result_list) != 1:
            cmds.delete(dup_nodes)

        if do_merge:
            if merge_distance is None:
                length_sum = cm.getBoundingboxEdgeLengthSum(last_node)
                merge_distance = length_sum / 1000
            shape = cm.getShape([last_node])
            vtx = cmds.ls(shape[0] + '.vtx[*]', fl=True)
            cmds.select(vtx)
            cmds.polyMergeVertex(d=merge_distance)

            # バインドを外して戻す（マージでvertexがズレるのを適正化）
            sk.exportWeight(last_node, self.weight_folder, 'tmp')
            sk.unbind(last_node)
            # cmds.select(last_node)
            # mm.eval('DeleteHistory;')
            sk.importWeight(last_node, self.weight_folder, 'tmp_weight.xml', 3)

        return last_node

    def startPaste(self, *args):
        dup_node = args[0]
        attrs = self._getAddAttrs(dup_node)
        cmds.undoInfo(openChunk=True)
        for attr in attrs:
            self.paste(dup_node, attr)
        cmds.select(dup_node)
        cmds.undoInfo(closeChunk=True)

    def paste(self, dup_node, attr):
        original_node, poly_list = cmds.getAttr(dup_node + '.' + attr)
        poly_list = pcm.str2List(poly_list)
        vertex_list = pm.polyListComponentConversion(poly_list, toVertex=True)
        # print('AAAA', original_node, vertex_list)

        sk.bindPairModel(dup_node, original_node)

        # セットを作成してWeightペースト
        tmp_set = cmds.sets(vertex_list)
        sk.copySkinWeight(dup_node, tmp_set, influenceAssociation_=['oneToOne'])
        cmds.delete(tmp_set)

    def originalNodeOnOff(self, *args):
        dup_node = args[0]
        onoff = args[1]
        attrs = self._getAddAttrs(dup_node)
        cmds.select(cl=True)
        for attr in attrs:
            original_node, poly_list = cmds.getAttr(dup_node + '.' + attr)
            cmds.setAttr(original_node + '.v', onoff)
            cmds.select(original_node, d=not onoff, add=True)

    def delete(self, *args):
        dup_node = args[0]
        cmds.delete(dup_node)
        self._updateUi()

    def objectMode(self, *args):
        mm.eval('changeSelectMode -object;')

    def polySelectMode(self, *args):
        sels = cmds.ls(sl=True)
        if sels:
            mm.eval('changeSelectMode -component;')
            mm.eval('doMenuComponentSelectionExt("{}", "facet", 1)'.format(sels[0]))

    @staticmethod
    def markingColor(nodes, set_color):
        for node in nodes:
            cmds.setAttr(node + '.overrideEnabled', set_color)


def main():
    Ui().initUi()
