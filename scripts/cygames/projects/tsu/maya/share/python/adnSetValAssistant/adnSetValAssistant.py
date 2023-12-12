# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : adnSetValAssistant
# Author  : toi
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import pymel.core as pm
import os
from collections import OrderedDict
from functools import partial
from dccUserMayaSharePythonLib import common as cm
from dccUserMayaSharePythonLib import pyCommon as pcm
#from dccUserMayaSharePythonLib import ui

#reload(cm)
#reload(pcm)


class Ui(object):
    def __init__(self):
        self.window_name = os.path.basename(os.path.dirname(__file__))
        self.attr_trs = ['translate', 'rotate', 'scale']

        self.frame_col = (0.2, 0.2, 0.8)
        self.frame_col2 = (0.8, 0.2, 0.2)

    def delOverwrapWindow(self):
        if pm.window(self.window_name, ex=True):
            pm.deleteUI(self.window_name)

    def initUi(self):
        #self.delOverwrapWindow()
        win = pm.window(self.window_name + '#', t=self.window_name, w=1200, mb=True)

        pm.menu(l='Help')
        pm.menuItem(l='Tool help', c="os.startfile('https://wisdom.cygames.jp/x/6l39Ig')")
        pm.menuItem(l='AssistDrive help', c="os.startfile('https://wisdom.cygames.jp/x/azR5BQ')")

        with pm.horizontalLayout(ratios=(1, 0, 1)):
            with pm.columnLayout(adj=True, co=('both', 2)):
                pm.button(l='↓↓　AssistDrive ジョイントをセット', c=partial(self.setNode), h=30)

                pm.separator(h=10)
                self.cl_attr = pm.columnLayout(adj=True)
            pm.separator(w=10, hr=False)
            with pm.frameLayout(l='角度と距離から move系AssistDrive の値を設定', en=False, bgc=self.frame_col2) as fl:
                with pm.columnLayout(adj=True, co=('both', 2), rs=2):
                    self.ffg_roll_axis = self._ffgAixs('駆動ジョイントの軸（ Roll Axis ）')
                    self.ffg_move_axis = self._ffgAixs('移動ジョイントの軸（ Move Axis ）')
                    self.ffg_offset = self._ffgAixs('オフセット')
                    self.ff_distance = self._sliderFloatField('移動距離', 0, 1000)
                    self.ff_min = self._sliderFloatField('最小角度', -180, 180)
                    self.ff_max = self._sliderFloatField('最大角度', -180, 180)
                    pm.separator(h=10)
                    pm.button(l='↑↑　AssistDrive ノードに値をセット  ', c=partial(self.main), h=30)
            self.fl_set_val = fl

        pm.showWindow(win)

    def setNode(self, *args):
        sels = pm.ls(sl=True)
        if not sels:
            return

        self.tgt_joint = sels[0]
        source_ADNs = [x for x in pm.listConnections(self.tgt_joint, s=True, d=False) if pm.nodeType(x) == 'AssistDriveNode']
        if not source_ADNs:
            return

        self.target_ADN = source_ADNs
        self.move_ADNs = [x for x in source_ADNs if 'Move' in pm.getAttr(x + '.DriveType')]
        if self.move_ADNs:
            self.target_ADN = self.move_ADNs[0]
        else:
            self.target_ADN = source_ADNs[0]

        self.drive_joint = pm.listConnections(self.target_ADN + '.InputMatrix', s=True, d=False)
        if not self.drive_joint:
            return
        self.drive_joint = self.drive_joint[0]

        children_layouts = pm.columnLayout(self.cl_attr, q=True, ca=True)
        if children_layouts:
            pm.deleteUI(children_layouts)
        #pm.evalDeferred(partial(self._createAttrUi))
        self._createAttrUi()

        enable_frame = True if self.move_ADNs else False
        pm.frameLayout(self.fl_set_val, e=True, en=enable_frame)
        if enable_frame:
            current_adn_node = pm.textField(self.tf_adn_joint, q=True, tx=True)
            roll_axis = pm.getAttr(current_adn_node + '.RollAxis')
            pm.floatFieldGrp(self.ffg_roll_axis, e=True, v1=roll_axis[0], v2=roll_axis[1], v3=roll_axis[2])
            move_axis = pm.getAttr(current_adn_node + '.MoveAxis')
            pm.floatFieldGrp(self.ffg_move_axis, e=True, v1=move_axis[0], v2=move_axis[1], v3=move_axis[2])
            offset = pm.getAttr(current_adn_node + '.MoveOffset')
            pm.floatFieldGrp(self.ffg_offset, e=True, v1=offset[0], v2=offset[1], v3=offset[2])

    def _textFieldJoint(self, node):
        with pm.horizontalLayout(ratios=(9, 1)):
            tf = pm.textField(tx=node.name(), h=26)
            pm.textField(tf, e=True, cc=partial(self._rename, node, tf))
            pm.button(l='選択', c='cmds.select("{}")'.format(node.name()))
        return tf

    def _rename(self, *args):
        node = args[0]
        tf = args[1]
        name = pm.textField(tf, q=True, tx=True)
        pm.rename(node, name)
        pm.textField(tf, e=True, cc=partial(self._rename, name, tf))

    def _createAttrUi(self):
        pm.setParent(self.cl_attr)
        with pm.frameLayout(l='駆動ジョイント', bgc=self.frame_col):
            with pm.columnLayout(adj=True, co=('both', 2)):
                self._textFieldJoint(self.drive_joint)
                pm.text(l='', h=2)
                pm.attrFieldGrp(at=self.drive_joint + '.t', pre=3)
                pm.attrFieldGrp(at=self.drive_joint + '.r', pre=3)
                pm.attrFieldGrp(at=self.drive_joint + '.s', pre=3)

        with pm.frameLayout(l='AssistDrive ジョイント', bgc=self.frame_col):
            with pm.columnLayout(adj=True, co=('both', 2)):
                self._textFieldJoint(self.tgt_joint)
                pm.text(l='', h=2)
                pm.attrFieldGrp(at=self.tgt_joint + '.t', pre=3)
                pm.attrFieldGrp(at=self.tgt_joint + '.r', pre=3)
                pm.attrFieldGrp(at=self.tgt_joint + '.s', pre=3)
                pm.attrFieldGrp(at=self.tgt_joint + '.preferredAngle', pre=3)
                pm.attrFieldGrp(at=self.tgt_joint + '.jointOrient', pre=3)
                pm.attrControlGrp(a=self.tgt_joint + '.side')
                pm.attrControlGrp(a=self.tgt_joint + '.type')
                pm.attrControlGrp(a=self.tgt_joint + '.otherType')
                pm.text(l='', h=5)

        with pm.frameLayout(l='AssistDrive ノード', bgc=self.frame_col):
            enable = False if self.move_ADNs else True

            with pm.columnLayout(adj=True, co=('both', 2)):
                self.tf_adn_joint = self._textFieldJoint(self.target_ADN)
                pm.text(l='', h=2)
                try:
                    pm.attrControlGrp(a=self.target_ADN + '.DriveType', en=enable)
                except:
                    pass
                try:
                    pm.attrFieldGrp(at=self.target_ADN + '.RollAxis', en=enable, pre=3)
                except:
                    pass
                try:
                    pm.attrFieldGrp(at=self.target_ADN + '.MoveAxis', en=enable, pre=3)
                except:
                    pass
                try:
                    pm.attrFieldGrp(at=self.target_ADN + '.MoveOffset', en=enable, pre=3)
                except:
                    pass
                try:
                    pm.attrControlGrp(a=self.target_ADN + '.MoveLength', en=enable)
                except:
                    pass
                try:
                    pm.attrFieldGrp(at=self.target_ADN + '.MoveRange', numberOfFields=2, en=enable, pre=3)
                except:
                    pass
                try:
                    pm.attrControlGrp(a=self.target_ADN + '.EaseType')
                except:
                    pass
                try:
                    pm.attrControlGrp(a=self.target_ADN + '.RollRate')
                except:
                    pass
                try:
                    pm.attrControlGrp(a=self.target_ADN + '.EtcRate')
                except:
                    pass
                try:
                    pm.attrControlGrp(a=self.target_ADN + '.RollType')
                except:
                    pass
                try:
                    pm.attrControlGrp(a=self.target_ADN + '.YawRate')
                except:
                    pass
                try:
                    pm.attrControlGrp(a=self.target_ADN + '.YawLimit')
                except:
                    pass
                try:
                    pm.attrControlGrp(a=self.target_ADN + '.PitchRate')
                except:
                    pass
                try:
                    pm.attrControlGrp(a=self.target_ADN + '.PitchLimit')
                except:
                    pass
                try:
                    pm.attrControlGrp(a=self.target_ADN + '.PitchLimit')
                except:
                    pass
                try:
                    pm.attrControlGrp(a=self.target_ADN + '.RotateOffset')
                except:
                    pass

    def _ffgAixs(self, label_):
        with pm.horizontalLayout() as hl:
            pm.text(l='')
            ffg = pm.floatFieldGrp(l=label_, nf=3, pre=3)
            hl.redistribute(1, 9)
        return ffg

    def _sliderFloatField(self, label_, min_, max_):
        with pm.horizontalLayout() as hl:
            pm.text(l=label_)
            fs = pm.floatSlider(min=min_, max=max_)
            ff = pm.floatField(pre=3)
            pm.floatSlider(fs, e=True, dc=partial(self._setFieldValFormSlider, ff, fs))
            pm.floatField(ff, e=True, cc=partial(self._setSliderValFromField, ff, fs))
            hl.redistribute(1, 3, 1)
        return ff

    def _setFieldValFormSlider(self, *args):
        ff = args[0]
        fs = args[1]
        val = cmds.floatSlider(fs, q=True, v=True)
        cmds.floatField(ff, e=True, v=val)

    def _setSliderValFromField(self, *args):
        ff = args[0]
        fs = args[1]
        val = cmds.floatField(ff, q=True, v=True)
        cmds.floatSlider(fs, e=True, v=val)

    # -----------------------------------------
    def main(self, *args):
        # UI値取得
        roll_axis = pm.floatFieldGrp(self.ffg_roll_axis, q=True, v=True)
        move_axis = pm.floatFieldGrp(self.ffg_move_axis, q=True, v=True)
        offset = pm.floatFieldGrp(self.ffg_offset, q=True, v=True)
        distance = pm.floatField(self.ff_distance, q=True, v=True)
        min = pm.floatField(self.ff_min, q=True, v=True)
        max = pm.floatField(self.ff_max, q=True, v=True)
        print(roll_axis, move_axis, offset, distance, min, max)

        # 変換
        tgt_angle = (max - min)
        angle_rate = 360.0 / tgt_angle
        set_distance = distance * angle_rate / 2
        print(set_distance)

        target_angle = max - min
        min_angle_rate = distance * (min / target_angle)
        max_angle_rate = distance * (max / target_angle)
        print(min_angle_rate, max_angle_rate)

        # 結果をAssistDriveノードの値に反映
        cmds.setAttr(self.target_ADN + '.RollAxis', *roll_axis)
        cmds.setAttr(self.target_ADN + '.MoveAxis', *move_axis)
        cmds.setAttr(self.target_ADN + '.MoveOffset', *offset)

        cmds.setAttr(self.target_ADN + '.MoveLength', set_distance)
        cmds.setAttr(self.target_ADN + '.MoveRange', *(min_angle_rate, max_angle_rate))

        # フレーム動かしてAssistDrive駆動させる
        cf = cmds.currentTime(q=True)
        cmds.currentTime(cf + 1, e=True)
        cmds.currentTime(cf, e=True)


def main():
    Ui().initUi()
