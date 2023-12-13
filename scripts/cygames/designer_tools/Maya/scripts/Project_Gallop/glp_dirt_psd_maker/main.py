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

from .. import base_common
from ..base_common import utility as base_utility
from .. import glp_common

from . import make_dirt_psd
from . import view
from . import modal_view

reload(base_common)
reload(glp_common)
reload(make_dirt_psd)


# ==================================================
def main():
    exporter = Main()
    exporter.create_ui()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ==================================================
    def __init__(self):

        self.tool_version = '21061101'
        self.tool_name = 'GallopDirtMaker'

        self.dirt_ref_dir_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/common/dirt_temp/scenes'
        self.dirt_ref_file_name = 'capsule_temp.ma'
        self.default_name_space = '__dirt_ref__'

        self.window_name = self.tool_name + 'Win'

        self.view = view.View()

    # ==================================================
    def deleteOverlappingWindow(self, target):
        '''Windowの重複削除処理
        '''

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
                widget.deleteLater()

    # ==================================================
    def create_ui(self):
        '''ui作成
        '''
        
        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)

        self.setup_view_event()

        # デフォルトのdirtリファレンスのパスをテキストボックスに入れておく
        self.view.ui.loadDirtRefEditLE.setText('{0}/{1}'.format(self.dirt_ref_dir_path, self.dirt_ref_file_name))

        self.view.show()

    # ==================================================
    def setup_view_event(self):

        # なぜかわかりませんが、lambdaで渡さないとうまく動かないことがある
        self.view.ui.loadDirtRefLoadBtn.clicked.connect(lambda: self.__load_dirt_reference())
        self.view.ui.transcriptDirtBtn.clicked.connect(lambda: self.__make_dirt_texture())

        self.view.ui.loadDirtRefEditSelectBtn.clicked.connect(lambda: self.__select_data_path_from_ui())
        self.view.ui.loadDirtRefEditOpenBtn.clicked.connect(lambda: self.__open_explorer_from_ui())
        self.view.ui.loadDirtRefEditCheckBtn.clicked.connect(lambda: self.__check_path_from_ui())

    # ==================================================
    def __select_data_path_from_ui(self):

        file_filter = 'All Files(*.*)'

        current_file_path = self.view.ui.loadDirtRefEditLE.text()
        current_dir_path = ''
        if current_file_path:
            if os.path.isfile(current_file_path):
                current_dir_path = \
                    os.path.dirname(current_file_path).replace('\\', '/')
            else:
                current_dir_path = current_file_path.replace('\\', '/')

        select_file_path, file_filter = QtWidgets.QFileDialog.getOpenFileName(self.view, 'select file', current_dir_path, file_filter, file_filter)

        if not select_file_path:
            return

        self.view.ui.loadDirtRefEditLE.setText(select_file_path)

    # ==================================================
    def __open_explorer_from_ui(self):
        base_utility.io.open_directory(self.view.ui.loadDirtRefEditLE.text())

    # ==================================================
    def __check_path_from_ui(self):

        q_ans = QtWidgets.QMessageBox.question(self.view, '確認', '対象データを確認しますか')
        if not q_ans == QtWidgets.QMessageBox.Yes:
            return
        
        data_path_list = self.__get_data_path_list(self.view.ui.loadDirtRefEditLE.text())

        if not data_path_list:
            QtWidgets.QMessageBox.information(self.view, '対象データリスト', '対象データがありません')
            return

        self.show_modal(data_path_list)

    # ==================================================
    def show_modal(self, data):

        custom_modal = modal_view.View()

        temp_text = ''
        item_count = 0
        for item in data:
            temp_text += item + '\n'
            item_count += 1

        custom_modal.ui.dataOutputArea.setPlainText(temp_text)
        custom_modal.ui.countLbl.setText('リスト数:{0}'.format(str(item_count)))

        custom_modal.exec_()

    # ==================================================
    def __get_data_path_list(self, target_data_path):

        target_data_path_list = []

        if not target_data_path:
            return

        if os.path.isdir(target_data_path):
            target_dir_path = target_data_path.replace('\\', '/')

            for root, dirs, files in os.walk(target_dir_path):
                
                this_root_path = root.replace('\\', '/')

                if this_root_path.find('/.') >= 0:
                    continue
                
                for this_file in files:
                    this_file_path = os.path.join(root, this_file).replace('\\', '/')
                    target_data_path_list.append(this_file_path)

        elif os.path.isfile(target_data_path):
            target_file_path = target_data_path.replace('\\', '/')
            target_data_path_list.append(target_file_path)

        return target_data_path_list

    # ==================================================
    def __load_dirt_reference(self):

        target_path = self.view.ui.loadDirtRefEditLE.text()

        if not os.path.exists(target_path):
            cmds.warning('リファレンスファイルが見つかりません。Dirtリファレンスのパスを確認してください。')
            return

        base_utility.reference.load(target_path, self.default_name_space)

    # ==================================================
    def __make_dirt_texture(self):

        dirt_maker = make_dirt_psd.MakeDirt()
        dirt_maker.make_dirt_psd()
