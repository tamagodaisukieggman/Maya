# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : updateModelToolUi
# Author  : toi
# Version : 0.0.2
# Update  : 2022/08/29
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import re
from functools import partial

import maya.cmds as cmds
import maya.mel as mm
from . import updateModelTool as umt
from dccUserMayaSharePythonLib import tsubasa_dumspl as tsubasa
from dccUserMayaSharePythonLib import ui
from dccUserMayaSharePythonLib import file_dumspl as f
from dccUserMayaSharePythonLib import common as cm


class UpdateModelToolUi(object):
    def __init__(self):
        self.window_name = 'updateModelToolUi'
        self.versionup_work_scene_name = None
        self.bt_list = []

        self.tf_ws = 'tf_workscene_umtu'
        self.tf_nm = 'tf_nwemodel_umtu'

        self.setting_dict = f.createSettingFile('updateModelToolUi')
        self.multiple_filters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"

    def bt(self, label_, func):
        return ui.qtbutton(l='* ' + label_, c=func, size=16, align='left')

    def setBtCol(self, bt, col):
        style_sheet = bt.styleSheet()
        style_sheet = style_sheet[:-1] + 'background-color: {0};'.format(col) + '}'
        bt.setStyleSheet(style_sheet)
        cmds.refresh()

    def init_ui(self):
        if cmds.window(self.window_name, ex=True):
            cmds.deleteUI(self.window_name)
        cmds.window(self.window_name, t='UpdateModelTool', w=400, mb=True)

        cmds.menu(l='Option')
        cmds.menuItem(l='Reference previous version (connect joint)', c=partial(self.setReference))
        cmds.menuItem(l='Reference specify scene (connect joint)', c=partial(self.setReferenceSpecify))
        cmds.menuItem(l='Load idle motion', c=partial(self.loadIdleMotion))
        cmds.menuItem(l='import method', d=True)
        cmds.radioMenuItemCollection()
        self.mi_list = []
        self.mi_list.append(cmds.menuItem(rb=True, l='index', docTag=0))
        self.mi_list.append(cmds.menuItem(rb=False, l='nearest', docTag=1))
        self.mi_list.append(cmds.menuItem(rb=False, l='barycentric', docTag=2))
        self.mi_list.append(cmds.menuItem(rb=False, l='bilinear', docTag=3))
        self.mi_list.append(cmds.menuItem(rb=False, l='over', docTag=4))

        cmds.menu(l='Help')
        cmds.menuItem(l='Tool help', c="os.startfile('https://wisdom.cygames.jp/x/ijoBGw')")

        cmds.columnLayout(adj=True, co=['both', 3], rs=2)
        cmds.separator(h=10)

        cmds.text('<big><b>[ Work Scene ]', al='left')
        cmds.rowLayout(nc=2, adj=True)
        cmds.popupMenu(b=3)
        cmds.menuItem(
            l='Set current scene path', ann='現在のシーンパスをセットします',
            c=partial(self._setCurrentScene))
        cmds.textField(self.tf_ws, placeholderText='作業シーンのパスをセット', tcc=self.setVersionupWorkScenePath)
        cmds.iconTextButton(i='SP_DirClosedIcon.png', st='iconOnly', c=partial(self.setPath, self.tf_ws))

        cmds.setParent('..')
        self.bt_list.append(self.bt('Load', partial(self.loadScene, self.tf_ws, True)))
        self.bt_list.append(self.bt('Export Weight', umt.exportWeight))
        self.bt_list.append(self.bt('Save Sets', umt.saveSets))
        self.bt_list.append(self.bt('CleanUp', umt.cleanUpWorkScene))
        self.bt_list.append(self.bt('Save Count up', self.startSaveCountUp))

        cmds.separator(h=10)
        cmds.text('<big><b>[ New Model Scene ]', al='left')
        cmds.rowLayout(nc=2, adj=True)
        cmds.popupMenu(b=3)
        cmds.menuItem(
            l='Set current chara model scene', ann='現在のキャラのp4vのmodelパスをセットします',
            c=partial(self._setCurrentCharaModelPath))
        cmds.textField(self.tf_nm, placeholderText='新モデルシーンのパス')
        cmds.iconTextButton(i='SP_DirClosedIcon.png', st='iconOnly', c=partial(self.setPath, self.tf_nm))

        cmds.setParent('..')
        self.bt_list.append(self.bt('Load', partial(self.loadScene, self.tf_nm, False)))
        self.bt_list.append(self.bt('CleanUp', umt.cleanUpAll))
        self.bt_list.append(self.bt('Merge Work Scene', self.startImportWorkScene))
        self.bt_list.append(self.bt('Import Weight', self.startImportWeight))
        self.bt_list.append(self.bt('Load Sets', umt.loadSets))
        self.bt_list.append(self.bt('Save Scene to Work Scene', self.startSave2WorkScene))

        cmds.separator(h=10)
        ui.qtbutton('Run All', c=self.do_all, size=16)
        cmds.showWindow(self.window_name)

        self.loadScenePath(self.tf_ws)
        self.loadScenePath(self.tf_nm)
        self.resetButtonColor()

    def resetButtonColor(self):
        for i in range(11):
            self.setBtCol(self.bt_list[i], 'dimgray')

    def loadScenePath(self, tf):
        tf_path = self.setting_dict.get(tf)
        if tf_path:
            cmds.textField(tf, e=True, tx=tf_path)

    def _setCurrentScene(self, *args):
        current = cmds.file(q=True, sn=True)
        cmds.textField(self.tf_ws, e=True, tx=current)

    def _setCurrentCharaModelPath(self, *args):
        id_ = tsubasa._getIdFromRoot()
        path_ = tsubasa.getCharaWorkPathFromId(id_) + 'model/maya/scenes/{}.mb'.format(id_)
        cmds.textField(self.tf_nm, e=True, tx=path_)
        self.setting_dict.set(self.tf_nm, path_)

    def setVersionupWorkScenePath(self, *args):
        path_ = cmds.textField(self.tf_ws, q=True, tx=True)
        self.versionup_work_scene_name = umt.getVersionUpSceneName(path_)
        self.setting_dict.set(self.tf_ws, path_)

    def setPath(self, tf):
        def_dir = ''
        current_path = cmds.textField(tf, q=True, tx=True)
        if os.path.isfile(current_path):
            def_dir = os.path.dirname(current_path)
        result = cmds.fileDialog2(fileFilter=self.multiple_filters, dialogStyle=2, fileMode=1, dir=def_dir)
        if result is not None:
            path_ = result[0]
            cmds.textField(tf, e=True, tx=path_)

            self.setting_dict.set(tf, path_)

    def startSaveCountUp(self, *args):
        umt.saveCountUp(self.versionup_work_scene_name)

    def loadScene(self, *args):
        tf = args[0]
        set_new_model_scene_path = args[1]

        load_path = cmds.textField(tf, q=True, tx=True)
        if os.path.isfile(load_path):
            cmds.file(load_path, o=True, f=True)

            if set_new_model_scene_path:
                id_ = tsubasa.getId(load_path)
                model_path = tsubasa.getCharaWorkPathFromId(id_)
                model_path = os.path.join(model_path, 'model', 'maya', 'scenes', id_ + '.mb')
                cmds.textField(self.tf_nm, e=True, tx=model_path)
                self.setVersionupWorkScenePath()

    def startImportWorkScene(self, *args):
        umt.importWorkScene(self.versionup_work_scene_name)

    def getImportMethodMode(self):
        mode = 0
        for mi in self.mi_list:
            if cmds.menuItem(mi, q=True, rb=True):
                mode = cmds.menuItem(mi, q=True, docTag=True)
        return mode

    def startImportWeight(self, *args):
        import_mode = self.getImportMethodMode()
        umt.importWeight(import_mode)

    def startSave2WorkScene(self, *args):
        cmds.file(rename=self.versionup_work_scene_name)
        cmds.file(s=True, f=True)
        mel_cmd = 'addRecentFile("{}", "mayaBinary")'.format(self.versionup_work_scene_name.replace(os.sep, '/'))
        mm.eval(mel_cmd)

    def confirm(self, message, icn):
        cmds.confirmDialog(
            b='OK', title='Confirm', message=message, icn=icn, p=self.window_name)

    def do_all(self, *args):
        def endProcess(message, icon_type):
            self.confirm(message, icon_type)
            self.resetButtonColor()

        col = '#4169e1'
        #try:
        self.loadScene(self.tf_ws, False)
        self.setBtCol(self.bt_list[0], col)

        umt.exportWeight()
        self.setBtCol(self.bt_list[1], col)

        umt.saveSets()
        self.setBtCol(self.bt_list[2], col)

        umt.cleanUpWorkScene()
        self.setBtCol(self.bt_list[3], col)

        self.startSaveCountUp()
        self.setBtCol(self.bt_list[4], col)

        self.loadScene(self.tf_nm, False)
        self.setBtCol(self.bt_list[5], col)

        umt.cleanUpAll()
        self.setBtCol(self.bt_list[6], col)

        self.startImportWorkScene()
        self.setBtCol(self.bt_list[7], col)

        self.startImportWeight()
        self.setBtCol(self.bt_list[8], col)

        umt.loadSets()
        self.setBtCol(self.bt_list[9], col)

        self.startSave2WorkScene()
        self.setBtCol(self.bt_list[10], col)

        cmds.evalDeferred(partial(endProcess, 'Finish !', 'information'))
        #except:
        #    cmds.evalDeferred(partial(endProcess, 'Failure...', 'critical'))

    def setReference(self, *args):
        scene_path = cmds.file(q=True, sn=True)
        scene_file_name = os.path.basename(scene_path)
        split_file = scene_file_name.split('_')
        if re.match('\w\d\d\d', split_file[1]):
            version = str(int(split_file[1][1:]) - 1).zfill(3)
            ns = 'v' + version

            current_dir_files = os.listdir(os.path.dirname(scene_path))
            for scene_file in current_dir_files:
                if not scene_file.endswith('.ma') and not scene_file.endswith('.mb'):
                    continue

                if version in scene_file:
                    previous_scene = os.path.join(os.path.dirname(scene_path), scene_file)
                    self.setConnectOtherScene(previous_scene, ns)

    def setReferenceSpecify(self, *args):
        result = cmds.fileDialog2(fileFilter=self.multiple_filters, dialogStyle=2, fileMode=1)
        if result is not None:
            path_ = result[0]
            self.setConnectOtherScene(path_, 'compare')

    def setConnectOtherScene(self, other_scene_path, ns):
        if cmds.file(other_scene_path, reference=True, ns=ns):

            # const
            cm.sameNameNodeSelect('null', ns + ':null')
            sels = cmds.ls(sl=True)
            for i in range(len(sels)):
                if i < len(sels) - 1:
                    if i % 2 == 0:
                        cmds.cutKey(sels[i + 1])
                        if sels[i].startswith('_a'):
                            continue

                        try:
                            if 'null' in sels[i] or '_000' in sels[i]:
                                cmds.pointConstraint(sels[i], sels[i + 1])
                            cmds.orientConstraint(sels[i], sels[i + 1])
                        except:
                            pass

            # set color
            nodes = cmds.ls(ns + ':LOD0', dag=True)
            result = []
            for node in nodes:
                shape = cmds.listRelatives(node, shapes=True)
                if shape:
                    result.append(node)

            if result:
                for node in result:
                    cmds.setAttr(node + '.useOutlinerColor', True)
                    cmds.setAttr(node + '.outlinerColor', *[1, 0.43, 0.43])
                    cmds.setAttr(node + '.overrideEnabled', True)
                    cmds.setAttr(node + '.overrideColor', 20)

                    shape = cmds.listRelatives(node, shapes=True)
                    if shape:
                        for s in shape:
                            cmds.setAttr(s + '.overrideEnabled', True)
                            cmds.setAttr(s + '.overrideColor', 18)

            cmds.setAttr(ns + ':null.v', False)

    def loadIdleMotion(self, *args):
        _motion = 'D:/cygames/tsubasa/tools/dcc_user/maya/share/python/baseBodyGuide/_data/_motion/_mb/_motion_idle.mb'
        imp_nodes = cmds.file(_motion, i=True, ns='idle', returnNewNodes=True)
        for top in cmds.ls(imp_nodes, assemblies=True):
            cmds.setAttr(top + '.v', False)

        cmds.evalDeferred(self._setSouece)

    def _setSouece(self):
        cmds.currentTime(10, e=True)
        cm.changeHIKSource('_default_character', 'idle:_default_character')
        anim_curves = cm.getAnimCurves()
        cmds.select(anim_curves)
        cmds.evalDeferred('cmds.playbackOptions(e=True, maxTime=1000)')
        cm.hum('finish !')


def main():
    UpdateModelToolUi().init_ui()
