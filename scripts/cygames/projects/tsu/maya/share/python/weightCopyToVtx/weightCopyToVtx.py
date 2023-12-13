# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : weightCopyToVtx
# Author  : toi
# Update  : 2022/9/07
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import pymel.core as pm
import os

from dccUserMayaSharePythonLib import common as cm
from dccUserMayaSharePythonLib import pyCommon as pcm
from dccUserMayaSharePythonLib import skinning as sk
from dccUserMayaSharePythonLib import file_dumspl as f


class WeightCopyToVtx(object):
    def __init__(self):
        self.window_name = os.path.basename(os.path.dirname(__file__))
        self.cop_tool = sk.CopyPasteMesh2Vtx()
        self.cop_tool_history = sk.CopyPasteMesh2Vtx()
        self.cop_v2v_tool = sk.CopyPasteVtxsWeight()

        self.wb = 'workbench'
        self.attr_name = 'weightCopytoVtxs'
        self.bt_col = [0.3, 0.3, 0.3]
        self.bt_cop_col = [0.1, 0.2, 0.4]
        self.frame_col = [0.2, 0.2, 0.8]
        self.tf_label = 'tf_label_weightCopytoVtxs'
        self.s_ofet = 5

        self.infl_assoc_dict = {
            'Closest joint': 'closestJoint',
            'Closest bone': 'closestBone',
            'One to one': 'oneToOne',
            'Label': 'label',
            'Name': 'name'
        }

        # 履歴用のアトリビュートリスト（値は入らない）
        self.history_at_list = []

        self.bt_list = []
        self.bt_list2 = []

        # 設定ファイル
        self.SETTING_DIR = os.path.join(
            os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"),
            'Documents', 'maya', 'Scripting_Files', 'weightCopyToVtx')
        self.SETTING_JSON = os.path.join(self.SETTING_DIR, 'weightCopyToVtx.json')
        if not os.path.isfile(self.SETTING_JSON):
            f.exportJson(self.SETTING_JSON)
        self.setting = f.JsonDict(self.SETTING_JSON)

    def delOverwrapWindow(self):
        if cmds.window(self.window_name, ex=True):
            pm.deleteUI(self.window_name)

    def initUi(self):
        self.delOverwrapWindow()
        pm.window(self.window_name, t=self.window_name, mb=True)
        pm.menu(l='Help')
        pm.menuItem(l='Tool help', c=pm.Callback(os.startfile, 'https://wisdom.cygames.jp/x/sU7AEw'))
        with pm.formLayout() as fl:
            with pm.frameLayout(l='Weight値のCopyPaste （ 頂点同士 ）', cll=True, bgc=self.frame_col) as fl_v2v:
                with pm.columnLayout(adj=True, co=('both', 3)):
                    with pm.horizontalLayout(ratios=[2, 3, 3]): #, ann='vtxを選択順番でコピーペーストします'):
                        pm.text(l='複数頂点同士 : ', al='right')
                        pm.button(l='Copy', c=pm.Callback(self.cop_v2v_tool.copyWeightSelVtxs))
                        pm.button(l='Paste', c=pm.Callback(self.cop_v2v_tool.pasteWeightSelVtxs))
                    with pm.horizontalLayout(ratios=[2, 6]):  # , ann='最初に選択したvtxのWeightに全てをペーストします'):
                        pm.text(l='交互選択 : ', al='right')
                        pm.button(l='CopyPaste', c=pm.Callback(self.cop_v2v_tool.alternateCopyPaste))
                    with pm.horizontalLayout(ratios=[2, 6]):# , ann='最初に選択したvtxのWeightに全てをペーストします'):
                        pm.text(l='最初の頂点に合わせる : ', al='right')
                        pm.button(l='CopyPaste', c=pm.Callback(self.cop_v2v_tool.pasteFirstSelVtx))
            with pm.frameLayout(l='Weight値のCopyPaste （ メッシュから頂点 ）', cll=True, bgc=self.frame_col) as fl_m2v:
                with pm.formLayout() as self.fl2:
                    tx1 = pm.text(l='-' * 40 + ' 【 新規CopyPaste 】 ' + '-' * 40)
                    with pm.columnLayout(adj=True) as cl:
                        with pm.horizontalLayout(ratios=[2, 3, 1]):
                            pm.text(l='コピー元メッシュ : ', al='right')
                            self.tf_copy_mesh = pm.textField(ed=False)
                            pm.button(l='<< set', c=pm.Callback(self._setSource))
                        with pm.horizontalLayout(ratios=[2, 3, 1]):
                            pm.text(l='対象の頂点 : ', al='right')
                            self.tf_paste_vtxs = pm.textField(ed=False)
                            pm.button(l='<< set', c=pm.Callback(self._setTarget))
                        self.op_ia1 = self.pulldown(1)
                        self.op_ia2 = self.pulldown(2)
                        self.op_ia3 = self.pulldown(3)
                        with pm.horizontalLayout(ratios=[1, 2]):
                            pm.text(l='')
                            self.cb_bind = pm.checkBox(l='足りないインフルエンスを強制的にバインド', v=True)
                        with pm.horizontalLayout():
                            pm.text(l='')
                            self.cb_add_history = pm.checkBox(l='履歴に追加する', v=True)
                            pm.button(l='CopyPaste　実行', c=pm.Callback(self._copyPaste), bgc=self.bt_cop_col)
                    tx2 = pm.text(l='-' * 47 + ' 【 履歴 】 ' + '-' * 47)
                    with pm.horizontalLayout() as hl_history:
                        self.cb_ia = pm.checkBox(l='influenceAssociation を履歴から適用')
                        self.bt_norm = pm.button(l='履歴を整理', c=pm.Callback(self._normHistory))
                    self.sl_his = pm.scrollLayout(cr=True)

                pm.formLayout(self.fl2, e=True, af=[(tx1, 'top', 0), (tx1, 'left', self.s_ofet), (tx1, 'right', self.s_ofet)])
                pm.formLayout(self.fl2, e=True, af=[(cl, 'top', 20), (cl, 'left', self.s_ofet), (cl, 'right', self.s_ofet)])
                pm.formLayout(self.fl2, e=True, af=[(tx2, 'top', 205), (tx2, 'left', self.s_ofet), (tx2, 'right', self.s_ofet)])
                pm.formLayout(self.fl2, e=True, af=[(hl_history, 'top', 220), (hl_history, 'left', self.s_ofet + 4), (hl_history, 'right', self.s_ofet)])

        pm.formLayout(fl, e=True, af=[(fl_v2v, 'top', 0), (fl_v2v, 'left', self.s_ofet), (fl_v2v, 'right', self.s_ofet)])
        pm.formLayout(fl, e=True, af=[(fl_m2v, 'top', 120), (fl_m2v, 'left', self.s_ofet), (fl_m2v, 'right', self.s_ofet), (fl_m2v, 'bottom', self.s_ofet)])

        # ---------------------------------
        pm.scriptJob(p=self.window_name, e=['SceneOpened', pm.Callback(self._updateUi)])
        pm.scriptJob(p=self.window_name, e=['SelectionChanged', pm.Callback(self._highLightButton)])
        pm.showWindow(self.window_name)
        self._updateUi()

    def _updateUi(self):
        # pm.evalDeferred(pm.Callback(pm.deleteUI(self.sl_his)))

        # 設定ファイルから復元
        cmds.optionMenuGrp(self.op_ia1, e=True, value=self.setting.get('op_ia1', 'Closest joint'))
        cmds.optionMenuGrp(self.op_ia2, e=True, value=self.setting.get('op_ia2', 'Label'))
        cmds.optionMenuGrp(self.op_ia3, e=True, value=self.setting.get('op_ia3', 'None'))
        pm.checkBox(self.cb_bind, e=True, v=self.setting.get('cb_bind', True))
        pm.checkBox(self.cb_add_history, e=True, v=self.setting.get('cb_add_history', True))
        pm.checkBox(self.cb_ia, e=True, v=self.setting.get('cb_ia', False))

        # ---------------------------------
        pm.deleteUI(self.sl_his)
        pm.setParent(self.fl2)
        self.sl_his = pm.scrollLayout(cr=True)
        pm.formLayout(
            self.fl2, e=True,
            af=[
                (self.sl_his, 'top', 250),
                (self.sl_his, 'left', self.s_ofet),
                (self.sl_his, 'right', self.s_ofet),
                (self.sl_his, 'bottom', self.s_ofet)
            ]
        )

        # ---------------------------------
        self._updateHistoryList()
        self.bt_list = []
        self.bt_list2 = []
        for i in range(len(self.history_at_list)):
            bt, bt2 = self._addHistoryUi(i + 1)
            self.bt_list.append(bt)
            self.bt_list2.append(bt2)

    def _highLightButton(self):
        selnode = cmds.ls(sl=True, type='transform')
        for bt2 in self.bt_list2:
            cmds.button(bt2, e=True, bgc=self.bt_col)
            if selnode:
                if cmds.button(bt2, q=True, l=True) == selnode[0]:
                    cmds.button(bt2, e=True, bgc=self.bt_cop_col)

    def _updateHistoryList(self):
        self.history_at_list = []
        if pm.objExists(self.wb):
            for at in pm.listAttr(self.wb, ud=True):
                if self.attr_name in at:
                    self.history_at_list.append(at)

        # アトリビュートの末尾番号を順番に揃える
        tmp_list = []
        for i in range(len(self.history_at_list)):
            tmp_list.append(pm.renameAttr(self.wb + '.' + self.history_at_list[i], self.attr_name + str((i + 1) * 10000)))
        for i in range(len(tmp_list)):
            self.history_at_list[i] = pm.renameAttr(self.wb + '.' + tmp_list[i], self.attr_name + str(i + 1))

    def _normHistory(self):
        history_at_list_tmp = []
        for i in range(len(self.history_at_list)):
            mesh_node, paste_mesh, vtxs, label, _ = self._getHistorySettings(i + 1)
            vtxs = pcm.str2List(vtxs)
            try:
                pm.select(mesh_node)
                pm.select(vtxs)
                history_at_list_tmp.append([mesh_node, paste_mesh, vtxs, label, _])
            except:
                pm.deleteAttr(self.wb + '.' + self.history_at_list[i])
                print('Delete: ', self.wb + '.' + self.history_at_list[i], mesh_node, paste_mesh, vtxs, label, _)

        self._updateUi()

    def pulldown(self, num):
        with pm.horizontalLayout(ratios=[1, 2]):
            cmds.text(l='Influence Association {0}: '.format(num))
            op = cmds.optionMenuGrp()
            if num != 1:
                cmds.menuItem(l='None')
            cmds.menuItem(l='Closest joint')
            cmds.menuItem(l='Closest bone')
            cmds.menuItem(l='One to one')
            cmds.menuItem(l='Label')
            cmds.menuItem(l='Name')
            cmds.optionMenuGrp(op, e=True)
        return op

    def _setSource(self):
        self.mesh_node = ''
        self.tf_copy_mesh.setText('')

        self.cop_tool._setMeshNodeFromSel()
        if self.cop_tool.mesh_node:
            self.tf_copy_mesh.setText(self.cop_tool.mesh_node)

    def _setTarget(self):
        self.vtxs = []
        self.tf_paste_vtxs.setText('')

        self.cop_tool._setVtxsFromSel()
        if self.cop_tool.vtxs:
            vtxs_text = self._convetVtxsTextforUi()
            self.tf_paste_vtxs.setText(vtxs_text)

    def _getInfluenceAssociationSettingFromUi(self):
        setting = []
        op1 = cmds.optionMenuGrp(self.op_ia1, q=True, v=True)
        if op1 != 'None':
            setting.append(self.infl_assoc_dict[op1])
        op2 = cmds.optionMenuGrp(self.op_ia2, q=True, v=True)
        if op2 != 'None':
            setting.append(self.infl_assoc_dict[op2])
        op3 = cmds.optionMenuGrp(self.op_ia3, q=True, v=True)
        if op3 != 'None':
            setting.append(self.infl_assoc_dict[op3])
        return setting

    def _saveInfluenceAssociationSetting(self, influenceAssociation_):
        self.setting.set('op_ia1', pcm.getKeyFormValDict(self.infl_assoc_dict, influenceAssociation_[0]))
        try:
            self.setting.set('op_ia2', pcm.getKeyFormValDict(self.infl_assoc_dict, influenceAssociation_[1]))
        except:
            pass
        try:
            self.setting.set('op_ia3', pcm.getKeyFormValDict(self.infl_assoc_dict, influenceAssociation_[2]))
        except:
            pass

    def _copyPaste(self):
        if self.cop_tool.mesh_node and self.cop_tool.vtxs:
            self.cop_tool.influenceAssociation = self._getInfluenceAssociationSettingFromUi()
            self.cop_tool.force_bind = self.cb_bind.getValue()
            self.cop_tool.paste()
            if self.cb_add_history.getValue():
                self._addHistory()
            self._saveInfluenceAssociationSetting(self.cop_tool.influenceAssociation)
            self.setting.set('cb_bind', self.cb_bind.getValue())
            self.setting.set('cb_add_history', self.cb_add_history.getValue())
        else:
            pm.warning('Source or Target が登録されていません')

    def _convetVtxsTextforUi(self):
        _text = self.cop_tool.paste_mesh + ' : '
        for vtx in self.cop_tool.vtxs:
            tmp = vtx.split('[')
            _text += tmp[1][:-1] + ', '
        return _text

    def _addHistory(self):
        if not pm.objExists(self.wb):
            pm.group(em=True, n=self.wb)

        new_historys = [
            self.cop_tool.mesh_node,
            self.cop_tool.paste_mesh,
            self.cop_tool.vtxs,
            '',
            self.cop_tool.influenceAssociation
        ]
        his_num = len(self.history_at_list) + 1
        self.history_at_list.append(self.attr_name + str(his_num))
        cm.addAt(self.wb, self.attr_name + str(his_num), new_historys)
        bt, bt2 = self._addHistoryUi(his_num)
        self.bt_list.append(bt)
        self.bt_list2.append(bt2)

    def _getHistorySettings(self, history_number):
        his_vals = pm.getAttr(self.wb + '.' + self.attr_name + str(history_number))
        influenceAssociation_ = 'oneToOne'
        mesh_node, paste_mesh, vtxs, label = his_vals[0:4]
        if len(his_vals) == 5:
            influenceAssociation_ = pcm.str2List(his_vals[4])
        return mesh_node, paste_mesh, vtxs, label, influenceAssociation_

    def _addHistoryUi(self, history_number):
        mesh_node, paste_mesh, vtxs, label, _ = self._getHistorySettings(history_number)
        pm.setParent(self.sl_his)
        vtxs = pcm.str2List(vtxs)
        with pm.horizontalLayout(ratios=[1, 3, 3, 3, 2, 1]) as hl:
            bt = pm.button(l=str(history_number), ann='meshとvtxを選択します', bgc=self.bt_col)
            pm.button(bt, e=True, c=pm.Callback(self._select, bt, [mesh_node, vtxs]))
            pm.textField(
                self.tf_label + str(history_number), tx=label, ann='履歴にラベルを付けます',
                cc=pm.Callback(self._editLabel, history_number))
            bt2 = pm.button(
                l=mesh_node, ann='meshのみを選択します',
                c=pm.Callback(self._select, bt, [mesh_node]), bgc=self.bt_col)
            pm.button(
                l=paste_mesh, ann='vtxのみを選択します',
                c=pm.Callback(self._select, bt, [vtxs]), bgc=self.bt_col)
            pm.iconTextButton(
                i='polyCopyUV.png', st='iconOnly', bgc=self.bt_cop_col,
                c=pm.Callback(self._copyPasteFromHistory, history_number))
            pm.iconTextButton(
                i='deleteClip.png', st='iconOnly', bgc=self.bt_col,
                c=pm.Callback(self._deleteUi, history_number))

        pm.layout(hl, e=True, ann=str(_))
        return bt, bt2

    def _editLabel(self, history_number):
        mesh_node, paste_mesh, vtxs, label, _ = self._getHistorySettings(history_number)
        new_label = pm.textField(self.tf_label + str(history_number), q=True, tx=True)
        new_historys = [mesh_node, paste_mesh, vtxs, new_label]
        pm.setAttr(self.wb + '.' + self.attr_name + str(history_number), new_historys)

    def _copyPasteFromHistory(self, history_number):
        mesh_node, paste_mesh, vtxs, _, influenceAssociation_ = self._getHistorySettings(history_number)
        use_ia_history = pm.checkBox(self.cb_ia, q=True, v=True)
        if not use_ia_history:
            influenceAssociation_ = self._getInfluenceAssociationSettingFromUi()
        self.cop_tool_history.mesh_node = mesh_node
        self.cop_tool_history.vtxs = pcm.str2List(vtxs)
        self.cop_tool_history.paste_mesh = paste_mesh
        self.cop_tool_history.influenceAssociation = influenceAssociation_
        self.cop_tool_history.paste()

        if not use_ia_history:
            self._saveInfluenceAssociationSetting(influenceAssociation_)

        self.setting.set('cb_ia', use_ia_history)

    def _select(self, current_bt, nodes):
        pm.select(nodes)
        for bt in self.bt_list:
            if bt != current_bt:
                pm.button(bt, e=True, bgc=[0.267, 0.267, 0.267])
            else:
                pm.button(bt, e=True, bgc=[0.267, 0.6, 0.267])
        print(nodes)

    def _deleteUi(self, history_number):
        target_at = self.wb + '.' + self.attr_name + str(history_number)
        pm.deleteAttr(target_at)
        self._updateUi()


def main():
    WeightCopyToVtx().initUi()
