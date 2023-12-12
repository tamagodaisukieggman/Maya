# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : lodViewer
# Author  : toi
# Version : 0.0.3
# Update  : 2022/4/20
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import pymel.core as pm
import os
import random
from dccUserMayaSharePythonLib import common as cm
from dccUserMayaSharePythonLib import tsubasa_dumspl as tsubasa
from dccUserMayaSharePythonLib import file_dumspl as f
from convertTex2jpgForMB import convertTex2jpgForMB
#import baseBodyGuide.ui as bbgui


class LodViewer(object):
    def __init__(self):
        self.window_name = os.path.basename(os.path.dirname(__file__))

        #self.bbgui = bbgui.baseBodyGuideUI()
        self.ref_motion_dir = 'D:/cygames/tsubasa/tools/dcc_user/maya/share/python/baseBodyGuide/_data/_motion/_mb'
        self.ref_motion_ns = 'refMotion'

        self.col = (0.017, 0.136, 0.31)

        self.transform_dict = {}

        self._pose_update = True

        self._body_face_dict = {
            'pl': 'fp',
            'np': 'fn',
            'em': 'fe'
        }

        self.face_joints = ['null', '_003', '_004', '_005', '_a04']

        self.setting_dict = f.createSettingFile('lodViewer')

    def delOverwrapWindow(self):
        if cmds.window(self.window_name, ex=True):
            pm.deleteUI(self.window_name)

    def initUi(self):
        self.delOverwrapWindow()
        win = pm.window(self.window_name, t=self.window_name, w=400)
        with pm.frameLayout(l='Model Import  ( from Portal )', mw=2, mh=2, bgc=self.col):
            with pm.verticalLayout():
                with pm.horizontalLayout():
                    self.tx_id = pm.textField(tx='pl0000', cc=pm.Callback(self._changedID))
                    pm.button(l='Body', c=pm.Callback(self._importBody))
                with pm.horizontalLayout():
                    self.tx_id_face = pm.textField(ed=True)
                    pm.button(l='Face', c=pm.Callback(self._importFace))
                self.cb_imp_lod = pm.checkBox(l='Import LOD', v=True, cc=pm.Callback(self._changeImpCb))
        with pm.frameLayout(l='Settings', mw=2, mh=2, bgc=self.col):
            with pm.verticalLayout():
                pm.button(l='AssistDrive Import', c=pm.Callback(self._importAd))
                pm.button(l='Texture Convert', c=pm.Callback(convertTex2jpgForMB.toLambert))
                pm.button(l='Akamachi NPC Delete except a', c=pm.Callback(self._delExceptA))
        with pm.frameLayout(l='Motion Import', mw=2, mh=2, bgc=self.col):
            pm.text(l='Reference motion', al='left')
            with pm.horizontalLayout():
                pm.button(l='Idle motion', c=pm.Callback(self._idleMotion))
                pm.button(l='Chrck motion', c=pm.Callback(self._checkMotion))
            pm.text(l='Character motion ', al='left')
            pm.iconTextButton(
                l='Select motion  ( from Portal )', i='folder-open.png', st='iconAndTextHorizontal',
                c=pm.Callback(self._charaMotionImport), bgc=(0.387, 0.387, 0.387))
        with pm.frameLayout(l='Reset Pose', mw=2, mh=2, bgc=self.col):
            pm.iconTextButton(
                l='Reset', i='np-head.png', st='iconAndTextHorizontal',
                c=pm.Callback(self._reset), bgc=(0.387, 0.387, 0.387))
        with pm.frameLayout(l='LOD　Visible', mw=2, mh=2, bgc=self.col):
            self.cb_toggle = pm.checkBox(l='Toggle Mode', cc=pm.Callback(self._toggleChange))
            with pm.rowLayout(nc=7):
                for i in range(8):
                    try:
                        pm.checkBox(
                            'cb_lod_{0}'.format(i),
                            l=' {0} '.format(i),
                            cc=pm.Callback(self._changeAttr, i)
                        )
                    except:
                        pass
            with pm.rowLayout('rl_lod_vis', nc=2, adj=True):
                pm.button(l='Show all', c=pm.Callback(self._allShow, True))
                pm.button(l='Hide all', c=pm.Callback(self._allShow, False), w=120)
                #vl.redistribute()
        with pm.frameLayout(l='Joint　Visible', mw=2, mh=2, bgc=self.col):
            self.cb_all_joint = pm.checkBox(l='All joint', v=True, cc=pm.Callback(self._visNull))
            self.cb_second = pm.checkBox(l='Secondary joints', v=True, cc=pm.Callback(self._visScondary))
            self.cb_ad = pm.checkBox(l='AssistDrive joints', v=True, cc=pm.Callback(self._visAssistDrive))
            self.cb_jx = pm.checkBox(l='Joint Xray', v=False, cc=pm.Callback(self._visJointXray))
        with pm.frameLayout(l='Set Color', mw=2, mh=2, bgc=self.col):
            with pm.horizontalLayout(ratios=[6, 4]):
                pm.text(l='Wire frame color', al='left')
                self.cb_wire = pm.checkBox(l='Wire frame on', cc=pm.Callback(self.wireFrameOn))
            with pm.horizontalLayout():
                pm.button(l='', bgc=(0, 0, 0), c=pm.Callback(self._setColor, (0, 0, 0)))
                pm.button(l='', bgc=(0.8, 0, 0), c=pm.Callback(self._setColor, (0.8, 0, 0)))
                pm.button(l='', bgc=(0.8, 0.8, 0), c=pm.Callback(self._setColor, (0.8, 0.8, 0)))
                pm.button(l='', bgc=(0, 0.8, 0), c=pm.Callback(self._setColor, (0, 0.8, 0)))
                pm.button(l='', bgc=(0, 0.8, 0.8), c=pm.Callback(self._setColor, (0, 0.8, 0.8)))
                pm.button(l='', bgc=(0, 0, 0.8), c=pm.Callback(self._setColor, (0, 0, 0.8)))
                pm.button(l='', bgc=(0.8, 0, 0.8), c=pm.Callback(self._setColor, (0.8, 0, 0.8)))
                pm.button(l='', bgc=(0.8, 0.8, 0.8), c=pm.Callback(self._setColor, (0.8, 0.8, 0.8)))
            pm.text(l='Material color', al='left')
            with pm.horizontalLayout(ratios=[7, 3]):
                pm.button(l='Set random color', c=pm.Callback(self.randAssignMT))
                pm.button(l='Set all mesh', c=pm.Callback(self.randAssignMTAll))
        with pm.frameLayout(l='Offset', mw=2, mh=2, bgc=self.col):
            with pm.horizontalLayout(ratios=[7, 3]):
                self.fs = pm.floatSliderGrp(dc=pm.Callback(self._offset), max=1000)
                self.ff = pm.floatField(cc=pm.Callback(self._offset2))
        win.show()

        if self._pose_update:
            if pm.objExists('null'):
                joints = cmds.ls('null', dag=True)
                for j in joints:
                    if not j.startswith('_a'):
                        self.transform_dict[j] = cm.getTransform(j)

        pm.scriptJob(p=win, e=['SceneOpened', pm.Callback(self._updateUi)])
        pm.scriptJob(p=win, e=['PostSceneRead', pm.Callback(self._updateUi)])
        self._updateUi()

    def _updateUi(self):
        self.cb_imp_lod.setValue(self.setting_dict.get('cb_imp_lod_val'))
        if self.setting_dict.get('current_id', None) is not None:
            pm.textField(self.tx_id, e=True, tx=self.setting_dict.get('current_id'))
        self._changedID()

    def _changeImpCb(self):
        self.setting_dict.set('cb_imp_lod_val', self.cb_imp_lod.getValue())

    def _changedID(self):
        tx = pm.textField(self.tx_id, q=True, tx=True)
        id_ = None
        if tx[:2] in self._body_face_dict:
            id_ = self._body_face_dict[tx[:2]]
            self.setting_dict.set('current_id', tx)

        if id_ is not None:
            pm.textField(self.tx_id_face, e=True, tx=id_ + tx[2:])

    def _getFbxPath(self, kate, id, model_or_lod=0):
        m_or_l = 'lod' if model_or_lod else 'Model'
        _path = r'D:\project\PRJ_034\p1\assets\work\{0}\{1}\{2}\{1}.fbx'.format(kate, id, m_or_l)
        return _path

    def _importBody(self):
        self._changedID()
        body_id = pm.textField(self.tx_id, q=True, tx=True)
        kate = body_id[:2]
        _path = self._getFbxPath(kate, body_id, self.cb_imp_lod.getValue())
        if os.path.isfile(_path):
            self.cb_wire.setValue(True)
            cmds.file(_path, i=True, typ='FBX')
            cmds.evalDeferred(self.wireFrameOn)
            cmds.evalDeferred(cm.setJointXrayVis)

    def _importFace(self):
        face_id = pm.textField(self.tx_id_face, q=True, tx=True)
        kate = face_id[:2]
        _path = self._getFbxPath(kate, face_id, self.cb_imp_lod.getValue())
        if os.path.isfile(_path):
            self.cb_wire.setValue(True)
            if not cmds.namespace(ex='face'):
                cmds.namespace(add=':face')
            cmds.namespace(set='face')
            cmds.file(_path, ns='face', i=True, typ='FBX')
            cmds.namespace(set=':')

            for fj in self.face_joints:
                if cmds.objExists('face:' + fj):
                    cmds.parentConstraint(fj, 'face:' + fj)

            cmds.setAttr('face:null.v', False)
            cmds.evalDeferred(self.wireFrameOn)
            cmds.evalDeferred(cm.setJointXrayVis)

    def _allShow(self, is_show):
        for i in range(8):
            try:
                pm.setAttr('LOD{0}.v'.format(i), is_show)
            except:
                pass
            try:
                pm.setAttr('face:LOD{0}.v'.format(i), is_show)
            except:
                pass
            try:
                pm.checkBox('cb_lod_{0}'.format(i), e=True, v=is_show)
            except:
                pass

    def _toggleChange(self):
        toggle = self.cb_toggle.getValue()
        pm.rowLayout('rl_lod_vis', e=True, en=not toggle)
        if toggle:
            self._allShow(False)
            pm.checkBox('cb_lod_{0}'.format(0), e=True, v=True)
            pm.setAttr('LOD{0}.v'.format(0), True)
            try:
                pm.setAttr('face:LOD{0}.v'.format(0), True)
            except:
                pass

    def _changeAttr(self, target_i):
        if self.cb_toggle.getValue():
            for i in range(8):
                try:
                    if i != target_i:
                        pm.checkBox('cb_lod_{0}'.format(i), e=True, v=False)
                        pm.setAttr('LOD{0}.v'.format(i), False)
                        try:
                            pm.setAttr('face:LOD{0}.v'.format(i), False)
                        except:
                            pass
                    else:
                        pm.checkBox('cb_lod_{0}'.format(i), e=True, v=True)
                        pm.setAttr('LOD{0}.v'.format(i), True)
                        try:
                            pm.setAttr('face:LOD{0}.v'.format(i), True)
                        except:
                            pass
                except:
                    pass

        else:
            try:
                pm.setAttr(
                    'LOD{0}.v'.format(target_i),
                    pm.checkBox('cb_lod_{0}'.format(target_i), q=True, v=True)
                )
            except:
                pass
            try:
                pm.setAttr(
                    'face:LOD{0}.v'.format(target_i),
                    pm.checkBox('cb_lod_{0}'.format(target_i), q=True, v=True)
                )
            except:
                pass

    def _reset(self):
        if pm.objExists('null'):
            joints = cmds.ls('null', dag=True)
            for j in joints:
                if not j.startswith('_a'):
                    try:
                        cm.setTransform(j, self.transform_dict[j])
                    except:
                        pass

    def _offset(self):
        fs_v = self.fs.getValue()
        for i in range(8):
            try:
                pm.setAttr('LOD{0}.tx'.format(i), i * fs_v)
            except:
                pass
        self.ff.setValue(fs_v)

    def _offset2(self):
        ff_v = self.ff.getValue()
        for i in range(8):
            try:
                pm.setAttr('LOD{0}.tx'.format(i), i * ff_v)
            except:
                pass
        self.fs.setValue(ff_v)

    def _importAd(self):
        id_ = tsubasa._getIdFromRoot()
        if id_ is None:
            return

        work_path = tsubasa.getCharaWorkPathFromId(id_)
        _adn_path = os.path.join(work_path, 'rig/_data/_assistdrive/{0}.csv'.format(id_))
        import tsubasa.maya.rig.assistdrive as assistdrive
        if os.path.isfile(_adn_path):
            assistdrive.import_assistdrive_settings(_adn_path, '', False, False)
            cm.hum('Success !')
        else:
            pm.warning('{0} が見つかりません'.format(_adn_path))

    def _importCharacter(self):
        if not pm.objExists('_default_character'):
            for j in tsubasa.PRIMARY_JOINTS:
                if pm.objExists(j):
                    pm.setAttr(j + '.rx', 0)
                    pm.setAttr(j + '.ry', 0)
                    pm.setAttr(j + '.rz', 0)
            import baseBodyGuide.ui as bbgui
            bbgui.baseBodyGuideUI().setDefinition()

    def _setReference(self, _file):
        ref = self.ref_motion_ns + 'RN'
        if pm.objExists(ref):
            ref_file = pm.referenceQuery(ref, filename=True)
            ref = pm.FileReference(ref_file)
            ref.remove()

        #pm.importFile(os.path.join(self.ref_motion_dir, _file), ns=self.ref_motion_ns)
        pm.createReference(os.path.join(self.ref_motion_dir, _file), ns=self.ref_motion_ns)
        ref_nodes = pm.referenceQuery(ref, nodes=True)
        for top in pm.ls(ref_nodes, assemblies=True):
            pm.setAttr(top + '.v', False)

        cm.hum('import motion...')
        pm.evalDeferred(self._setSouece)

    def _setSouece(self):
        anim_curves = cm.getAnimCurves()
        pm.select(anim_curves)
        cm.setAllKeyRange()
        cm.changeHIKSource('_default_character', self.ref_motion_ns + ':_default_character')
        cm.hum('finish !')

    def _idleMotion(self):
        self._importCharacter()
        self._setReference('_motion_idle.mb')

    def _checkMotion(self):
        self._importCharacter()
        self._setReference('_motion_check.mb')

    def _visNull(self):
        pm.setAttr('null.v', self.cb_all_joint.getValue())

    def _visScondary(self):
        joints = pm.ls('null', dag=True)
        for j in joints:
            if j.name().startswith('_c') \
                or j.name().startswith('_d') \
                    or j.name().startswith('_e'):
                j.overrideEnabled.set(not self.cb_second.getValue())
                j.overrideVisibility.set(self.cb_second.getValue())

    def _visAssistDrive(self):
        joints = pm.ls('null', dag=True)
        for j in joints:
            if j.name().startswith('_a'):
                j.overrideEnabled.set(not self.cb_ad.getValue())
                j.overrideVisibility.set(self.cb_ad.getValue())

    def _visJointXray(self):
        cm.setJointXrayVis(self.cb_jx.getValue())

    def _delExceptA(self):
        nodes = [x for x in pm.ls(transforms=True)]
        for node in nodes:
            if '_LOD' in node.name() and not node.getShape():
                if not node.startswith('a_') and not node.startswith('face:a_'):
                    pm.delete(node)

    def _setColor(self, col):
        sels = cmds.ls(sl=True)
        if not sels:
            return

        for sel in sels:
            mesh_name = sel
            if 'LOD' in mesh_name:
                mesh_name = mesh_name.rsplit('_', 1)[0]

            for i in range(8):
                mesh = mesh_name
                if i != 0:
                    mesh = mesh_name + '_LOD{0}'.format(i)

                if pm.objExists(mesh):
                    shape = pm.PyNode(mesh).getShape()
                    if shape:
                        shape.overrideEnabled.set(1)
                        shape.overrideRGBColors.set(1)
                        shape.overrideColorRGB.set(col)

    def randAssignMT(self):
        sels = cmds.ls(sl=True)
        if not sels:
            return

        for sel in sels:
            mesh_name = sel
            if 'LOD' in mesh_name:
                mesh_name = mesh_name.rsplit('_', 1)[0]

            select_list = []
            for i in range(8):
                mesh = mesh_name
                if i != 0:
                    mesh = mesh_name + '_LOD{0}'.format(i)

                if pm.objExists(mesh):
                    select_list.append(mesh)

            x = random.uniform(0, 1.5)
            y = random.uniform(0, 1.5)
            z = random.uniform(0, 1.5)

            mt = cmds.shadingNode('lambert', n='randAssignMT#', asShader=True)
            cmds.setAttr(mt + '.color', x, y, z, type='double3')
            pm.select(select_list, r=True)
            cmds.hyperShade(assign=mt)
            cm.hum('{0},{1},{2}'.format(x, y, z))
        cm.hum()

    def randAssignMTAll(self):
        nodes = pm.ls('LOD0', dag=True)
        result = []
        for node in nodes:
            try:
                if node.getShape():
                    result.append(node)
            except:
                pass
        pm.select(result)
        self.randAssignMT()

    def _charaMotionImport(self):
        id_ = tsubasa._getIdFromRoot()
        if id_ is None:
            pm.warning('idが取得できません')
            return

        self._pose_update = False
        project_path = tsubasa.getCharaProjectPathFromId(id_)
        anim_path = os.path.join(project_path, 'Animation/Files')
        if not os.path.isdir(anim_path):
            anim_path = project_path
        motion_path = pm.fileDialog2(fileMode=1, dir=anim_path, ff='fbx(*.fbx)')
        if motion_path is not None:
            pm.importFile(motion_path)
            anim_curves = cm.getAnimCurves()
            pm.select(anim_curves)
            cm.setAllKeyRange()

            # AssistDriveのキーを削除
            null = [x for x in cmds.ls(type='joint') if 'null' in x]
            adn_joints = cmds.ls(null[0], dag=True, type='joint')
            for adn_joint in adn_joints:
                if adn_joint.startswith('_a'):
                    cmds.cutKey(adn_joint)

        pm.evalDeferred(pm.Callback('self._pose_update = True'))

    def wireFrameOn(self):
        state_ = pm.checkBox(self.cb_wire, q=True, v=True)
        cm.setWireFrameVis(state_)


def main():
    LodViewer().initUi()
