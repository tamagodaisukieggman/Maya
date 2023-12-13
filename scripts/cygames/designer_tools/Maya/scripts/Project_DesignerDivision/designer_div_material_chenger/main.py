# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import sys

from PySide2 import QtWidgets
from maya import OpenMayaUI
import maya.cmds as cmds

import shiboken2
from . import material_controller as mtl_controller
from .ui import material_changer_win as main_win  # メインウインドウ（この中のクラスはウインド重複防止関数内でtype比較しているのでリロードNG）
from .project_data import project_define as pj_define

try:
    from importlib import reload
    from builtins import object
except Exception:
    pass

reload(mtl_controller)
reload(pj_define)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):
    """処理等を記載していくメインのクラス
    """

    # ==================================================
    def __init__(self):
        """コンストラクタ
        """

        self.gui = main_win.GUI()
        self.controller = None

    # ==================================================
    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            # for Maya 2022-
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if type(target) == type(widget):
                widget.close()          # クローズイベントを呼んでウインドウを閉じる
                widget.deleteLater()    # Mayaウインドウの子からインスタンスを削除

    # ==================================================
    def show_ui(self):
        """UIの呼び出し
        """

        # 前処理
        self.deleteOverlappingWindow(self.gui)

        # UIのセットアップなどなど
        self.setup_view_event()
        self.update_controller()

        # 表示
        self.gui.show()

    # ===============================================
    def setup_view_event(self):

        self.gui.addCallback('SceneOpened', self.update_controller)
        self.gui.ui.txt_info.setReadOnly(True)

        # event
        self.gui.ui.btn_update_root.clicked.connect(self.__update_root_event)

        self.gui.ui.btn_material_default.clicked.connect(self.__material_default_event)
        self.gui.ui.btn_material_work.clicked.connect(self.__material_work_event)
        self.gui.ui.btn_material_unity.clicked.connect(self.__material_unity_event)

        self.gui.ui.btn_outline_default.clicked.connect(self.__outline_default_event)
        self.gui.ui.btn_outline_unity.clicked.connect(self.__outline_unity_event)

    # ===============================================
    def update_controller(self, arg=None):

        # モデルルートとコントローラーの初期化
        self.gui.ui.txt_root.setText('')
        self.__init_root_txt()
        self.__init_controller_from_ui()
        self.__update_info_txt()

    # ===============================================
    def __update_info_txt(self):

        text = self.__get_info_text()
        self.gui.ui.txt_info.setPlainText(text)

    # ===============================================
    def __init_root_txt(self):

        # 入力がなければシーン名から取得を試みる
        if not self.gui.ui.txt_root.text():
            self.gui.ui.txt_root.setText(self.__get_root_from_scene_name())

    # ==================================================
    def __get_root_from_scene_name(self):

        scene_path = cmds.file(q=True, sn=True)

        if not scene_path:
            return ''

        # シーン名と同じトランスフォールがあればそれをルートとみなす
        file_base_name = os.path.splitext(os.path.basename(scene_path))[0]
        roots = cmds.ls('{}'.format(file_base_name), l=True)

        if not roots:
            return ''
        else:
            return roots[0]

    # ===============================================
    def __init_controller_from_ui(self):

        root = self.gui.ui.txt_root.text()

        if not root or not cmds.objExists(root):
            # ルートが未記入or見つからない場合
            return

        # 特殊なフォルダ構成ではないので、sceneやsourceimagesのフォルダ指定はなし
        self.controller = mtl_controller.MaterialController()
        self.controller.initialize(root, None, None)

    # ===============================================
    def __get_info_text(self):

        # controllerが設定できていない場合
        if not self.controller:
            return '情報が取得できませんでした。モデルの親階層を入力し「更新」を押してください。'

        # header
        text = '=' * 20 + '\n'
        text += self.gui.ui.txt_root.text() + '\n'
        text += '=' * 20 + '\n'

        text += '\n'

        # info_text
        mesh_mtl_str_list = []
        for material_data in self.controller.material_data_list:

            if not material_data.is_assigned:
                continue

            short_name = material_data.mesh.split('|')[-1]
            mesh_mtl_str = '{} : {}'.format(short_name, material_data.name)
            if mesh_mtl_str not in mesh_mtl_str_list:
                mesh_mtl_str_list.append(mesh_mtl_str)

        for mesh_mtl_str in mesh_mtl_str_list:
            text += mesh_mtl_str
            text += '\n'

        return text

    # ===============================================
    def __update_root_event(self):

        self.__init_controller_from_ui()
        self.__update_info_txt()

    # ===============================================
    def __material_default_event(self):

        if not self.controller:
            return
        else:
            self.controller.change_material_by_type(pj_define.MTL_TYP_DEFAULT)

        self.__update_info_txt()

    # ===============================================
    def __material_work_event(self):

        if not self.controller:
            return
        else:
            self.controller.change_material_by_type(pj_define.MTL_TYP_PSD)

        self.__update_info_txt()

    # ===============================================
    def __material_unity_event(self):

        if not self.controller:
            return
        else:
            self.controller.change_material_by_type(pj_define.MTL_TYP_TOON)

        self.__update_info_txt()

    # ===============================================
    def __outline_default_event(self):

        if not self.controller:
            return
        else:
            self.controller.change_material_by_type(pj_define.MTL_TYP_DEFAULT, pj_define.MSH_SFX_OUTLINE)

        self.__update_info_txt()

    # ===============================================
    def __outline_unity_event(self):

        if not self.controller:
            return
        else:
            self.controller.change_material_by_type(pj_define.MTL_TYP_OUTLINE, pj_define.MSH_SFX_OUTLINE)

        self.__update_info_txt()
