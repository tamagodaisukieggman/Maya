# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

from PySide2 import QtCore, QtGui, QtWidgets
from maya import OpenMayaUI

from . import view

import maya.cmds as cmds
import shiboken2
import sys


class Main(object):

    def __init__(self):

        self.view = view.View()

        self.model = None

    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return
        try:
            main_window = shiboken2.wrapInstance(
                long(main_window), QtWidgets.QMainWindow)
        except Exception:
            # for Maya 2022-
            main_window = shiboken2.wrapInstance(
                int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if type(target) == type(widget):
                widget.deleteLater()

    def show_ui(self):
        """UI表示
        """
        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)
        if sys.version_info.major == 2:
            self.model = QtGui.QStringListModel()
        else:
            # for Maya 2022-
            self.model = QtCore.QStringListModel()
        self.view.ui.targetObjectListView.setModel(self.model)

        self.setup_view_event()
        self.view.show()

    def setup_view_event(self):
        """UIのevent設定
        """

        self.view.ui.execButton.clicked.connect(
            lambda: self.set_impact_param()
        )

        self.view.ui.addTargetButton.clicked.connect(
            lambda: self.add_target_list()
        )

        self.view.ui.deleteTargetButton.clicked.connect(
            lambda: self.delete_target_list()
        )

        self.view.ui.allDeleteTargetButton.clicked.connect(
            lambda: self.clear_target_list()
        )

    def add_target_list(self):
        """選択したオブジェクトを対象オブジェクト一覧に追加
        """

        sels_org = cmds.ls(sl=True, l=True)
        sels = list(set(cmds.ls(sels_org, o=True, l=True)))
        if not sels:
            return

        target_list = self.model.stringList()
        for sel in sels:

            if sel in target_list:
                continue

            target_list.append(sel)

        self.model.setStringList(target_list)

    def delete_target_list(self):
        """選択したオブジェクトを対象オブジェクト一覧から削除
        """

        sels_org = cmds.ls(sl=True, l=True)
        sels = list(set(cmds.ls(sels_org, o=True, l=True)))
        if not sels:
            return

        target_list = self.model.stringList()
        tmp_target_list = []

        for target in target_list:

            if target in sels:
                continue

            tmp_target_list.append(target)

        if target_list != tmp_target_list:
            self.model.setStringList(tmp_target_list)

    def clear_target_list(self):
        """全てのオブジェクトを対象オブジェクト一覧から削除
        """

        self.model.setStringList([])

    def set_impact_param(self):
        """影響度をUV3にセット
        """

        sels = cmds.ls(sl=True, l=True)

        has_processed = False
        target_list = self.model.stringList()
        for target in target_list:

            if not cmds.objExists(target):
                continue

            uvsets = cmds.polyUVSet(target, q=True, allUVSets=True)
            if len(uvsets) < 3:

                if len(uvsets) == 1:
                    # uvsetをコピーしてダミー作成
                    cmds.polyUVSet(target, uvSet=uvsets[0], copy=True, newUVSet='uv2')

                    # 再度個数確認
                    uvsets = cmds.polyUVSet(target, q=True, allUVSets=True)

                # uvsetが2つの場合、影響力などが加味されていないため単純にUVを2つコピーする
                if len(uvsets) == 2:
                    cmds.polyUVSet(target, uvSet=uvsets[0], copy=True, newUVSet='uv3')

                    # 再度個数確認
                    uvsets = cmds.polyUVSet(target, q=True, allUVSets=True)

            if 'uv3' not in uvsets:
                return

            impact_value = self.view.ui.impactParamSpinBox.value()

            # uv3にyが一番低い頂点のx/yをそれぞれu/vに代入
            cmds.select(target)
            cmds.polyUVSet(uvSet='uv3', currentUVSet=True)
            cmds.select(target + '.map[*]')
            cmds.polyEditUV(relative=False, uValue=impact_value, vValue=0)

            has_processed = True

        cmds.select(sels)

        if has_processed:
            cmds.confirmDialog(title='完了', message='処理が完了しました。')
