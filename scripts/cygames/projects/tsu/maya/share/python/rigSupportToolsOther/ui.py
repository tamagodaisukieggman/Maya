# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : rigSupportToolsOther.ui
# Author  : toi
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
import imp
from . import tools
# from . import skinPaintWeightSelectButton
from . import convertTex2ColorOnly
from . import npcTools
from dccUserMayaSharePythonLib import common as cm
from dccUserMayaSharePythonLib import pyCommon as pcm
from dccUserMayaSharePythonLib import skinning as sk
from dccUserMayaSharePythonLib import ui
from dccUserMayaSharePythonLib import tsubasa_dumspl as tsubasa
from dccUserMayaSharePythonLib import file_dumspl as f
# from rigSupportTools import ui as rstui
from attrWatcher import attrWatcher
from convertTex2jpgForMB import convertTex2jpgForMB

imp.reload(tools)
imp.reload(cm)
imp.reload(pcm)
imp.reload(sk)
imp.reload(ui)
imp.reload(f)
imp.reload(attrWatcher)
imp.reload(convertTex2ColorOnly)
imp.reload(npcTools)


class Ui(object):

    SETTING_DIR = os.path.join(os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"), 'Documents', 'maya', 'Scripting_Files')
    SETTING_JSON = os.path.join(SETTING_DIR, 'rigSupportToolsOtherSetting.json')
    if not os.path.isfile(SETTING_JSON):
        f.exportJson(SETTING_JSON)

    setting_dict = f.importJson(SETTING_JSON)

    def __init__(self):
        self.window_name = os.path.basename(os.path.dirname(__file__))
        self.doc_name = os.path.basename(os.path.dirname(__file__)) + '_doc'
        self.button_width = 100

    def delOverwrapWindow(self):
        if cmds.window(self.window_name, ex=True):
            cmds.deleteUI(self.window_name)

    def text(*args, **kwargs):
        cmds.text(al='left', *args, **kwargs)

    def itb(*args, **kwargs):
        cmds.iconTextButton(
            l='Apply', i='execute.png', st='iconAndTextHorizontal', bgc=(0.33, 0.33, 0.33),
            *args, **kwargs)

    def itb2(*args, **kwargs):
        cmds.iconTextButton(
            l='Launch', i='channelBox.png', st='iconAndTextHorizontal', bgc=(0.33, 0.33, 0.33),
            *args, **kwargs)

    def itb3(*args, **kwargs):
        cmds.iconTextButton(
            l='Create', i='addCreateGeneric.png', st='iconAndTextHorizontal', bgc=(0.33, 0.33, 0.33),
            *args, **kwargs)

    def initUi(self):
        self.delOverwrapWindow()
        cmds.window(self.window_name, t=self.window_name, w=400, mb=True)

        cmds.menu(l='Help')
        cmds.menuItem(l='Tool help', c=pm.Callback(os.startfile, 'https://wisdom.cygames.jp/x/wcArCw'))

        # top_cl = cmds.columnLayout(adj=True)
        top_cl = cmds.scrollLayout(cr=True)
        cmds.separator()

        # Select--------------------------------------------------
        cmds.frameLayout(l='Select', cll=True)
        cl = cmds.columnLayout(adj=True)

        # same_name_node_select
        rl = cmds.rowLayout(
            adj=True,
            nc=2,
            ann='先に選択した階層と後から選択した階層内の同名ノードを交互に選択します(ctrl押しでAssistDrive除外)')
        self.text(l='Select pair same name')
        cmds.rowLayout(adj=True, nc=2, w=self.button_width)
        self.itb(c=lambda *args: self.startSelect())
        cmds.setParent(cl)

        # sel_joint_hierarchy_ignore_del
        cmds.rowLayout(adj=True, nc=2, ann='プライマリージョイントを階層選択')
        self.text(l='Sel joint hierarchy ignore del')
        cmds.rowLayout(adj=True, nc=2, w=self.button_width)
        self.itb(c=lambda *args: self.startSelHierarchyIgnoreDel())
        cmds.setParent(cl)

        # selPrimaryJoints
        cmds.rowLayout(adj=True, nc=2, ann='プライマリージョイントを階層選択')
        self.text(l='Select primary')
        cmds.rowLayout(adj=True, nc=2, w=self.button_width)
        self.itb(c=lambda *args: tsubasa.selPrimaryJoints())
        cmds.setParent(cl)

        # sel_joint_hierarchy_ignore_del
        cmds.rowLayout(adj=True, nc=2, ann='シェイプ持ちのノードだけ選択')
        self.text(l='Select with shape node')
        cmds.rowLayout(adj=True, nc=2, w=self.button_width)
        self.itb(c=lambda *args: self.startSelWithShapeNode())
        cmds.setParent(cl)

        # node_select_window
        cmds.rowLayout(adj=True, nc=2, ann='選択ノードのセレクトボタンを作成')
        self.text(l='Node selecter')
        cmds.rowLayout(adj=True, nc=2, w=self.button_width)
        self.itb2(c=lambda *args: self.startNodeSelecter())
        cmds.setParent(cl)

        # select_set
        cmds.rowLayout(adj=True, nc=2, ann='選択セットの保存と呼び出しを行います')
        self.text(l='Select set')
        cmds.rowLayout(adj=True, nc=2, w=self.button_width)
        cmds.button(l='Save', c=lambda *args: self.startSaveSelectSet())
        cmds.button(l='Select', c=lambda *args: self.startSelectSet(), w=self.button_width / 2)
        cmds.setParent(cl)

        # select_opposite_joint
        cmds.rowLayout(adj=True, nc=2, ann='反対側のジョイントを選択')
        self.text(l='Select opposite joint')
        cmds.rowLayout(adj=True, nc=2, w=self.button_width)
        self.itb(c=lambda *args: pm.select(cm.getOppositeJoint(pm.ls(sl=True)[0])))
        cmds.setParent(cl)

        # select_related_influences
        cmds.rowLayout(adj=True, nc=2, ann='接続されているskinClusterのインフルエンスを選択')
        self.text(l='Select related influences')
        cmds.rowLayout(adj=True, nc=2, w=self.button_width)
        self.itb(c=lambda *args: sk.selectRelatedInfluences(cmds.ls(sl=True), True))

        # Pair process--------------------------------------------------
        cmds.setParent(top_cl)
        cmds.frameLayout(
            l='Pair process', cll=True,
            ann='選択ノード内を（偶数番から奇数番へ影響を与える）ように交互に連続処理します')
        cl = cmds.columnLayout(adj=True)

        cmds.radioCollection()
        cmds.rowLayout(nc=2)
        #cmds.text(l='')
        self.rb_alternation = cmds.radioButton(l='alternation', sl=True)
        cmds.radioButton(l='first')
        cmds.setParent(cl)

        cmds.separator(h=10)

        # Parent Const
        cmds.rowLayout(adj=True, nc=2, ann='parenConst:先に選択したノード → 後から選択したノード（ctrl押しでオフセットTrue）')
        self.text(l='Const')
        cmds.rowLayout(adj=True, nc=4, w=self.button_width)
        cmds.button(l='P', c=lambda *args: self.startConst(0))
        cmds.button(l='O', c=lambda *args: self.startConst(1))
        cmds.button(l='S', c=lambda *args: self.startConst(2))
        cmds.button(l='Pa', c=lambda *args: self.startConst(3))
        cmds.setParent(cl)

        # Connect Rotate
        cmds.rowLayout(adj=True, nc=2, ann='Connect Rotate:先に選択したノード → 後から選択したノード')
        self.text(l='Connect Rotate')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startConnectRotate())
        cmds.setParent(cl)

        # copy
        cmds.rowLayout(adj=True, nc=2, ann='先に選択したノードのTRS値に、後から選択したノードのTRS値を合わせます')
        self.text(l='Copy val')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startCopy())
        cmds.setParent(cl)

        # swap
        cmds.rowLayout(adj=True, nc=2, ann='双方の値を入れ替えます（複数選択OK：端数は無視）')
        self.text(l='Swap val')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startSwap())
        cmds.setParent(cl)

        # match world transforms
        cmds.rowLayout(adj=True, nc=2, ann='先に選択したノードの位置回転に、後から選択したノードを合わせます')
        self.text(l='Match world transforms')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startMatch())
        cmds.setParent(cl)

        # Mirror Trans
        cmds.rowLayout(adj=True, nc=2, ann='先に選択したノードのYZ反転位置に、後から選択したノードを合わせます')
        self.text(l='Mirror Trans')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startMirrorTrans())
        cmds.setParent(cl)

        # name
        cmds.rowLayout(adj=True, nc=2, ann='先に選択したノード名と、後から選択したノード名を合わせます（ネームスペースを除く）')
        self.text(l='Match name')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startMatchName())
        cmds.setParent(cl)

        # joint label
        cmds.rowLayout(adj=True, nc=2)
        self.text(l='Match Joint Label')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startMatchLabel())
        cmds.setParent(cl)

        cmds.separator(h=10)

        # Create Ax
        cmds.rowLayout(adj=True, nc=2, ann='先に選択したノードの子供としてaxグループノードとロケータを作成し、コンストします')
        self.text(l='Create Ax')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb3(c=lambda *args: self.startCreateAx())
        cmds.setParent(cl)

        # Create Ctrl Locator
        cmds.rowLayout(adj=True, nc=2, ann='先に選択したノードの子供としてロケータを作成し、コンストします')
        self.text(l='Create Ctrl Locator')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb3(c=lambda *args: self.startCreateCtrlLocator())
        cmds.setParent(cl)

        cmds.separator(h=10)

        # Copy paste vertex weight
        cmds.rowLayout(adj=True, nc=2, ann='')
        self.text(l='Copy paste vertex weight')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startCopyPasteVertexWeight())
        cmds.setParent(cl)

        # bind_pair_model
        cmds.rowLayout(adj=True, nc=2, ann='先に選択したノードが影響を受けているinfluencesに、後から選択したノードをbindします')
        self.text(l='Bind same influences')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startBindPairModel())
        cmds.setParent(cl)

        # copy_skin_weight
        cmds.rowLayout(adj=True, nc=2, ann='先に選択したノードのskin情報を、後から選択したノードにペーストします')
        self.text(l='Copy skin weight')
        cmds.rowLayout(adj=True, nc=2, w=self.button_width)
        self.itb(c=lambda *args: self.startCopySkinWeight())
        cmds.setParent(cl)

        # bind_and_copy
        cmds.rowLayout(adj=True, nc=2, ann='バインドとコピースキンウエイトを同時に行います')
        self.text(l='Bind and copy ( Position )')
        cmds.rowLayout(adj=True, nc=2, w=self.button_width)
        self.itb(c=lambda *args: self.startBindAndCopy(infle='closestJoint'))
        cmds.setParent(cl)

        # bind_and_copy
        cmds.rowLayout(adj=True, nc=2, ann='バインドとコピースキンウエイトを同時に行います')
        self.text(l='Bind and copy ( Label )')
        cmds.rowLayout(adj=True, nc=2, w=self.button_width)
        self.itb(c=lambda *args: self.startBindAndCopy())
        cmds.setParent(cl)

        # bind_and_copy
        cmds.rowLayout(adj=True, nc=2, ann='バインドとコピースキンウエイトを同時に行います')
        self.text(l='Bind and copy ( One to one )')
        cmds.rowLayout(adj=True, nc=2, w=self.button_width)
        self.itb(c=lambda *args: self.startBindAndCopy(infle='oneToOne'))
        cmds.setParent(cl)

        '''
        cmds.frameLayout(l='skin')

        #write_pair_model
        cmds.rowLayout(adj=True, nc=2, ann='tmp_nodeに選択したノードのペア情報を書き込む')
        self.text(l='write_pair_model')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        cmds.button(l='apply', c=lambda *args: self.startWritePairModel())
        cmds.setParent(cl)
        '''

        # Tsubasa--------------------------------------------------
        cmds.setParent(top_cl)
        cmds.frameLayout(l='Tsubasa', cll=True)
        cl = cmds.columnLayout(adj=True)

        cmds.rowLayout(adj=True, nc=2)
        self.text(l='fbxシーン用にテクスチャをjpg変換')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb2(c=lambda *args: convertTex2jpgForMB.main())
        cmds.setParent(cl)

        cmds.rowLayout(adj=True, nc=2)
        self.text(l='NPC Tools')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb2(c=lambda *args: npcTools.initUi())
        cmds.setParent(cl)

        cmds.rowLayout(adj=True, nc=2)
        self.text(l='Normalize mesh for export')
        cmds.rowLayout(
            adj=True, nc=1, w=self.button_width,
            ann='出力前のprune, round, max_influenceを掛けます（選択ノードの階層以下が対象）')
        self.itb2(c=lambda *args: self.startNormailze())
        cmds.setParent(cl)

        # Etc--------------------------------------------------
        cmds.setParent(top_cl)
        cmds.frameLayout(l='Etc', cll=True)
        cl = cmds.columnLayout(adj=True)

        # Duplicate
        cmds.rowLayout(adj=True, nc=2, ann='選択した２ノードの階層内全ノードを、名前ベースで比較します')
        self.text(l='Duplicate')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb3(c=lambda *args: self.startDuplicate())
        cmds.setParent(cl)

        # Create joint hierarchy
        cmds.rowLayout(adj=True, nc=2, ann='X軸方向に伸びるジョイント階層を作成する')
        self.text(l='Create joint hierarchy')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb3(c=lambda *args: self.startCreateJoint())
        cmds.setParent(cl)

        # Create wld
        cmds.rowLayout(adj=True, nc=2, ann='選択ノードのwldノードを作成する')
        self.text(l='Create wld')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb3(c=lambda *args: self.startCreateWld())
        cmds.setParent(cl)

        # Copy Clipboard sel node
        cmds.rowLayout(adj=True, nc=2, ann='ctrl押しで改行入り')
        self.text(l='to clipboard sel node')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startCopy2Clip())
        cmds.setParent(cl)

        # Round
        cmds.rowLayout(adj=True, nc=2, ann='選択ノードのトランスフォーム値を少数第一位までにまるめます')
        self.text(l='Round')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startRound())
        cmds.setParent(cl)

        # Compare val
        cmds.rowLayout(adj=True, nc=2, ann='先に選択したノードのTRS値と、後から選択したノードのTRS値を比較します')
        self.text(l='Compare val')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startCompareVal())
        cmds.setParent(cl)

        # Compare parent and child
        cmds.rowLayout(adj=True, nc=2, ann='先に選択したノードと、後から選択したノードの親子名を比較します（ネームスペースを除く）')
        self.text(l='Compare parent and child')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startCompareParentChild())
        cmds.setParent(cl)

        # Compare hierarchy
        cmds.rowLayout(adj=True, nc=2, ann='選択した２ノードの階層内全ノードを、名前ベースで比較します')
        self.text(l='Compare name two hierarchy')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startCompareHierarchy())
        cmds.setParent(cl)

        # add_namespace_all_nodes
        cmds.rowLayout(adj=True, nc=2, ann='全てのノードに指定したネームスペースを追加する')
        self.text(l='Add namespace all nodes')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startAddNamespaceAllnodes())
        cmds.setParent(cl)

        # Aim to child
        cmds.rowLayout(adj=True, nc=2, ann='ジョイントの向きを子供の方向へ向ける（tgt, src, upv の順に3つ選択して実行 ： ctrl押しでマイナス方向）')
        self.text(l='Aim to child')
        cmds.rowLayout(adj=True, nc=3, w=self.button_width)
        cmds.button(l='X', c=lambda *args: self.startAimToChild('X'))
        cmds.button(l='Y', c=lambda *args: self.startAimToChild('Y'), w=self.button_width / 3)
        cmds.button(l='Z', c=lambda *args: self.startAimToChild('Z'), w=self.button_width / 3)
        cmds.setParent(cl)

        # Mirror Joint
        cmds.rowLayout(adj=True, nc=2, ann='選択ジョイントの反対に反転ジョイントを作成（選択が２つある場合は一つ目の反対値を２つ目に適用する）ctrl押しでマイナス方向')
        self.text(l='Mirror Joint')
        cmds.rowLayout(adj=True, nc=3, w=self.button_width)
        cmds.button(l='X', c=lambda *args: self.startMirrorJoint('X'))
        cmds.button(l='Y', c=lambda *args: self.startMirrorJoint('Y'), w=self.button_width / 3)
        cmds.button(l='Z', c=lambda *args: self.startMirrorJoint('Z'), w=self.button_width / 3)
        cmds.setParent(cl)

        # segmentscale
        cmds.rowLayout(adj=True, nc=2, ann='選択ノードの階層に含まれるジョイントのセグメントスケールをoff')
        self.text(l='SegmentScale Off')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb(c=lambda *args: self.startSetSegmentScaleOff())
        cmds.setParent(cl)

        # limit
        cmds.rowLayout(adj=True, nc=2, ann='現在値で選択ノードのリミットをかけます')
        self.text(l='Set limit current val')
        cmds.rowLayout(adj=True, nc=2, w=self.button_width)
        cmds.button(l='On', c=lambda *args: self.startLimit())
        cmds.button(l='Off', c=lambda *args: self.startLimit(False), w=self.button_width / 2)
        cmds.setParent(cl)

        # marking_color
        cmds.rowLayout(adj=True, nc=2, ann='選択ノードのアウトライナカラーを変更（シェイプがある場合はシェイプのオーバーライドも）')
        self.text(l='Marking color')
        cmds.rowLayout(adj=True, nc=2, w=self.button_width)
        cmds.button(l='Set', c=lambda *args: self.startMarkingColor())
        cmds.button(l='Off', c=lambda *args: self.startMarkingColor(False), w=self.button_width / 2)
        cmds.setParent(cl)

        # decomp locator
        cmds.rowLayout(adj=True, nc=2, ann='選択ジョイント以下のジョイントオリエントを一覧表示する')
        self.text(l='Locator with decompMat')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb2(c=lambda *args: self.startCreateLocWithDecomp())
        cmds.setParent(cl)

        # joint_orient_list
        cmds.rowLayout(adj=True, nc=2, ann='選択ジョイント以下のジョイントオリエントを一覧表示する')
        self.text(l='Joint Orient List')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb2(c=lambda *args: self.startJointOrientList())
        cmds.setParent(cl)

        # joint_orient_list
        cmds.rowLayout(adj=True, nc=2, ann='選択ジョイント以下のMaintainMaxInfluencesを一覧表示する')
        self.text(l='MaintainMaxInfluences List')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb2(c=lambda *args: self.startMmiList())
        cmds.setParent(cl)

        # skin_paint_weight_select_button
        # cmds.rowLayout(adj=True, nc=2, ann='ペイントツールとセレクトボタンアイコンだけのウインドウを作成する')
        # self.text(l='Skin paint weight select button')
        # cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        # self.itb2(c=lambda *args: self.startSkinPaintWeightSelectButton())
        # cmds.setParent(cl)

        # move joint test
        cmds.rowLayout(adj=True, nc=2, ann='選択以下のジョイントを順番に動かしてWeightの飛びを確認します')
        self.text(l='Move joint test')
        cmds.rowLayout(adj=True, nc=1, w=self.button_width)
        self.itb2(c=lambda *args: self.modeJointTest())
        cmds.setParent(cl)

        # doc化
        doc_ui_list = cmds.lsUI(type='dockControl')
        if doc_ui_list is not None:
            if self.doc_name in doc_ui_list:
                cmds.deleteUI(self.doc_name)
        cmds.dockControl(self.doc_name, area='left', content=self.window_name, allowedArea=['right', 'left'])
        #cmds.showWindow(self.window_name)

    # ----------------------------------------------------------------------------------------
    def _isAlternation(self):
        return cmds.radioButton(self.rb_alternation, q=True, sl=True)

    def _pairProcessing(self, command):
        cm.hum()
        sels = cmds.ls(sl=True)
        if self._isAlternation():
            for i, sel in enumerate(sels):
                if i < len(sels) - 1:
                    if i % 2 == 0:
                        command(sels[i], sels[i + 1])
        else:
            for i, sel in enumerate(sels):
                if i < len(sels) - 1:
                    command(sels[0], sels[i + 1])
        cm.hum('Finished')

    def startSelect(self):
        sels = cmds.ls(sl=True)
        if cmds.getModifiers() == 4:
            cm.sameNameNodeSelect(sels[0], sels[1], ['_a'])
        else:
            cm.sameNameNodeSelect(sels[0], sels[1])

    def startLimit(self, set_limit=True):
        cm.hum()
        sels = cmds.ls(sl=True)
        for sel in sels:
            cm.limit(sel, set_limit)
        cm.hum('Finished')

    def startCopy(self):
        self._pairProcessing(cm.copy)

    def startMatch(self):
        self._pairProcessing(cm.match)

    def startMatchName(self):
        self._pairProcessing(cm.matchName)

    def startMatchLabel(self):
        self._pairProcessing(cm.matchJointLabel)

    def startCopyPasteVertexWeight(self):
        self._pairProcessing(sk.copyPasteVertexWeight)

    def startConst(self, cons):
        sels = pm.ls(sl=True)
        offset = True if cmds.getModifiers() == 4 else False
        if self._isAlternation():
            for i in range(len(sels)):
                if i < len(sels) - 1:
                    if i % 2 == 0:
                        if cons == 0:
                            pm.pointConstraint(sels[i], sels[i + 1], mo=offset)
                        elif cons == 1:
                            pm.orientConstraint(sels[i], sels[i + 1], mo=offset)
                        elif cons == 2:
                            pm.scaleConstraint(sels[i], sels[i + 1], mo=offset)
                        elif cons == 3:
                            pm.parentConstraint(sels[i], sels[i + 1], mo=offset)
        else:
            for i, sel in enumerate(sels):
                if i < len(sels) - 1:
                    if cons == 0:
                        pm.pointConstraint(sels[0], sels[i + 1], mo=offset)
                    elif cons == 1:
                        pm.orientConstraint(sels[0], sels[i + 1], mo=offset)
                    elif cons == 2:
                        pm.scaleConstraint(sels[0], sels[i + 1], mo=offset)
                    elif cons == 3:
                        pm.parentConstraint(sels[0], sels[i + 1], mo=offset)

    def startConnectRotate(self):
        sels = pm.ls(sl=True)
        if self._isAlternation():
            for i in range(len(sels)):
                if i < len(sels) - 1:
                    if i % 2 == 0:
                        pm.connectAttr(sels[i].name() + '.rx', sels[i + 1].name() + '.rx')
                        pm.connectAttr(sels[i].name() + '.ry', sels[i + 1].name() + '.ry')
                        pm.connectAttr(sels[i].name() + '.rz', sels[i + 1].name() + '.rz')
        else:
            for i, sel in enumerate(sels):
                if i < len(sels) - 1:
                    pm.connectAttr(sels[0].name() + '.rx', sels[i + 1].name() + '.rx')
                    pm.connectAttr(sels[0].name() + '.ry', sels[i + 1].name() + '.ry')
                    pm.connectAttr(sels[0].name() + '.rz', sels[i + 1].name() + '.rz')

    def startSwap(self):
        cm.hum()
        sels = cmds.ls(sl=True)
        for i, sel in enumerate(sels):
            if i % 2 == 0:
                cm.swap(sels[i], sels[i + 1])
        cm.hum('Finished')

    def startCompareVal(self):
        split_str = '  :  '

        cm.hum()
        sels = cmds.ls(sl=True)
        not_same_list = []
        for i, sel in enumerate(sels):
            if i % 2 == 0:
                if cm.compareVal(sels[i], sels[i + 1]):
                    not_same_list.append(sels[i] + split_str + sels[i + 1])

        if not_same_list:
            tx = (
                '<big>上記ノードの組み合わせは値が異なりました。</big><br>'
                'The above nodes have different values than each other.')
        else:
            tx = '<big>全てのノードの値は一致しました。</big><br>All value is same.'

        tslw = ui.TextScrollListWindow(not_same_list, 'CompareVal')
        pm.setParent(tslw.cl)
        pm.text(tx, al='left')

        def selnode():
            pm.select(cl=True)
            sel_items = tslw.tsl.getSelectItem()
            for sel_item in sel_items:
                sel_item = sel_item.split(split_str)
                pm.select(sel_item, add=True)

        tslw.tsl.selectCommand(pm.Callback(selnode))
        tslw.init_ui()

    def startCompareParentChild(self, check_only=False):
        split_str = '  :  '

        cm.hum()
        sels = cmds.ls(sl=True)
        error_list = []
        for i, sel in enumerate(sels):
            if i % 2 == 0:
                result = cm.compareHierarchyParentChildren(sels[i], sels[i + 1])
                if result:
                    error_list.append(sels[i] + split_str + sels[i + 1])

        if check_only:
            return error_list

        if error_list:
            tx = (
                '<big>上記のノードの組み合わせは親子が異なっていました。</big><br>'
                'The above nodes have different parents and children.')
        else:
            tx = "<big>全てのノードの親子は一致しました。</big><br>All the nodes' parents and children matched."

        tslw = ui.TextScrollListWindow(error_list, 'CompareParentChild')
        pm.setParent(tslw.cl)
        pm.text(tx, al='left')

        def selnode():
            pm.select(cl=True)
            sel_items = tslw.tsl.getSelectItem()
            for sel_item in sel_items:
                sel_item = sel_item.split(split_str)
                pm.select(sel_item, add=True)

        tslw.tsl.selectCommand(pm.Callback(selnode))
        tslw.init_ui()

    def startSelWithShapeNode(self):
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

    def startNodeSelecter(self):
        sels = cmds.ls(sl=True)
        if sels:
            from nodeSelecter import nodeSelecter
            nodeSelecter.main()

    def startSaveSelectSet(self):
        cm.hum()
        sels = cmds.ls(sl=True)
        self.setting_dict['select_set'] = sels
        f.exportJson(self.SETTING_JSON, self.setting_dict)
        cm.hum('Saved')

    def startSelectSet(self):
        ss = self.setting_dict['select_set']
        cmds.select(ss)

    def startCopySkinWeight(self):
        cm.hum()
        sels = cmds.ls(sl=True)

        if self._isAlternation():
            for i, sel in enumerate(sels):
                if i % 2 == 0:
                    try:
                        sk.copySkinWeight(sels[i], sels[i + 1])
                        print('Success : copySkinWeight', sels[i], sels[i + 1])
                    except Exception as e:
                        print('{0} {1} {2} {3} {4}'.format('=' * 20, 'error : copySkinWeight', sels[i], sels[i + 1], '=' * 20))
                        print(e)
        else:
            for i, sel in enumerate(sels):
                if i < len(sels) - 1:
                    try:
                        sk.copySkinWeight(sels[0], sels[i + 1])
                        print('Success : copySkinWeight', sels[0], sels[i + 1])
                    except Exception as e:
                        print('{0} {1} {2} {3} {4}'.format('=' * 20, 'error : copySkinWeight', sels[i], sels[i + 1], '=' * 20))
                        print(e)

        cm.hum('Finished')

    '''
    def startWritePairModel(self):
        sels = cmds.ls(sl=True)
        for i, sel in enumerate(sels):
            if i % 2 == 0:
                sk.writePairModel(sels[i], sels[i + 1])
        sk.create_bind_pair_model_window()
    '''

    def startBindPairModel(self):
        sels = cmds.ls(sl=True)
        finish_works = 0

        if self._isAlternation():
            for i, sel in enumerate(sels):
                if i < len(sels) - 1:
                    if i % 2 == 0:
                        if not sk.bindPairModel(sels[i], sels[i + 1]):
                            print('Success : bindPairModel', sels[i], sels[i + 1])
                            finish_works += 1
                        #except Exception as e:
                        #	print('{0} {1} {2} {3} {4}'.format('=' * 20, 'error : bindPairModel', sels[i], sels[i + 1], '=' * 20))
                        #	print(e)
        else:
            for i, sel in enumerate(sels):
                if i < len(sels) - 1:
                    if not sk.bindPairModel(sels[0], sels[i + 1]):
                        print('Success : bindPairModel', sels[0], sels[i + 1])
                        finish_works += 1
                    #except Exception as e:
                    #	print('{0} {1} {2} {3} {4}'.format('=' * 20, 'error : bindPairModel', sels[i], sels[i + 1], '=' * 20))
                    #	print(e)

        cmds.select(sels)
        cm.hum('Finished {0} / {1}'.format(finish_works, int(len(sels) / 2)))

    @staticmethod
    def startCompareHierarchy(check_only=False):
        sels = cmds.ls(sl=True)
        if len(sels) != 2:
            pm.warning('Select 2 nodes')
            return

        result = cm.getDifferentNodesIn2Hierarchy(sels[0], sels[1])

        if check_only:
            return result

        if result:
            text_ = ('<big>上記ノードは どちらかの階層にしか含まれていません。</big><br>'
                'The above nodes are only included in one of the hierarchies.')
        else:
            text_ = '<big>２つの階層のノード構成は一致しました。</big><br>The node configuration of the two hierarchies matched.'

        tslw = ui.TextScrollListWindow(result, 'CompareHierarchy')
        pm.setParent(tslw.cl)
        pm.text(text_, al='left')

        def selnode():
            pm.select(cl=True)
            sel_items = tslw.tsl.getSelectItem()
            for sel_item in sel_items:
                pm.select(sel_item, add=True)

        tslw.tsl.selectCommand(pm.Callback(selnode))
        tslw.init_ui()

    @staticmethod
    def startSelHierarchyIgnoreDel():
        sels = cmds.ls(sl=True)
        sk.selJointHierarchyIgnoreDel(sels)

    @staticmethod
    def startAddNamespaceAllnodes():
        tools.addNamespaceAllNodes()

    @staticmethod
    def startSkinPaintWeightSelectButton():
        skinPaintWeightSelectButton.skinPaintWeightSelectButton()

    @staticmethod
    def startAttrWatcher():
        attrWatcher.main()

    @staticmethod
    def startMarkingColor(set_color=True):
        sels = [x for x in pm.ls(pm.ls(sl=True, type=('transform', 'joint')))]
        tools.markingColor(sels, set_color)

    @staticmethod
    def startCreateJoint():
        w = 'CreateJointSetting'
        rc = 'Rc_' + w
        ifg = 'Ifg_' + w

        def main():
            axis = cmds.radioButton(cmds.radioCollection(rc, q=True, sl=True), q=True, l=True)
            num = cmds.intSliderGrp(ifg, q=True, v=True)
            tools.createJointHierarchy(axis, num)

        if cmds.window(w, ex=True):
            cmds.deleteUI(w)
        cmds.window(w, t=w, w=400)
        cmds.columnLayout(adj=True)
        cmds.radioCollection(rc)
        cmds.rowLayout(nc=6)
        cmds.radioButton(l='+x', sl=True)
        cmds.radioButton(l='-x')
        cmds.radioButton(l='+y')
        cmds.radioButton(l='-y')
        cmds.radioButton(l='+z')
        cmds.radioButton(l='-z')
        cmds.setParent('..')
        cmds.intSliderGrp(ifg, max=10, min=0, fmx=100, f=True, cc=pm.Callback(main))
        cmds.showWindow(w)

    @staticmethod
    def startCreateWld(set_color=True):
        sels = [x for x in pm.ls(pm.ls(sl=True, type=('transform', 'joint')))]
        if sels:
            for s in sels:
                cm.createWld(s)

    @staticmethod
    def startDuplicate():
        sels = cmds.ls(sl=True)
        if sels:
            for sel in sels:
                if pm.getModifiers() == 4:
                    cm.duplicate(sel, True)
                else:
                    cm.duplicate(sel)

    @staticmethod
    def startJointOrientList():
        sels = cmds.ls(sl=True)
        if not sels:
            return

        sk.selJointHierarchyIgnoreDel(sels)
        aw = attrWatcher.Ui()
        aw.nodes = cmds.ls(sl=True)
        at_rl_list = aw.initAcg(['jointOrient'])
        for at, rl in at_rl_list:
            val = cmds.getAttr(at)[0]
            if val[0] != 0.0 or val[1] != 0.0 or val[2] != 0.0:
                cmds.rowLayout(rl, e=True, bgc=[1, 0, 0])

    @staticmethod
    def startMmiList():
        sels = cmds.ls(sl=True)
        if not sels:
            return

        shapes = sk.getShapeHierarchy(sels)
        skin_clusters = sk.listRelatedSkinClusters(shapes)
        cmds.select(skin_clusters)
        aw = attrWatcher.Ui()
        aw.nodes = cmds.ls(sl=True)
        if not aw.nodes:
            pm.warning('no skinClusters')
            return

        at_rl_list = aw.initAcg(['maintainMaxInfluences'])
        #for at, rl in at_rl_list:
        #	val = cmds.getAttr(at)[0]
        #	if val[0] != 0.0 or val[1] != 0.0 or val[2] != 0.0:
        #		cmds.rowLayout(rl, e=True, bgc=[1, 0, 0])

    def startSetSegmentScaleOff(self):
        sels = cmds.ls(sl=True)
        if not sels:
            return

        nodes = cmds.ls(sels[0], dag=True)
        result = self.setSegmentScaleOff(nodes)
        cm.hum('{0} joints done'.format(len(result)))

    @staticmethod
    def setSegmentScaleOff(nodes):
        set_list = []
        for node in nodes:
            if cmds.nodeType(node) == 'joint':
                if cmds.getAttr(node + '.segmentScaleCompensate'):
                    cmds.setAttr(node + '.segmentScaleCompensate', 0)
                    set_list.append(node)
        return set_list

    @staticmethod
    def startCreateAx():
        sels = pm.ls(sl=True)
        for i in range(len(sels)):
            if i % 2 == 0:
                _parent = sels[i]
                _source = sels[i + 1]

                ax = pm.group(em=True, n=_source + '_ax')
                pm.parent(ax, _parent)
                cm.match(_source, ax)

                loc = pm.spaceLocator(n=_source + '_ctrl')
                pm.parent(loc, ax)
                cm.resetTransform(loc)
                pm.parentConstraint(loc, _source)
                pm.scaleConstraint(loc, _source)

    @staticmethod
    def startCreateCtrlLocator():
        sels = pm.ls(sl=True)
        for i in range(len(sels)):
            if i % 2 == 0:
                _parent = sels[i]
                _source = sels[i + 1]

                loc = pm.spaceLocator(n=_source + '_ctrl')
                pm.parent(loc, _parent)
                cm.match(_source, loc)

                pm.parentConstraint(loc, _source)
                pm.scaleConstraint(loc, _source)

    @staticmethod
    def startRound():
        sels = pm.ls(sl=True)
        for sel in sels:
            t = pm.getAttr(sel + '.t')
            pm.setAttr(sel + '.t', *[round(t[0], 1), round(t[1], 1), round(t[2], 1)])
            r = pm.getAttr(sel + '.r')
            pm.setAttr(sel + '.r', *[round(r[0], 1), round(r[1], 1), round(r[2], 1)])

    def startBindAndCopy(self, infle=['label', 'closestJoint']):
        cm.hum()
        sels = cmds.ls(sl=True)

        def main(src, tgt):
            print('####', src, ' > ', tgt)
            try:
                sk.bindPairModel(src, tgt)
                print('Success : bindPairModel')
                cmds.refresh()
                time.sleep(0.05)
                sk.copySkinWeight(src, tgt, influenceAssociation_=infle)
                cmds.refresh()
                time.sleep(0.05)
                print('Success : bind_and_copy')
            except Exception as e:
                print('{0} {1} {2}'.format('=' * 20, 'error : bind_and_copy', '=' * 20))
                print(e)
                print(sys.exc_info()[2].tb_lineno)

        if self._isAlternation():
            for i, sel in enumerate(sels):
                if i < len(sels) - 1:
                    if i % 2 == 0:
                        main(sels[i], sels[i + 1])
        else:
            for i, sel in enumerate(sels):
                if i < len(sels) - 1:
                    main(sels[0], sels[i + 1])

        pm.select(sels)
        cm.hum('Finished')

    @staticmethod
    def modeJointTest():
        sels = pm.ls(sl=True)
        joints = pm.ls(sels[0], dag=True, type='joint')

        t = 0
        for j in joints:
            try:
                pm.setAttr(j + '.t', lock=False)
                pm.setAttr(j + '.tx', lock=False)
                pm.setAttr(j + '.ty', lock=False)
                pm.setAttr(j + '.tz', lock=False)
                #pm.mel.eval('CBdeleteConnection "{0}.t"'.format(j.name()))
                pm.mel.eval('CBdeleteConnection "{0}.tx"'.format(j.name()))
                pm.mel.eval('CBdeleteConnection "{0}.ty"'.format(j.name()))
                pm.mel.eval('CBdeleteConnection "{0}.tz"'.format(j.name()))

                pm.setKeyframe(j, at=['tx', 'ty', 'tz'], t=t)
                t += 10

                val = [0, 100, 100]
                _side = pm.getAttr(j + '.side')
                if _side == 1:
                    x_val = 100
                elif _side == 2:
                    x_val = -100
                else:
                    x_val = 0

                current_val = pm.getAttr(j + '.t')
                current_worldval = pm.xform(j, q=True, ws=True, t=True)
                pm.xform(j, ws=True, t=[current_worldval[0] + x_val, current_worldval[1] + 100, current_worldval[2] + 100])
                pm.setKeyframe(j, at=['tx', 'ty', 'tz'], t=t)

                t += 10
                pm.setAttr(j + '.t', *current_val)
                pm.setKeyframe(j, at=['tx', 'ty', 'tz'], t=t)

                t += 10
            except:
                pass

        pm.playbackOptions(e=True, max=t, min=0)

    @staticmethod
    def startNormailze():
        from autoNormalize import autoNormalize
        autoNormalize.main()

    @staticmethod
    def startAimToChild(axis):
        sels = pm.ls(sl=True)

        aimvec = 1
        upvec = 1
        if pm.getModifiers() == 4:
            aimvec = -1
        if pm.getModifiers() == 1 or pm.getModifiers() == 5:
            upvec = -1

        if len(sels) == 3:
            tgt, child, upv = sels
            if axis == 'X':
                cm.aimToChild(tgt, child, upv, vec=[(aimvec, 0, 0), (0, 0, upvec)])
            elif axis == 'Y':
                cm.aimToChild(tgt, child, upv, vec=[(0, aimvec, 0), (0, 0, upvec)])
            else:
                cm.aimToChild(tgt, child, upv, vec=[(0, 0, aimvec), (0, 0, upvec)])
        else:
            tgt, child = sels
            if axis == 'X':
                cm.aimToChild(tgt, child, vec=[(aimvec, 0, 0), (0, 0, upvec)])
            elif axis == 'Y':
                cm.aimToChild(tgt, child, vec=[(0, aimvec, 0), (0, 0, upvec)])
            else:
                cm.aimToChild(tgt, child, vec=[(0, 0, aimvec), (0, 0, upvec)])

        pm.select(tgt)

    @staticmethod
    def startMirrorTrans():
        sels = pm.ls(sl=True)
        for i in range(len(sels)):
            if i % 2 == 0:
                cm.mirrorTrans(sels[i], sels[i + 1])

    def startCreateLocWithDecomp(self):
        decomp = cmds.shadingNode('decomposeMatrix', asUtility=True, name='testDecomposeMatrix')
        loc = cmds.spaceLocator(n='from_{}'.format(decomp))[0]

        cm.connectTrss(decomp, loc)

    def startCopy2Clip(self):
        sels = cmds.ls(sl=True)
        result_text = ''
        if pm.getModifiers() == 4:
            for sel in sels:
                result_text += sel + '\n'
            result_text = result_text.rstrip('\n')
        else:
            for sel in sels:
                result_text += sel + ', '
            result_text = result_text.rstrip(', ')

        cm.toClip(result_text)


def main():
    Ui().initUi()
