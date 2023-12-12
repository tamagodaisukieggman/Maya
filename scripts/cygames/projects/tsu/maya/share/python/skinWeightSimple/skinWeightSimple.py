# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : skinWeightSimple
# Author  : toi
# Version : 0.1.1
# Update  : 2022/9/13
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import pymel.core as pm
import os
import shutil
#import tsubasa.maya.tools.skinweight as skinweight

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

from dccUserMayaSharePythonLib import common as cm
from dccUserMayaSharePythonLib import tsubasa_dumspl as tbs
from dccUserMayaSharePythonLib import file_dumspl as f
#from dccUserMayaSharePythonLib import ui
from dccUserMayaSharePythonLib import skinning


class SkinWeightSimple(object):
    def __init__(self):
        self.window_name = os.path.basename(os.path.dirname(__file__))

        # 設定ファイル
        self.setting = f.createSettingFile('skinWeightSimple')
        self.weight_folder = os.path.join(f.getSettingFilePath('skinWeightSimple'), 'weight')
        if not os.path.isdir(self.weight_folder):
            os.makedirs(self.weight_folder)
        self.weight_folder_trash = os.path.join(f.getSettingFilePath('skinWeightSimple'), 'weight_trash')
        if not os.path.isdir(self.weight_folder_trash):
            os.makedirs(self.weight_folder_trash)

    '''
    def _getSwtTool(self):
        self.swt_window_name = 'skinweight_tool'
        skinweight.main()
        window = [x for x in pm.lsUI(windows=True) if x.name() == self.swt_window_name][0]
        #for x in inspect.getmembers(window, inspect.ismethod):
        #	print(x[0])
        window.setVisible(False)

        # skinweight_tool UIの取得
        textFields = ui.getMenbersContainedWindow(self.swt_window_name, 'textField')
        self.tf_dir = textFields[0]
        self.rb_index_name = 'import_index'
        self.rb_pos_name = 'import_closestpoint'
        self.rb_comp_name = 'import_closestpoint'
        self.rb_uv_name = 'import_uvspace'

        buttons = ui.getMenbersContainedWindow(self.swt_window_name, 'button')
        for b in buttons:
            if 'Export Weight (Multi)' in pm.button(b, q=True, l=True):
                self.bt_export = ui.mayaToPySide(b, QPushButton)
            elif 'Import Weight (Multi)' in pm.button(b, q=True, l=True):
                self.bt_import = ui.mayaToPySide(b, QPushButton)
    '''

    def delOverwrapWindow(self):
        if cmds.window(self.window_name, ex=True):
            pm.deleteUI(self.window_name)

    def _getId(self):
        scene_name = cmds.file(q=True, sn=True)
        id_ = tbs.getId(scene_name)
        if id_ is not None:
            return id_
        else:
            return scene_name

    def _initUI(self):
        self.delOverwrapWindow()
        win = pm.window(self.window_name, t=self.window_name, w=400, mb=True)
        pm.menu(l='Options')
        pm.menuItem(l='weightファイル置き場のtmpフォルダを開く', c=pm.Callback(self._openTmpFold))

        with pm.verticalLayout() as vl:
            with pm.horizontalLayout(ratios=[1, 0, 4]):
                with pm.verticalLayout():
                    pm.button(l='LOD以下 メッシュ選択', c=pm.Callback(self._selLODMesh))
                    pm.button(l='前回export メッシュ選択', c=pm.Callback(self._selLastMesh))
                pm.separator(horizontal=False, w=10)
                with pm.verticalLayout(ratios=[1, 0, 1]):
                    with pm.horizontalLayout(ratios=[1, 1, 1]):
                        self.cb_0f_ex = pm.checkBox(l='set 0f', v=True)
                        self.cb_unbind = pm.checkBox(l='unbind', v=True)
                        pm.button(l='Export', c=pm.Callback(self._export))
                    pm.separator()
                    with pm.horizontalLayout(ratios=[2, 1]):
                        with pm.verticalLayout():
                            with pm.horizontalLayout(ratios=[1, 2]):
                                self.cb_0f_im = pm.checkBox(l='set 0f', v=True)
                                pm.text(l='')
                            with pm.horizontalLayout(ratios=[1, 1, 1]):
                                pm.text(l='import method :')
                                pm.radioCollection()
                                self.rb_index = pm.radioButton(l='index', sl=True)
                                pm.radioButton(l='position')
                        pm.button(l='Import', c=pm.Callback(self._import))
        #vl.redistribute()
        win.show()

    '''
    def _setWeightFold(self):
        #meshs = pm.ls(sl=True)
        scene_path = cmds.file(q=True, sn=True)
        scene_dir = os.path.dirname(scene_path)
        weight_fold = os.path.join(scene_dir, 'weight')
        if not os.path.isdir(weight_fold):
            os.makedirs(weight_fold)
        return weight_fold
    '''

    def _selLODMesh(self):
        if pm.objExists('LOD0'):
            cm.selMeshHierarchy('LOD0')

    def _selLastMesh(self):
        #id = self._getId()
        #if id in self.setting._dict:
        #    pm.select(self.setting.get(id))
        cmds.select(self.setting.get('selected_nodes'))

    def _setTmpPath(self):
        weight_dir = self._setWeightFold()
        #pm.textField(self.tf_dir, e=True, tx=weight_fold)
        return weight_dir

    def _export(self):
        cm.hum()
        #self._getSwtTool()
        #export_dir = self._setTmpPath()

        sels = cmds.ls(sl=True)
        if not sels:
            cmds.warning('メッシュの選択がありません')
            return

        # ゴミ箱（weight_trash）を空に
        for wFt in os.listdir(self.weight_folder_trash):
            os.remove(os.path.join(self.weight_folder_trash, wFt))

        # 既存のファイルをゴミ箱（weight_trash）へ移動
        for wF in os.listdir(self.weight_folder):
            shutil.move(os.path.join(self.weight_folder, wF), self.weight_folder_trash)

        if self.cb_0f_ex.getValue():
            pm.currentTime(0, e=True)

        #self.bt_export.click()
        export_meshes, xml_files = skinning.exportWeightMulti(
            sels, self.weight_folder, self.cb_unbind.getValue())
        '''
        xml_files = []
        export_meshes = []
        for sel in sels:
            xml_path = skinning.exportWeight(sel, self.weight_folder)
            if xml_path is not None:
                xml_files.append(os.path.basename(xml_path))
                export_meshes.append(sel)
                cm.hum(sel)

                if self.cb_unbind.getValue():
                    #pm.mel.eval('doDetachSkin "2" { "3","0" };')
                    skinning.unbind(sel)
            else:
                print('no deformer {}'.format(sel))
        '''
        #id = self._getId()
        #self.setting.set(id, sels)
        #self.setting.set(id + '_xml', xml_files)
        self.setting.set('selected_nodes', export_meshes)
        self.setting.set('xml_files', xml_files)
        cm.hum('Export completed !')

    def _import(self):
        cm.hum()
        #self._getSwtTool()
        #import_dir = self._setTmpPath()

        sels = cmds.ls(sl=True)
        if not sels:
            cmds.warning('メッシュの選択がありません')
            return

        # ui値取得
        #pm.radioButton(self.rb_index_name, e=True, sl=True)
        if self.cb_0f_im.getValue():
            pm.currentTime(0, e=True)
        import_mode = 0 if pm.radioButton(self.rb_index, q=True, sl=True) else 2

        # xmlファイル名リスト取得
        xml_files = self.setting.get('xml_files')

        #self.bt_import.click()
        '''
        inful_joints = []
        for i in range(len(sels)):
            # xmlは生成順に適用する（異なるメッシュの場合はメッシュ名からファイル名を取得できない為）
            inful_joints += skinning.importWeight(sels[i], self.weight_folder, xml_files[i], mode=import_mode)
            cm.hum(sels[i])
        '''
        inful_joints = skinning.importWeightMulti(sels, self.weight_folder, xml_files, import_mode)
        cmds.select(sels)
        # cmds.select(inful_joints, add=True)
        cm.hum('Import completed !')

    def _openTmpFold(self):
        #weight_fold = self._setWeightFold()
        #if weight_fold is not None:
        os.startfile(self.weight_folder)

    '''
    def autoExportWeight():
        tsubasa.maya.tools.skinweighteditor.gui.main()
        swe = ui.getPySideWindow('Skin Weight Editor')
        swe.hide()

        """
        #スクリプトジョブを停止
        try:
            swe_sb = 0
            swe_sb = [x for x in cmds.scriptJob(listJobs=True) if 'SkinWeightEditor' in x]
            swe_sb = swe_sb[0].split(':')[0]
            if swe_sb:
                cmds.scriptJob(k=int(swe_sb))
        except:
            pass
        """

        les = swe.findChildren(QLineEdit)
        les[7].setText(str(round_))
        les[8].setText(str(prune_))
        les[9].setText(str(max_influence_))
        pbs = swe.findChildren(QPushButton)
        for pb in pbs:
            if pb.text() == 'Prune':
                cm.hum('Prune.....')
                pb.click()
        for pb in pbs:
            if pb.text() == 'Round':
                cm.hum('Round.....')
                pb.click()
            elif pb.text() == 'Max Influence':
                cm.hum('Max Influence.....')
                pb.click()

        #swe.close()

    def main(prune_=0.010, round_=3, max_influence_=4):
        cm.hum('Start normalize')
        sel = pm.ls(sl=True)
        if sel:
            nodes = pm.ls(sel[0], dag=True)
            result = []
            for node in nodes:
                try:
                    if node.getShape():
                        result.append(node)
                except:
                    pass
            pm.select(result)

            sel = pm.ls(sl=True)
            if sel:
                autoNormalize(prune_, round_, max_influence_)
                cm.hum('Finish !')
    '''


def main():
    SkinWeightSimple()._initUI()
