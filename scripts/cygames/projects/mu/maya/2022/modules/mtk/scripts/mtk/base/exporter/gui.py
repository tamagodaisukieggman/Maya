# -*- coding: utf-8 -*-
u"""FBX Exporter (GUI)

.. END__CYGAMES_DESCRIPTION
"""
import os
import re
from distutils.util import strtobool

try:
    from PySide2.QtCore import Qt
except ImportError:
    from PySide.QtCore import Qt
import maya.cmds as cmds

from mtku.maya.base.window import BaseWindow
from mtku.maya.constant import MTK_MAYA_MANUAL_HELP_URL
from mtku.maya.log import MtkDBLog
from mtk.utils import getCurrentSceneFilePath


logger = MtkDBLog(__name__)


class BaseExporter(BaseWindow):

    def __init__(self, *args, **kwargs):
        super(BaseExporter, self).__init__(*args, **kwargs)

        self.common_ui = None
        self.common_ui_file = '{0}/exporter.ui'.format(os.path.dirname(__file__))
        self.url = '{}/file/fbxexporter.html'.format(MTK_MAYA_MANUAL_HELP_URL)

        self.width = 600
        self._key_directory = '{}.directory'.format(__package__)
        self._key_bookmarks = '{}.bookmarks'.format(__package__)
        self._key_can_checkout_ma = '{}.can_checkout_ma'.format(__package__)
        self._key_can_checkout_fbx = '{}.can_checkout_fbx'.format(__package__)
        self._key_can_validate = '{}.can_validate'.format(__package__)

        self.mode = kwargs.setdefault('mode', 0)

    def create(self):
        u"""Windowのレイアウト作成"""
        self._add_common_layout()
        # 設定値の読み込み
        self.read_settings()
        # コマンドの接続
        self._connect()
        # UIの設定値変更
        self.edit_settings()
        # イベント設定
        self.event_scene_opened()

    def show(self, *args):
        u"""Windowの表示"""
        windows = ('CharaExporter', 'EnvExporter', 'MotionExporter', 'OldMotionExporter')
        for _window in windows:
            if cmds.window(_window, ex=True):
                cmds.deleteUI(_window)

        super(BaseExporter, self).show()

    def _add_common_layout(self):
        frame_layout = cmds.frameLayout(l='FBX')
        self.common_ui = self.load_file(self.common_ui_file, frame_layout)
        cmds.setParent('..')

    def help(self, *args):
        u"""help表示"""
        cmds.showHelp(self.url, a=True)

    def _connect(self):
        if self.mode == 0:
            self.common_ui.line_edit_directory.textChanged.connect(self.save_settings)
            self.common_ui.push_button_browse_directory.clicked.connect(self._browse_directory)

        # self.common_ui.push_button_add_bookmark.clicked.connect(self._add_bookmark)
        self.common_ui.check_box_can_checkout_ma.clicked.connect(self.save_settings)
        self.common_ui.check_box_can_checkout_fbx.clicked.connect(self.save_settings)
        self.common_ui.check_box_checker.clicked.connect(self.save_settings)

    # ########################################
    # PySide
    # ########################################
    def is_checked_q_check_box(self, q_check_box):
        u"""QCheckBoxがONかどうか

        :param q_check_box: QCheckBox
        :return: bool
        """
        if q_check_box.checkState() == Qt.CheckState.Checked:
            return True
        else:
            return False

    def set_q_check_box(self, q_check_box, value):
        u"""QCheckBoxのON/OFFの設定

        bool値(文字列も可)を渡してQCheckBoxのON/OFFを設定する

        :param q_check_box: QCheckBox
        :param value: bool (文字列も可)
        """
        bool_value = strtobool(str(value))
        if bool_value:
            q_check_box.setCheckState(Qt.CheckState.Checked)
        else:
            q_check_box.setCheckState(Qt.CheckState.Unchecked)

    # ########################################
    # Settings
    # ########################################
    def save_settings(self, *args):
        u"""設定の保存"""
        settings = {}

        if self.mode == 0:
            settings[self._key_directory] = self.common_ui.line_edit_directory.text()
        settings[self._key_can_checkout_ma] = (
            self.is_checked_q_check_box(self.common_ui.check_box_can_checkout_ma)
        )
        settings[self._key_can_checkout_fbx] = (
            self.is_checked_q_check_box(self.common_ui.check_box_can_checkout_fbx)
        )
        settings[self._key_can_validate] = (
            self.is_checked_q_check_box(self.common_ui.check_box_checker)
        )

        [cmds.optionVar(sv=(k, v)) for k, v in settings.items()]

        return settings

    def reset_settings(self, *args):
        u"""設定のリセット"""
        if self.mode == 0:
            self.common_ui.line_edit_directory.setText(self._get_output_dir_from_scene())
        self.set_q_check_box(self.common_ui.check_box_can_checkout_ma, False)
        self.set_q_check_box(self.common_ui.check_box_can_checkout_fbx, True)
        self.set_q_check_box(self.common_ui.check_box_checker, True)
        # リセット後に設定を保存
        self.save_settings()

    def read_settings(self):
        u"""設定の読み込み"""
        output_dir = str(cmds.optionVar(q=self._key_directory))
        output_dir = re.sub(r'\\', '/', output_dir)
        can_checkout_ma = strtobool(str(cmds.optionVar(q=self._key_can_checkout_ma)))
        can_checkout_fbx = strtobool(str(cmds.optionVar(q=self._key_can_checkout_fbx)))
        can_validate = strtobool(str(cmds.optionVar(q=self._key_can_validate)))
        if self.mode == 0:
            self.common_ui.line_edit_directory.setText(output_dir) if output_dir else None

        self.set_q_check_box(self.common_ui.check_box_can_checkout_ma, can_checkout_ma)
        self.set_q_check_box(self.common_ui.check_box_can_checkout_fbx, can_checkout_fbx)
        self.set_q_check_box(self.common_ui.check_box_checker, can_validate)

        return {
            'output_dir': output_dir,
            'can_checkout_ma': can_checkout_ma,
            'can_checkout_fbx': can_checkout_fbx,
            'can_validate': can_validate,
        }

    def edit_settings(self, *args):
        u"""currentのシーンに合わせてUIの値を適切に設定"""
        if self.mode == 0:
            self.common_ui.line_edit_directory.setText(self._get_output_dir_from_scene())

    # ########################################
    # Command
    # ########################################
    def _browse_directory(self, *args):
        starting_directory = self.common_ui.line_edit_directory.text()
        dirs = cmds.fileDialog2(ds=2, fm=3, okc='Set', dir=starting_directory)
        if dirs:
            self.common_ui.line_edit_directory.setText(dirs[0])

    def _add_bookmark(self, *args):
        bookmarks_str = cmds.optionVar(q=self._key_bookmarks)
        bookmark_str = self.common_ui.line_edit_directory.text()

        if type(bookmark_str) == 'str':
            bookmarks_str += ';{}'.format(bookmark_str)
        else:
            bookmarks_str = bookmark_str[:]
        cmds.optionVar(sv=(self._key_bookmarks, bookmarks_str))

        bookmarks = bookmarks_str.split(';')
        self.common_ui.combo_box_bookmarks.clear()
        self.common_ui.combo_box_bookmarks.addItems(bookmarks)

    def _get_output_dir_from_scene(self):
        u"""Mayaシーンからuassetの出力フォルダを取得

        :return: 出力フォルダのパス
        """
        maya_scene_path = getCurrentSceneFilePath()
        if not maya_scene_path:
            return ''

        output_root = os.path.dirname(os.path.dirname(maya_scene_path))
        dir_path = '{}/uassets'.format(output_root)
        return dir_path

    # ########################################
    # Event
    # ########################################
    def _event_set_line_edit_directory(self, *args):
        dir_path = self._get_output_dir_from_scene()
        if not dir_path:
            return
        logger.debug(dir_path)
        self.common_ui.line_edit_directory.setText(dir_path)

    def event_scene_opened(self):
        u"""MayaシーンOpen時に実行されるイベント"""
        # 出力先を自動でセット
        cmds.scriptJob(e=['SceneOpened', self._event_set_line_edit_directory], p=self.window)
