# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : weightGradation
# Author  : toi
# Version : 0.0.3
# Update  : 2021/11/22
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
from dccUserMayaSharePythonLib import ui
from dccUserMayaSharePythonLib import skinning as sk
from dccUserMayaSharePythonLib import file_dumspl as f



class WeightGradation(object):
    def __init__(self):
        self.window_name = os.path.basename(os.path.dirname(__file__))

        #段階関連変数
        self.counter = 0
        self.vtxs_dict = {}
        self.before_vtxs_dict = {}

        #距離関連変数
        self.sel_vtx_distance = []

        #UI
        self.bt_col = [0.1, 0.2, 0.4]

        #設定ファイル
        self.SETTING_DIR = os.path.join(
            os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"),
            'Documents', 'maya', 'Scripting_Files', 'weightGradation', 'data')
        self.SETTING_JSON = os.path.join(self.SETTING_DIR, 'weightGradation.json')
        if not os.path.isfile(self.SETTING_JSON):
            f.exportJson(self.SETTING_JSON)
        self.setting = f.JsonDict(self.SETTING_JSON)


    def delOverwrapWindow(self):
        if cmds.window(self.window_name, ex=True):
            pm.deleteUI(self.window_name)

    def initUi(self):
        self.delOverwrapWindow()

        win = pm.window(self.window_name, t=self.window_name, w=400, mb=True)
        pm.menu(l='Help')
        pm.menuItem(l='Tool help', c=pm.Callback(os.startfile, 'https://wisdom.cygames.jp/x/M-HbEw'))

        cl_top = pm.columnLayout(adj=True, co=['both', 5])
        pm.separator(h=10)
        with pm.horizontalLayout(ratios=[3, 1]):
            pm.text(l='')
            pm.button(l='UIリセット', c=pm.Callback(pm.evalDeferred, main))
        pm.separator(h=10)
        with pm.horizontalLayout(ratios=[4, 2, 1, 1]):
            pm.text(l='influenceジョイント')
            self.tf_inf_joint = pm.textField(tx=self.setting.get('kInfjoint', ''))
            pm.button(l='<< set', c=pm.Callback(self._setInfJoint), bgc=self.bt_col)
            pm.button(l='select', c=pm.Callback(self._select, 1))
        with pm.horizontalLayout(ratios=[4, 2, 1, 1]):
            pm.text(l='mesh')
            self.tf_mesh = pm.textField(ed=False)
            pm.text(l='')
            pm.button(l='select', c=pm.Callback(self._select, 2))
        with pm.horizontalLayout(ratios=[4, 2, 1, 1]):
            pm.text(l='skinCluster')
            self.tf_sc = pm.textField(ed=False)
            pm.text(l='')
            pm.button(l='select', c=pm.Callback(self._select, 3))
        pm.separator(h=10)

        self.tab = pm.tabLayout()

        #---------------------------------
        cl_step = pm.columnLayout(adj=True)
        pm.separator()
        with pm.horizontalLayout(ratios=[6, 2]) as hl:
            pm.button(l='頂点選択拡大 >', c=pm.Callback(self._traverse), bgc=self.bt_col)
            pm.button(l='< 戻る', c=pm.Callback(self._back))
        pm.separator()
        self.cl_step_inner = pm.columnLayout(adj=True)
        pm.setParent('..')
        pm.separator()
        with pm.rowLayout(nc=2, adj=True):
            #pm.button(l='頂点全選択', c=pm.Callback(self._selAllVtxs))
            #pm.radioCollection()
            #self.rb_avg = pm.radioButton(l='均等', sl=True, onCommand=pm.Callback(self._adjustWeightAll))
            #pm.radioButton(l='距離', onCommand=pm.Callback(self._adjustWeightAll))
            pm.text(l='最大値')
            self.fs_adjust_max = pm.floatSlider(min=0, max=1, v=1, dc=pm.Callback(self._adjustWeightAll), w=300)
        with pm.rowLayout(nc=2, adj=True):
            pm.text(l='最小値')
            self.fs_adjust_mim = pm.floatSlider(min=0, max=1, v=0, dc=pm.Callback(self._adjustWeightAll), w=300)

        #---------------------------------
        pm.setParent('..')
        cl_distance = pm.columnLayout('cl_distance', adj=True)
        with pm.horizontalLayout(ratios=[4, 2, 1, 1]):
            pm.text(l='基準vtx')
            self.tf_base = pm.textField(tx=self.setting.get('kBaseVtx', ''))
            pm.button(l='<< set', c=pm.Callback(self._setBaseVtxs), bgc=self.bt_col)
            pm.button(l='select', c=pm.Callback(self._select, 4))
        with pm.horizontalLayout():
            pm.text('最大値')
            self.fs_adjust_max2 = pm.floatSlider(min=0, max=1, v=1)
        with pm.horizontalLayout():
            pm.text('最小値')
            self.fs_adjust_mim2 = pm.floatSlider(min=0, max=1)
        pm.separator()
        with pm.horizontalLayout():
            pm.text('')
            pm.button(l='前回のvtx選択復元', c=pm.Callback(self._restoreSelectionVtx))

        pm.setParent(cl_top)
        pm.button(l='Weight 適用', c=pm.Callback(self.main), h=40, bgc=self.bt_col)


        pm.tabLayout(self.tab, e=True, tabLabel=((cl_step, '段階'), (cl_distance, '距離')))
        win.show()

    def _getSetMeshAndSkinCluster(self):
        mesh_text = self.tf_mesh.getText()
        if not mesh_text:
            mesh = sk.getMeshNameFromSelVtx()
            self.tf_mesh.setText(mesh)
        else:
            mesh = mesh_text

        skc_text = self.tf_sc.getText()
        if not skc_text:
            skc = sk.listRelatedSkinClusters([mesh])
            if not skc:
                return

            skc = sk.listRelatedSkinClusters([mesh])[0].name()
            self.tf_sc.setText(skc)

    ##---------------------------------------------------------------------------------
    ##段階
    ##---------------------------------------------------------------------------------
    def _setVtxLineUi(self, current_vtxs):
        pm.setParent(self.cl_step_inner)
        with pm.rowLayout(self._rlVtxLineName(self.counter), nc=2, adj=True):
            #with pm.rowLayout(nc=2):
            pm.button(l=str(self.counter), c=pm.Callback(self._selVtx, self.counter))
            pm.popupMenu(b=3)
            pm.menuItem(l='全頂点選択', c=pm.Callback(self._selAllVtxs))
            #	if len(current_vtxs) > 10:
            #		pm.text(l=str(current_vtxs[:10])[1:-1] + ' ...')
            #	else:
            #		pm.text(l=str(current_vtxs)[1:-1])
            pm.floatSlider(self._ffVtxLineName(self.counter), min=0, max=1, w=300)

    def _adjustWeightAll(self):
        adj_slider_val_max = self.fs_adjust_max.getValue()
        adj_slider_val_mim = self.fs_adjust_mim.getValue()
        dif = adj_slider_val_max - adj_slider_val_mim
        div_val = dif / self.counter
        #print(div_val)
        for i in range(1, self.counter + 1):
            #x = div_val * float(i) + adj_slider_val_mim# - (div_val * (1 / float(i)))
            #print(i, self._ffVtxLineName(self.counter - i))
            #print('    ', 1 / float(i), div_val * (1 / float(i)), x)
            set_val = 0
            if i == 1:
                set_val = adj_slider_val_mim
            elif i == self.counter:
                set_val = adj_slider_val_max
            else:
                #print(div_val * (1 / float(i)))
                set_val = div_val * i + adj_slider_val_mim - (div_val * (1 / float(i)))
            pm.floatSlider(self._ffVtxLineName(self.counter - i), e=True, v=set_val)
        #print('-' * 50)

    def _selVtx(self, count):
        #mesh = self.tf_mesh.getText()
        #sk.selectListingVtx(mesh, self.vtxs_dict[count])
        if pm.getModifiers() == 4:
            pm.select(self.vtxs_dict[count], toggle=True)
        else:
            pm.select(self.vtxs_dict[count])

    def _selAllVtxs(self):
        pm.select(cl=True)
        #mesh = self.tf_mesh.getText()
        for i in range(self.counter):
            #sk.selectListingVtx(mesh, self.vtxs_dict[i], True)
            pm.select(self.vtxs_dict[i], add=True)

    def _rlVtxLineName(self, count):
        return 'rl_vtx_line_' + str(count)

    def _ffVtxLineName(self, count):
        return 'ff_vtx_line_' + str(count)

    def _setInfJoint(self):
        sel = cmds.ls(sl=True, type='joint')
        if sel:
            pm.textField(self.tf_inf_joint, e=True, tx=sel[0])
            self.setting.set('kInfjoint', sel[0])
        else:
            pm.textField(self.tf_inf_joint, e=True, tx='')
            self.setting.set('kInfjoint', '')
            pm.warning('jointを選択してください')

    def _traverse(self):
        if self.counter:
            self._selAllVtxs()
        sel = cmds.ls(sl=True)
        if not sel:
            return

        self._getSetMeshAndSkinCluster()

        if self.counter:
            sk.polySelectTraverse()

        #sel = cmds.ls(sl=True)
        #vtxs = sk.listingVtxNumber(sel)
        vtxs = cmds.ls(sl=True, fl=True)
        current_vtxs = vtxs

        if self.counter:
            current_vtxs = sorted(pcm.negationList(vtxs, self.before_vtxs_dict[self.counter - 1]))

        self.vtxs_dict[self.counter] = current_vtxs
        self._setVtxLineUi(current_vtxs)

        self.before_vtxs_dict[self.counter] = vtxs
        self.counter += 1
        self._adjustWeightAll()

    def _back(self):
        self.counter -= 1
        pm.deleteUI(self._rlVtxLineName(self.counter))
        self._selAllVtxs()

    def _select(self, mode):
        if mode == 1:
            target_node = self.tf_inf_joint.getText()
        elif mode == 2:
            target_node = self.tf_mesh.getText()
        elif mode == 3:
            target_node = self.tf_sc.getText()
        elif mode == 4:
            target_node = self.tf_base.getText()

        if pm.objExists(target_node):
            pm.select(target_node)
        else:
            pm.warning('対象が存在しません')


    ##---------------------------------------------------------------------------------
    ##距離
    ##---------------------------------------------------------------------------------
    def _setBaseVtxs(self):
        vtxs = []
        sels = cmds.ls(sl=True, fl=True)
        if sels:
            vtxs = [x for x in sels if 'vtx[' in x]

        if vtxs:
            pm.textField(self.tf_base, e=True, tx=vtxs[0])
            self.setting.set('kBaseVtx', vtxs[0])
            self._getSetMeshAndSkinCluster()
        else:
            pm.textField(self.tf_base, e=True, tx='')
            self.setting.set('kBaseVtx', '')
            pm.warning('vertexを選択してください')

    def _restoreSelectionVtx(self):
        pm.select(self.sel_vtx_distance)


    ##---------------------------------------------------------------------------------
    def main(self):
        self._getSetMeshAndSkinCluster()

        mesh = self.tf_mesh.getText()
        skc = self.tf_sc.getText()
        inf_joint = self.tf_inf_joint.getText()
        if not inf_joint:
            pm.warning('influenceジョイントがsetされていません')
            return

        try:
            pm.skinCluster(skc, e=True, addInfluence=inf_joint,	weight=0)
        except:
            pass

        #段階
        if pm.tabLayout(self.tab, q=True, selectTabIndex=True) == 1:

            for i in range(self.counter):
                w_val = pm.floatSlider(self._ffVtxLineName(i), q=True, v=True)
                vtxs = self.vtxs_dict[i]
                #sk.selectListingVtx(mesh, vtxs)
                pm.select(vtxs)
                for vtx in vtxs:
                    pm.skinPercent(skc, transformValue=[(inf_joint, w_val)])

            pm.select(inf_joint)

        #距離
        else:
            sel_vtxs = cmds.ls(sl=True, fl=True)
            if not sel_vtxs:
                return
            else:
                sel_vtxs = [x for x in sel_vtxs if '.vtx[' in x]
                self.sel_vtx_distance = sel_vtxs

            base_vtx = pm.textField(self.tf_base, q=True, tx=True)
            print(sel_vtxs, base_vtx)

            adj_slider_val_max = self.fs_adjust_max2.getValue()
            adj_slider_val_mim = self.fs_adjust_mim2.getValue()
            dif = adj_slider_val_max - adj_slider_val_mim

            max_distance = 0
            distance_dict = {}
            for v in sel_vtxs:
                #print(v, base_vtx)
                current_vtx_distance = sk.distance2Coordinate(base_vtx, v)
                distance_dict[v] = current_vtx_distance
                if max_distance < current_vtx_distance:
                    max_distance = current_vtx_distance
            print(max_distance, dif, distance_dict)

            for v, distance in distance_dict.items():
                w_val = (1 - (distance / max_distance)) * dif + adj_slider_val_mim
                print(v, distance, 1 - (distance / max_distance), w_val)
                pm.select(v)
                pm.skinPercent(skc, transformValue=[(inf_joint, w_val)])

            pm.select(inf_joint)


def vtxFromMeshName(mesh, vtx_num):
    return '{0}.vtx[{1}]'.format(mesh, vtx_num)


def vtxsFromMeshName(mesh, vtx_num_list):
    result = []
    for vtx_num in vtx_num_list:
        result.append('{0}.vtx[{1}]'.format(mesh, vtx_num))
    return result


def main():
    WeightGradation().initUi()
