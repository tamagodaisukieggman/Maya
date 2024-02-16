# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import shiboken2

from PySide2 import QtWidgets
from maya import OpenMayaUI

from . import view, controller

try:
    # Maya2022-
    from builtins import object
except Exception:
    pass


class Main(object):

    def __init__(self):
        """[summary]
        """

        self.parent = self.__get_parent()

        # windowの重複削除処理
        self.__delete_overlapping_window([view.View(), view.CaptureWindow(), view.ShotgridLoginDialog()])

        self.view = view.View()
        self.capture_window = view.CaptureWindow(self.parent)
        self.login_dialog = view.ShotgridLoginDialog(self.parent)
        self.controller = controller.Controller(self.view, self.capture_window, self.login_dialog)

    def __get_parent(self):

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return None

        if sys.version_info.major == 2:
            parent = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            # Maya2022-
            parent = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        if parent is None:
            return None

        return parent

    def __delete_overlapping_window(self, target_list):
        """Windowの重複削除処理
        """

        if self.parent is None:
            return

        for widget in self.parent.children():
            for target in target_list:
                if type(target) == type(widget):
                    widget.deleteLater()

    def show_ui(self):
        """[summary]
        """

        if not self.controller.check_loading_shotgun_api_module():
            return

        self.setup_event()

        self.controller.load_ui_setting()

        self.view.show()

        self.controller.setup_scene_reload_scriptjob()

        self.controller.update_asset_data_view()

        if not self.controller.is_sg_setting_setup_finished:
            self.controller.show_login_dialog()

    def mainwindow_close_event(self):
        """[summary]
        """
        self.controller.save_ui_setting()
        self.__delete_overlapping_window([view.View(), view.CaptureWindow(), view.ShotgridLoginDialog()])

    def setup_event(self):
        """UIのevent設定
        """

        # CloseEvent時の実行イベント
        # 関数渡すとそれを実行する
        self.view.close_event_exec = self.mainwindow_close_event

        self.login_dialog.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(
            lambda: self.controller.set_sg_account_info_for_dialog())

        self.view.ui.login_status.triggered.connect(lambda: self.controller.show_login_dialog())

        # 共通設定
        self.view.ui.open_target_dir_button.clicked.connect(
            lambda: self.controller.open_target_dir_for_ui(self.view.ui.target_dir_line))
        self.view.ui.set_target_dir_button.clicked.connect(
            lambda: self.controller.set_target_dir_to_ui(self.view.ui.target_dir_line))

        self.view.ui.sg_asset_add_button.clicked.connect(
            lambda: self.controller.register_new_asset())

        # ScreenShot
        self.view.ui.ss_register_sg_button.clicked.connect(
            lambda: self.capture_window.show())

        # PlayBlast
        self.view.ui.pb_register_sg_button.clicked.connect(
            lambda: self.controller.register_playblast_movie())

        # capture_window
        self.capture_window.captureButton.clicked.connect(
            lambda: self.controller.register_screenshot())


if __name__ == '__main__':

    main = Main()
    main.show_ui()
