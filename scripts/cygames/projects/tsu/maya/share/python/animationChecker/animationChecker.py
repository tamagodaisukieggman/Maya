# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : animationChecker
# Author  : toi
# Release  : 2023/1/23
# LastUpdate  : 2023/1/23
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import pymel.core as pm
import os
import sys
# from collections import OrderedDict
from dccUserMayaSharePythonLib import common as cm
from dccUserMayaSharePythonLib import pyCommon as pcm
from dccUserMayaSharePythonLib import file_dumspl as f

#reload(f)
#reload(pcm)


class AnimationChecker(object):
    def __init__(self):
        self.window_name = os.path.basename(os.path.dirname(__file__))

        self.target_files = []
        self.input_values = []
        self.target_attrs = []
        self.target_file_ext = ''
        self.result_dict = {}

        self.attr_cb_name = 'cb_{}_ac'

        # 設定ファイル
        self.setting = f.createSettingFile(self.window_name)

    def delOverwrapWindow(self):
        if cmds.window(self.window_name, ex=True):
            pm.deleteUI(self.window_name)

    def initUi(self):
        self.delOverwrapWindow()
        pm.window(self.window_name, t=self.window_name, w=400, mb=True)

        pm.menu(l='Help')
        pm.menuItem(l='Tool help', c=pm.Callback(os.startfile, 'https://wisdom.cygames.jp/x/ZkP-I'))

        # ---------------------------------
        self.fl = pm.formLayout()

        top_cl = pm.columnLayout(adj=True)
        pm.separator()

        with pm.horizontalLayout(ratios=[0, 10, 1]) as hl:
            pm.text(l='対象フォルダ : ', ann='')
            self.tf_dir = pm.textField(tx=self.setting.get('tf_dir'))
            pm.iconTextButton(
                st='iconOnly', i='SP_DirClosedIcon.png',
                c=pm.Callback(self.setDir))
            hl.redistribute()

        self.cb_icf = pm.checkBox(
            l='子孫フォルダ内のファイルを含める', ann='フォルダ内に含まれるフォルダ内のファイルも対象にする',
            v=self.setting.get('cb_icf', False), cc=pm.Callback(self.startGetFiles))

        with pm.horizontalLayout(ratios=[0, 1]):
            self.tx_find_file = pm.text(l='見つかったファイル : ')
            self.fbx_num_text = pm.text(l='', al='left')

        pm.separator(h=12)

        pm.radioCollection()
        self.rb_no_anim_files = pm.radioButton(l='指定したジョイントにキーが無い [ fbx ] ファイルを探す', sl=True)
        self.tf_user_input_value = pm.textField(tx=self.list2String(self.setting.get('tf_user_input_value')))
        with pm.horizontalLayout():
            for trs in cm.trsList():
                ui_name = self.attr_cb_name.format(trs)
                pm.checkBox(ui_name, l=trs, v=self.setting.get(ui_name, True))

        pm.separator(h=12)

        self.bt_lacg = pm.iconTextButton(
            l='Start check', c=pm.Callback(self.start), st='iconAndTextHorizontal',
            ann='', i='refEdFileList.png', bgc=(0.33, 0.33, 0.33))
        pm.separator(h=3, style='none')
        self.cb_show_finding_only = pm.checkBox(
            l='該当したファイルのみ表示する', ann='オフにすると調査した全てのファイルを表示します',
            v=self.setting.get('cb_show_finding_only', False), cc=pm.Callback(self._showReslut))

        pm.setParent(self.fl)
        self.tsl = pm.textScrollList(ams=True)

        # レイアウト調整
        if sys.hexversion < 0x3000000:
            tsl_pos = 190
        else:
            tsl_pos = 200
        pm.formLayout(self.fl, e=True, af=[(top_cl, 'top', 0), (top_cl, 'left', 10), (top_cl, 'right', 10)])
        pm.formLayout(self.fl, e=True, af=[(self.tsl, 'top', tsl_pos), (self.tsl, 'right', 10), (self.tsl, 'left', 10), (self.tsl, 'bottom', 10)])
        # ---------------------------------

        pm.showWindow(self.window_name)
        self.startGetFiles()

    def _getExt(self):
        if pm.radioButton(self.rb_no_anim_files, q=True, sl=True):
            self.target_file_ext = 'fbx'

    def setDir(self):
        chioce = pm.fileDialog2(fm=2, okCaption='Select')
        if chioce is not None:
            pm.textField(self.tf_dir, e=True, tx=chioce[0])
            self.startGetFiles()

            self.setting.set('tf_dir', chioce[0])

    def startGetFiles(self):
        self._getExt()
        target_dir = pm.textField(self.tf_dir, q=True, tx=True)
        if not os.path.isdir(target_dir):
            return

        include_child = pm.checkBox(self.cb_icf, q=True, v=True)
        self.setting.set('cb_icf', include_child)

        self.tx_find_file.setLabel('見つかったファイル : ')
        self.fbx_num_text.setLabel('')

        files = f.getAllFiles(target_dir, include_child)
        if files:
            self.target_files = [x for x in files if x.endswith('.{}'.format(self.target_file_ext))]
            if self.target_files:
                self.tx_find_file.setLabel('見つかった{}ファイル : '.format(self.target_file_ext))
                self.fbx_num_text.setLabel('<font color=yellow>' + str(len(self.target_files)))

    def start(self):
        if not self.target_files:
            pm.warning('{}ファイルが見つかりません'.format(self.target_file_ext))
            return

        input_values = pm.textField(self.tf_user_input_value, q=True, tx=True)
        if not input_values:
            if pm.radioButton(self.rb_no_anim_files, q=True, sl=True):
                pm.warning('ジョイントが指定されていません')
                return
        self.input_values = list(set([x.strip() for x in input_values.split(' ') if x]))
        self.setting.set('tf_user_input_value', self.input_values)

        self.attr_val_list = []
        for trs in cm.trsList():
            cb_name = self.attr_cb_name.format(trs)
            cb_val = pm.checkBox(cb_name, q=True, v=True)
            self.setting.set(cb_name, cb_val)
            if cb_val:
                self.attr_val_list.append(trs)

        if not self.attr_val_list:
            pm.warning('対象アトリビュートを選択してください')
            return

        if pm.confirmDialog(
            title='Confirm', message='maya上でシーンを連続して開いて調べます\n全て終わるまで止めることはできません',
            button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel',
            p=self.window_name, icn='question') == 'OK':
            self.main()

    def main(self):
        self.result_dict = {}
        for target_file in self.target_files:
            cmds.file(f=True, new=True)
            f.importFbx(target_file)

            joints = pm.ls(type='joint')
            joints_remove_ns_dict = {x.split(':')[-1]: x for x in joints}

            message = ''
            for input_value in self.input_values:
                if input_value in joints_remove_ns_dict:
                    no_anim_list = self._checkAnimationExists(joints_remove_ns_dict[input_value])
                    if no_anim_list:
                        no_anim_list_stroing = ''
                        for no_anim in no_anim_list:
                            no_anim_list_stroing += no_anim + ', '
                        no_anim_list_stroing = no_anim_list_stroing[:-2]
                        message += '{} : {}'.format(joints_remove_ns_dict[input_value], no_anim_list_stroing) + ' / '
            self.result_dict[target_file] = message
        self._showReslut()

    def _checkAnimationExists(self, node):
        no_anim_list = []
        for trs in self.attr_val_list:
            if not pm.keyframe(node, q=True, tc=True, at=trs):
                no_anim_list.append(trs)
        return no_anim_list

    def _showReslut(self):
        if not self.result_dict:
            return

        self.result_dict = pcm.sortDict(self.result_dict)
        show_finding_only = pm.checkBox(self.cb_show_finding_only, q=True, v=True)
        self.setting.set('cb_show_finding_only', show_finding_only)

        pm.textScrollList(self.tsl, e=True, ra=True)
        for file_name, message in self.result_dict.items():
            if not show_finding_only or message:
                pm.textScrollList(self.tsl, e=True, a=os.path.basename(file_name) + '  |  ' + message)

    @staticmethod
    def list2String(targetList):
        result = ''
        for l in targetList:
            result += l + ' '
        return result


def main():
    AnimationChecker().initUi()
