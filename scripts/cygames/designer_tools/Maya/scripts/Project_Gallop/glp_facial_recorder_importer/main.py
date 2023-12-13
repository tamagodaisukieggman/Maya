# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
    from importlib import reload
except Exception:
    pass

import os
import sys

import maya.cmds as cmds
from maya import OpenMayaUI

import shiboken2
from PySide2 import QtWidgets
from . import glp_facial_importer_gui
from . import glp_facial_importer_root

reload(glp_facial_importer_root)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ===============================================
    def __init__(self):

        self.main_window = glp_facial_importer_gui.GUI()
        self.importer_root = glp_facial_importer_root.GlpFacialImporterRoot()

        self.TITLE_SEPARATOR = '=' * 20

    # ===============================================
    def show_ui(self):
        """UIの呼び出し
        """

        self.deleteOverlappingWindow(self.main_window)
        self.__setup_view_event()
        self.main_window.show()

        self.__initialize_ui()

    # ===============================================
    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(
                long(main_window), QtWidgets.QMainWindow)
        else:
            # for Maya 2022-
            main_window = shiboken2.wrapInstance(
                int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if type(target) == type(widget):
                widget.close()
                widget.deleteLater()

    # ===============================================
    def __setup_view_event(self):

        self.main_window.ui.select_dir_button.clicked.connect(self.select_dir_button_event)
        self.main_window.ui.show_info_button.clicked.connect(self.show_info_button_event)
        self.main_window.ui.get_crrent_frame_button.clicked.connect(self.get_crrent_frame_button_event)
        self.main_window.ui.get_current_target_button.clicked.connect(self.get_current_target_button_event)
        self.main_window.ui.bake_start_button.clicked.connect(self.bake_start_button_event)

    # ===============================================
    def __initialize_ui(self, arg=None):

        self.main_window.ui.start_option_edit.setText(str(0))
        self.main_window.ui.target_option_edit.setText(self.importer_root.FACIAL_CTRL_ROOT)

    # ===============================================
    def select_dir_button_event(self):

        select_dir = cmds.fileDialog2(fm=3)

        if select_dir:
            self.main_window.ui.import_dir_edit_text.setText(select_dir[0])

    # ===============================================
    def show_info_button_event(self):

        self.clear_log()
        check_ok = 'ベイク可能です'
        check_ng = 'ベイク出来ません　パスを確認してください'

        log_str = ''
        log_str += self.TITLE_SEPARATOR + '\n'
        log_str += '記録データ情報' + '\n'
        log_str += self.TITLE_SEPARATOR + '\n'

        data_dir_path = self.main_window.ui.import_dir_edit_text.text()

        if not os.path.exists(data_dir_path):
            log_str += 'ディレクトリが存在していません'
            log_str = check_ng + '\n\n' + log_str
            self.write_log(log_str)
            return

        self.importer_root.initialize(data_dir_path, self)

        # ドリブンキーの情報
        log_str += 'データファイル情報' + '\n'

        if not self.importer_root.driven_key_info_data_path_list:
            log_str += '記録ファイルがみつかりませんでした'
            log_str = check_ng + '\n\n' + log_str
            self.write_log(log_str)
            return
        else:
            for data_path in self.importer_root.driven_key_info_data_path_list:
                log_str += os.path.basename(data_path) + '\n'

        log_str += '\n'

        # 時間の情報
        log_str += '記録時間情報' + '\n'

        if not self.importer_root.frame_time_dict_list:
            log_str += '時間記録が取得できませんでした'
            log_str = check_ng + '\n\n' + log_str
            self.write_log(log_str)
            return
        else:
            last_time = self.importer_root.frame_time_dict_list[-1]['time']
            frame_count = len(self.importer_root.frame_time_dict_list)
            log_str += 'サンプリング時間 : {}秒'.format(last_time) + '\n'
            log_str += '現在のfpsでのフレーム数 : {}フレーム'.format(frame_count) + '\n'

        log_str = check_ok + '\n\n' + log_str
        self.write_log(log_str)

    # ===============================================
    def get_crrent_frame_button_event(self):

        current_frame = cmds.currentTime(q=True)
        self.main_window.ui.start_option_edit.setText(str(int(current_frame)))

    # ===============================================
    def get_current_target_button_event(self):

        current_select = cmds.ls(sl=True, type='transform', l=True)

        if current_select:
            self.main_window.ui.target_option_edit.setText(current_select[0])

    # ===============================================
    def bake_start_button_event(self):

        self.clear_log()
        log_str = ''
        log_str += self.TITLE_SEPARATOR + '\n'
        log_str += 'ベイク開始' + '\n'
        log_str += self.TITLE_SEPARATOR

        self.write_log(log_str)

        data_dir_path = self.main_window.ui.import_dir_edit_text.text()
        self.importer_root.initialize(data_dir_path, self)

        frame_offset = 0
        try:
            frame_offset = int(self.main_window.ui.start_option_edit.text())
        except Exception:
            pass

        target_root = self.main_window.ui.target_option_edit.text()

        result = self.importer_root.bake_facial(frame_offset, target_root)

        if result:
            self.write_log('ベイク完了')
        else:
            self.write_log('ベイクを中止しました')

    # ===============================================
    def clear_log(self):

        self.main_window.ui.log_edit.clear()

    # ===============================================
    def write_log(self, text, should_append=True):

        if should_append:
            self.main_window.ui.log_edit.append(text)
        else:
            self.main_window.ui.log_edit.setText(text)

        cmds.refresh(cv=True)
