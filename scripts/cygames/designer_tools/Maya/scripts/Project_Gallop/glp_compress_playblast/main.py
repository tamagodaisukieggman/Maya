# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except Exception:
    pass

import os
import sys
import re
import glob
import time

import maya.cmds as cmds
from maya import OpenMayaUI
from maya.app.general import mayaMixin

import random
import shiboken2
from PySide2.QtCore import Qt
from PySide2.QtCore import QSettings
from PySide2 import QtGui, QtWidgets
from . import glp_compress_playblast_gui
from . import movie_compresser


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ===============================================
    def __init__(self):

        self.PATH_OPTION_VAR = 'GlpCompressPlayblastPathVar'
        self.KEEP_ORIGINAL_OPTION_VAR = 'GlpCompressPlayblastKeepOrgVar'
        self.START_TIME_OPTION_VAR = 'GlpCompressPlayblastStartTimeVar'
        self.VIEW_MP4_OPTION_VAR = 'GlpCompressPlayblastViewMp4Var'
        self.START_BUTTON_LABEL = 'プレイブラスト圧縮を開始'
        self.STOP_BUTTON_LABEL = 'プレイブラスト圧縮を停止'
        self.RED_COLOR_CODE = '#880000'
        self.GREEN_COLOR_CODE = 'green'

        self.is_enable_compression = False
        self.main_window = glp_compress_playblast_gui.GUI()
        self.script_job_num = None

        self.movie_compresser = movie_compresser.MovieCompresser()
        self.is_import_ok = self.movie_compresser.is_module_imported

    # ===============================================
    def show_ui(self):
        '''UIの呼び出し
        '''

        self.deleteOverlappingWindow(self.main_window)
        self.__setup_view_event()
        self.main_window.show()

        self.__initialize_ui()

    # ===============================================
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
                widget.close()
                widget.deleteLater()

    # ===============================================
    def __setup_view_event(self):

        self.main_window.ui.target_dir.textChanged.connect(self.__target_dir_text_event)
        self.main_window.ui.should_keep_original.stateChanged.connect(self.__keep_original_check_event)
        self.main_window.ui.should_open_mp4.stateChanged.connect(self.__view_mp4_check_event)
        self.main_window.ui.compress_switch.clicked.connect(self.__compress_switch_event)
        self.main_window.ui.open_dir.clicked.connect(self.__open_dir_event)

    # ===============================================
    def __initialize_ui(self, arg=None):

        self.main_window.ui.compress_switch.setText(self.START_BUTTON_LABEL)
        self.main_window.ui.compress_switch.setStyleSheet('background-color: {};'.format(self.GREEN_COLOR_CODE))

        # option varからの初期化
        # 対象パス
        path_option_var = self.__get_option_var(self.PATH_OPTION_VAR)
        if path_option_var:
            self.main_window.ui.target_dir.setText(path_option_var)

        keep_original_option_var = self.__get_option_var(self.KEEP_ORIGINAL_OPTION_VAR)

        # 元avi保持
        if keep_original_option_var is None:
            self.__set_option_var(self.KEEP_ORIGINAL_OPTION_VAR, 'False')
            keep_original_option_var = self.__get_option_var(self.KEEP_ORIGINAL_OPTION_VAR)

        if keep_original_option_var == 'True':
            self.main_window.ui.should_keep_original.setChecked(True)
        else:
            self.main_window.ui.should_keep_original.setChecked(False)

        # 圧縮mp4を開くか
        view_mp4 = self.__get_option_var(self.VIEW_MP4_OPTION_VAR)

        if view_mp4 is None:
            self.__set_option_var(self.VIEW_MP4_OPTION_VAR, 'True')
            view_mp4 = self.__get_option_var(self.VIEW_MP4_OPTION_VAR)

        if view_mp4 == 'True':
            self.main_window.ui.should_open_mp4.setChecked(True)
        else:
            self.main_window.ui.should_open_mp4.setChecked(False)

        # デフォルトで圧縮をオンにしておく
        if not self.is_enable_compression:
            self.__compress_switch_event()

        self.__update_info()

    # ===============================================
    def __target_dir_text_event(self, arg=None):

        self.__set_option_var(self.PATH_OPTION_VAR, self.main_window.ui.target_dir.text())
        current_time = time.time()
        self.__set_option_var(self.START_TIME_OPTION_VAR, current_time)
        self.__update_info()

    # ===============================================
    def __check_path(self):

        option_var = self.__get_option_var(self.PATH_OPTION_VAR)

        if not option_var:
            return False

        if self.main_window.ui.target_dir.text() == option_var:
            return True
        else:
            return False

    # ===============================================
    def __keep_original_check_event(self, arg=None):

        if self.main_window.ui.should_keep_original.isChecked():
            self.__set_option_var(self.KEEP_ORIGINAL_OPTION_VAR, 'True')
        else:
            self.__set_option_var(self.KEEP_ORIGINAL_OPTION_VAR, 'False')

        current_time = time.time()
        self.__set_option_var(self.START_TIME_OPTION_VAR, current_time)
        self.__update_info()

    # ===============================================
    def __view_mp4_check_event(self, arg=None):

        if self.main_window.ui.should_open_mp4.isChecked():
            self.__set_option_var(self.VIEW_MP4_OPTION_VAR, 'True')
        else:
            self.__set_option_var(self.VIEW_MP4_OPTION_VAR, 'False')

    # ===============================================
    def __compress_switch_event(self, arg=None):

        if not self.is_import_ok:
            return

        if not self.is_enable_compression:
            self.is_enable_compression = True
        else:
            self.is_enable_compression = False

        if self.is_enable_compression:
            self.main_window.ui.compress_switch.setText(self.STOP_BUTTON_LABEL)
        else:
            self.main_window.ui.compress_switch.setText(self.START_BUTTON_LABEL)

        if self.is_enable_compression:

            # ツールの開始時間を記録。これ以降のプレイブラスト書き出しaviを対象にする
            current_time = time.time()
            self.__set_option_var(self.START_TIME_OPTION_VAR, current_time)

            self.__create_script_job()
            self.main_window.ui.compress_switch.setStyleSheet('background-color: {};'.format(self.RED_COLOR_CODE))
        else:
            self.__delete_script_job()
            self.main_window.ui.compress_switch.setStyleSheet('background-color: {};'.format(self.GREEN_COLOR_CODE))

        self.__update_info()

    # ===============================================
    def __create_script_job(self):

        self.script_job_num = cmds.scriptJob(cf=['playblasting', self.compress_avi_script_job], p=self.main_window.objectName())
        print('create job : {}'.format(self.script_job_num))

    # ===============================================
    def __delete_script_job(self):

        if self.script_job_num is None:
            return

        if not cmds.scriptJob(ex=self.script_job_num):
            return

        cmds.scriptJob(kill=self.script_job_num, f=True)
        print('delete job : {}'.format(self.script_job_num))

        self.script_job_num = None

    # ===============================================
    def __open_dir_event(self, arg=None):

        path = self.__get_option_var(self.PATH_OPTION_VAR)

        if not os.path.exists(path):
            return

        try:
            os.startfile(path)
        except Exception:
            print('開けませんでした')

    # ===============================================
    def __update_info(self):

        if not self.is_import_ok:
            self.main_window.ui.info_text.setPlainText(
                '必要なモジュールのインポートに失敗しました\ngallop_maya_bootのバッチからMayaを起動していることを確認してください'
            )
            return

        state_info = ''
        if self.is_enable_compression:
            state_info = '圧縮設定が適用中：「{}」ボタンを押すかウインドウを閉じると圧縮設定を停止します'.format(self.STOP_BUTTON_LABEL)
        else:
            state_info = '「{}」ボタンを押して圧縮設定を適用します'.format(self.START_BUTTON_LABEL)

        path = self.__get_option_var(self.PATH_OPTION_VAR)
        keep_original_option_var = self.__get_option_var(self.KEEP_ORIGINAL_OPTION_VAR)

        path_info = ''
        if not path:
            path_info = '圧縮対象にするディレクトリのパスが指定されていません'
        else:
            path_info = '圧縮設定適用中は以下のディレクトリに出力されたaviファイルをmp4に圧縮します\n{}'.format(path)

        keep_original_info = ''
        if keep_original_option_var == 'True':
            keep_original_info = 'オリジナルのaviファイルを保持します'
        else:
            keep_original_info = 'オリジナルのaviファイルは圧縮後に削除されます\n(※削除ファイルを再生しようとするため、プレイブラストオプションのViewはオフにしてください)'

        final_text = '{}\n\n{}\n{}'.format(state_info, path_info, keep_original_info)
        self.main_window.ui.info_text.setPlainText(final_text)

    # ===============================================
    def __get_option_var(self, option_var):

        if not cmds.optionVar(exists=option_var):
            return None

        return cmds.optionVar(q=option_var)

    # ===============================================
    def __set_option_var(self, option_var, value):

        cmds.optionVar(sv=[option_var, str(value)])

    # ===============================================
    def compress_avi_script_job(self):
        '''scriptJobに送るメソッド
        '''

        if not cmds.optionVar(exists='GlpCompressPlayblastPathVar'):
            return

        target_dir_path = cmds.optionVar(q='GlpCompressPlayblastPathVar')

        if not os.path.exists(target_dir_path):
            return

        avi_list = glob.glob('{}/*.avi'.format(target_dir_path))

        start_time = 0.0
        if cmds.optionVar(exists='GlpCompressPlayblastStartTimeVar'):
            start_time = float(cmds.optionVar(q='GlpCompressPlayblastStartTimeVar'))

        should_view_mp4 = False
        if cmds.optionVar(exists='GlpCompressPlayblastViewMp4Var') and cmds.optionVar(q='GlpCompressPlayblastViewMp4Var') == 'True':
            should_view_mp4 = True

        if not avi_list:
            return
        elif len(avi_list) > 1:
            # 複数ファイル圧縮時は必ず再生しない
            should_view_mp4 = False

        remove_org_avi = False
        if cmds.optionVar(q='GlpCompressPlayblastKeepOrgVar') == 'False':
            remove_org_avi = True

        for avi_path in avi_list:

            print('=' * 20)
            print('{}の処理を開始'.format(avi_path))

            # 判定のためにaviの作成日時を取得
            avi_mtime = os.path.getmtime(avi_path)

            mp4_path = avi_path.replace('.avi', '.mp4')

            # 既にaviより新しいmp4があればスキップ
            if os.path.exists(mp4_path):
                mp4_mtime = os.path.getmtime(mp4_path)

                if avi_mtime < mp4_mtime:
                    print('変換済スキップ：avi_mtime={}, mp4_mtime={}'.format(avi_mtime, mp4_mtime))
                    continue

            # ツールスタート前のaviはスキップ
            if avi_mtime < start_time:
                print('古いaviのためスキップ：avi_mtime={}, start_time={}'.format(avi_mtime, start_time))
                continue

            self.movie_compresser.compress_avi_to_mp4(avi_path, mp4_path, remove_org_avi, should_view_mp4)

        # 次回の圧縮対象ファイルの開始期間を更新
        current_time = time.time()
        cmds.optionVar(sv=['GlpCompressPlayblastStartTimeVar', str(current_time)])
