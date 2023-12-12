# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : bindAndCopyWeight.bindAndCopyWeight
# Author  : toi
# Version : 0.1.1
# Update  : 2020/11/11
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import maya.mel as mm
import pymel.core as pm
import os
import sys
import time
import json
import stat
from functools import partial
from collections import OrderedDict
from dccUserMayaSharePythonLib import common as cm
from dccUserMayaSharePythonLib import skinning as sk
from dccUserMayaSharePythonLib import file_dumspl as f
from rigSupportToolsOther import ui


def bindAndCopy(surfaceAssociation, influenceAssociation, normalize):
	sels = cmds.ls(sl=True)
	count = 0
	for i, sel in enumerate(sels):
		if i % 2 == 0:
			count += 1
			try:
				print('####', sels[i], ' > ', sels[i + 1])
				sk.bindPairModel(sels[i], sels[i + 1])
				print('Success : bindPairModel')
			except Exception as e:
				print('{0} {1} {2}'.format('=' * 20, 'error : bindPairModel', '=' * 20))
				print(e)
				print(sys.exc_info()[2].tb_lineno)
				
			cmds.refresh()
			time.sleep(0.02)
			
			try:
				sk.copySkinWeight(
					sels[i],
					sels[i + 1],
					surfaceAssociation_=surfaceAssociation,
					influenceAssociation_=influenceAssociation,
					normalize_=normalize)
				print('Success : copyWeight')
			except Exception as e:
				print('{0} {1} {2}'.format('=' * 20, 'error : copyWeight', '=' * 20))
				print(e)
				print(sys.exc_info()[2].tb_lineno)
				
			cmds.refresh()
			time.sleep(0.02)
			cm.hum('{0} / {1}'.format(count, int(len(sels) / 2)))
			print()
			
	
class Ui(object):

	SETTING_DIR = os.path.join(os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"), 'Documents', 'maya', 'Scripting_Files')
	SETTING_JSON = os.path.join(SETTING_DIR, 'bindAndCopyWeight.json')
	if not os.path.isfile(SETTING_JSON):
		f.exportJson(SETTING_JSON)
		
	setting_dict = f.importJson(SETTING_JSON)
		
	def __init__(self):
		self.window_name = os.path.basename(os.path.dirname(__file__))
		
		self.surf_assoc_dict = {
			1: ['Closest point on surface', 'closestPoint'],
			2: ['Ray cast', 'rayCast'],
			3: ['Closest component', 'closestComponent']
		}
		
		self.infl_assoc_dict = {
			'Closest joint': 'closestJoint',
			'Closest bone': 'closestBone',
			'One to one': 'oneToOne',
			'Label': 'label',
			'Name': 'name'
		}
	
		#設定辞書初期化
		self.setting_dict.setdefault('rbg_sa', 1)
		self.setting_dict.setdefault('op_ia1', 1)
		self.setting_dict.setdefault('op_ia2', 1)
		self.setting_dict.setdefault('op_ia3', 1)
		self.setting_dict.setdefault('cbg_norm', False)
		
	def toolReset(self):
		self.setting_dict = {
			'rbg_sa': 1,
			'op_ia1': 1,
			'op_ia2': 1,
			'op_ia3': 1,
			'cbg_norm': False
		}
		f.exportJson(self.SETTING_JSON, self.setting_dict)
		self.updateUi()

	def delOverwrapWindow(self):
		if cmds.window(self.window_name, ex=True):
			cmds.deleteUI(self.window_name)
			
	def pulldown(self, num):
		op = cmds.optionMenuGrp(l='Influence Association {0}: '.format(num))
		if num != 1:
			cmds.menuItem(l='None')
		cmds.menuItem(l='Closest joint')
		cmds.menuItem(l='Closest bone')
		cmds.menuItem(l='One to one')
		cmds.menuItem(l='Label')
		cmds.menuItem(l='Name')
		cmds.optionMenuGrp(op, e=True)
		return op
			
	def initUi(self):
		self.delOverwrapWindow()
		cmds.window(self.window_name, t=self.window_name, w=400, mb=True)
		cmds.menu(l='Tools')
		cmds.menuItem(l='Tool reset', c=pm.Callback(self.toolReset))
		cmds.menu(l='Help')
		cmds.menuItem(l='Tool help', c=pm.Callback(os.startfile, 'https://wisdom.cygames.jp/x/A_UrCw'))
		top_cl = cmds.columnLayout(adj=True, co=['both', 2])
		cmds.separator()
		
		cmds.frameLayout(l='CopySkinWeightOptions', cll=True)
		cmds.columnLayout(adj=True)
		self.rbg_sa = cmds.radioButtonGrp(
			l='Surface Association: ', numberOfRadioButtons=3, vr=True,
			labelArray3=[self.surf_assoc_dict[1][0], self.surf_assoc_dict[2][0], self.surf_assoc_dict[3][0]])
		cmds.separator(h=10)
		
		self.op_ia1 = self.pulldown(1)
		self.op_ia2 = self.pulldown(2)
		self.op_ia3 = self.pulldown(3)
		cmds.separator(h=10)
		
		self.cbg_norm = cmds.checkBoxGrp(l='', label1='Normalize')
		cmds.separator(h=10, style='none')
		cmds.setParent(top_cl)
		
		cmds.separator(h=10)
		cmds.text(l='', h=3)
		cmds.text(l='同名同階層のメッシュの バインド状態とウエイトをコピペします', al='left')
		cmds.text(l='「 コピー元モデルのルートノード 」  →  「 コピー先モデルのルートノード 」 の順に選択して実行', al='left')
		cmds.separator(h=10)
		cmds.button(
			l='新旧階層の ノードの数と名前の違いをチェック', c=pm.Callback(self.compareHierarchy),
			ann='実行前に階層のチェックを行います。それぞれのルートノードを選択してからボタンを押してください。')
		cmds.separator(h=10)
		cmds.button(l='実行', c=pm.Callback(self.startBindAndCopy), h=30)
		cmds.text(l='', h=3)
		cmds.showWindow(self.window_name)
		self.updateUi()
		
	def updateUi(self):
		cmds.radioButtonGrp(self.rbg_sa, e=True, sl=self.setting_dict['rbg_sa'])
		cmds.optionMenuGrp(self.op_ia1, e=True, sl=self.setting_dict['op_ia1'])
		cmds.optionMenuGrp(self.op_ia2, e=True, sl=self.setting_dict['op_ia2'])
		cmds.optionMenuGrp(self.op_ia3, e=True, sl=self.setting_dict['op_ia3'])		
		cmds.checkBoxGrp(self.cbg_norm, e=True, v1=self.setting_dict['cbg_norm'])
		
	def compareHierarchy(self):
		ui.Ui().startCompareHierarchy()
		
	def startBindAndCopy(self):
		cm.hum()
		sels = cmds.ls(sl=True)
		if len(sels) != 2:
			cmds.warning('no select nodes')
			return
			
		#階層のチェック
		result = cm.getDifferentNodesIn2Hierarchy(sels[0], sels[1])
		if result:
			response = cmds.confirmDialog(
				title='Confirm', message='2つの階層内の構成が異なっています。\n正しく動作しない可能性があります。',
				button=['強制実行', '中止'], defaultButton='中止', cancelButton='中止', dismissString='中止',
				p=self.window_name, icon='warning')
			if response == '中止':
				return
			
		surf_assoc_num = cmds.radioButtonGrp(self.rbg_sa, q=True, sl=True)
		surf_assoc = self.surf_assoc_dict[surf_assoc_num][1]
		
		infl_assoc_list = []
		op1 = cmds.optionMenuGrp(self.op_ia1, q=True, v=True)
		if op1 != 'None':
			infl_assoc_list.append(self.infl_assoc_dict[op1])
		op2 = cmds.optionMenuGrp(self.op_ia2, q=True, v=True)
		if op2 != 'None':
			infl_assoc_list.append(self.infl_assoc_dict[op2])
		op3 = cmds.optionMenuGrp(self.op_ia3, q=True, v=True)
		if op3 != 'None':
			infl_assoc_list.append(self.infl_assoc_dict[op3])
			
		normalize = cmds.checkBoxGrp(self.cbg_norm, q=True, v1=True)
		print(surf_assoc, infl_assoc_list, normalize)
		
		cm.sameNameNodeSelect(sels[0], sels[1])

		bindAndCopy(surf_assoc, infl_assoc_list, normalize)
		cm.hum('終了しました')
		
		#設定保存
		self.setting_dict['rbg_sa'] = surf_assoc_num
		self.setting_dict['op_ia1'] = cmds.optionMenuGrp(self.op_ia1, q=True, sl=True)
		self.setting_dict['op_ia2'] = cmds.optionMenuGrp(self.op_ia2, q=True, sl=True)
		self.setting_dict['op_ia3'] = cmds.optionMenuGrp(self.op_ia3, q=True, sl=True)
		self.setting_dict['cbg_norm'] = normalize
		f.exportJson(self.SETTING_JSON, self.setting_dict)
		
			
def main():
	Ui().initUi()