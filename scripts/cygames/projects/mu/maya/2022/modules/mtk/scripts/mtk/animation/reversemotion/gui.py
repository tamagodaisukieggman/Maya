# -*- coding: utf-8 -*-
u"""モーション反転ツール(GUI)

..
    END__CYGAMES_DESCRIPTION
"""

import codecs
import os
from distutils.util import strtobool
from functools import partial

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication
except ImportError:
    from PySide.QtCore import Qt
    from PySide.QtGui import QApplication

import maya.cmds as cmds
import maya.mel as mel

from mtk.base.window import BaseWindow
import mtk.utils.mayabatch as mayabatch
import logging
# from mtku.maya.mtklog import MtkLog
from .command import ReverseMotionCmd
from mtk.utils import getCurrentSceneFilePath


# logger = MtkLog(__name__)
logger = logging.getLogger(__name__)


class ReverseMotion(BaseWindow):

    def __init__(self, *args, **kwargs):
        u"""初期化"""
        super(ReverseMotion, self).__init__(*args, **kwargs)

        self.ui = None
        self.url = 'https://wisdom.cygames.jp/pages/viewpage.action?pageId=30421204'

        self._tool_name = 'reversemotion'
        self.title = 'ReverseMotion'

        self._key_type = '{}.type'.format(__package__)
        self._key_axis = '{}.axis'.format(__package__)
        self._key_right_id = '{}.right_id'.format(__package__)
        self._key_left_id = '{}.left_id'.format(__package__)

        self._key_mode = '{}.mode'.format(__package__)
        self._key_can_save = '{}.can_save'.format(__package__)
        self._key_dirname = '{}.dirname'.format(__package__)

        self.width = 630
        self.height = 440

    def create(self):
        u"""Windowのレイアウト作成"""
        dirpath = os.path.dirname(__file__)
        ui_file = '{0}/{1}.ui'.format(dirpath, self._tool_name)
        self.ui = self.load_file(ui_file)
        self._add_menus()
        self.read_settings()
        self._change_type_event()
        self._change_mode_event()
        self._connect()

    def _add_execform(self):
        u"""Apply Closeボタンの追加

        :return: フォーム名
        """
        execform = cmds.formLayout(nd=100)

        export_scene_btn = cmds.button(l=u'現在のシーンを反転', h=26, c=self._apply_scene)
        export_wf_btn = cmds.button(
            l=u'WorkFilerで選択したファイルを反転', h=26, c=self._apply_workfiler
        )
        close_btn = cmds.button(l='Close', h=26, c=self.close)

        # レイアウト
        cmds.formLayout(
            execform, e=True,
            af=(
                [export_scene_btn, 'left', 0],
                [export_scene_btn, 'bottom', 5],
                [export_wf_btn, 'bottom', 5],
                [close_btn, 'bottom', 5],
                [close_btn, 'right', 0],
            ),
            ap=(
                [export_scene_btn, 'right', 1, 33],
                [close_btn, 'left', 0, 67],
            ),
            ac=(
                [export_wf_btn, 'left', 4, export_scene_btn],
                [export_wf_btn, 'right', 4, close_btn],
            ),
        )

        cmds.setParent('..')  # execform
        return execform

    def _add_menus(self):
        u"""メニューアイテムを追加"""
        menu_debug = self.add_menu('Debug')
        self.add_menuitem(u'コントローラーのリセット', menu_debug, ReverseMotionCmd.debug_reset_controller)
        self.add_menuitem(u'コントローラーの情報を表示', menu_debug, ReverseMotionCmd.debug_show_info)
        self.add_menuitem(u'コントローラーの情報を表示(behaviorのみ)', menu_debug, partial(ReverseMotionCmd.debug_show_info, mode=1))
        self.add_menuitem(
            u'コントローラーの情報を表示(leftノードのみ)',
            menu_debug,
            partial(ReverseMotionCmd.debug_show_info, displays_left_only=True),
        )
        self.add_menuitem(
            u'コントローラーの情報を表示(behavior, leftノードのみ)',
            menu_debug,
            partial(ReverseMotionCmd.debug_show_info, mode=1, displays_left_only=True),
        )

    def read_settings(self, *args):
        u"""設定の読み込み"""
        axis = cmds.optionVar(q=self._key_axis)
        right_id = cmds.optionVar(q=self._key_right_id)
        left_id = cmds.optionVar(q=self._key_left_id)

        typ = cmds.optionVar(q=self._key_type)
        mode = cmds.optionVar(q=self._key_mode)
        # can_exec_bg = strtobool(str(cmds.optionVar(q=self._key_can_exec_bg)))
        can_save = strtobool(str(cmds.optionVar(q=self._key_can_save)))
        dirpath = cmds.optionVar(q=self._key_dirname)

        if typ == 'local':
            self.ui.radio_button_local.setChecked(True)
        else:
            self.ui.radio_button_world.setChecked(True)

        if axis == 'x':
            self.ui.radio_button_x.setChecked(True)
        elif axis == 'y':
            self.ui.radio_button_y.setChecked(True)
        else:
            self.ui.radio_button_z.setChecked(True)

        if right_id:
            self.ui.line_edit_right_id.setText(right_id)
        if left_id:
            self.ui.line_edit_left_id.setText(left_id)

        if mode == 'pose':
            self.ui.radio_button_pose.setChecked(True)
        else:
            self.ui.radio_button_motion.setChecked(True)
        if can_save:
            self.ui.checkbox_can_save.setChecked(True)
        else:
            self.ui.checkbox_can_save.setChecked(False)
        if dirpath:
            self.ui.line_edit_dirname.setText(dirpath)

    def save_settings(self, *args):
        u"""設定の保存

        :return: 設定 (dict)
        """
        settings = {
            self._key_type: self._get_type_from_ui(),
            self._key_axis: self._get_axis_from_ui(),
            self._key_right_id: self.ui.line_edit_right_id.text(),
            self._key_left_id: self.ui.line_edit_left_id.text(),
            self._key_mode: self._get_mode_from_ui(),
            self._key_can_save: self._is_checked_qcheckbox(self.ui.checkbox_can_save),
            self._key_dirname: self.ui.line_edit_dirname.text(),
        }

        # mayaPrefs.melに保存
        [cmds.optionVar(sv=(k, v)) for k, v in settings.items()]
        logger.debug(settings)
        return settings

    def reset_settings(self, *args):
        u"""設定のリセット"""
        self.ui.radio_button_local.setChecked(True)
        self.ui.radio_button_world.setChecked(False)

        self.ui.radio_button_x.setChecked(True)
        self.ui.radio_button_y.setChecked(False)
        self.ui.radio_button_z.setChecked(False)

        self.ui.line_edit_left_id.setText('_L_')
        self.ui.line_edit_right_id.setText('_R_')

        self.ui.radio_button_pose.setChecked(True)
        self.ui.radio_button_motion.setChecked(False)

        self.ui.checkbox_can_save.setChecked(True)
        self.ui.line_edit_dirname.setText('')
        # リセット後に設定を保存
        self.save_settings()

    def _get_type_from_ui(self):
        u"""ラジオボタンで選択している軸の取得

        :return: 軸
        """
        if self.ui.radio_button_local.isChecked():
            typ = 'local'
        elif self.ui.radio_button_world.isChecked():
            typ = 'world'
        else:
            typ = 'both'
        return typ

    def _get_axis_from_ui(self):
        u"""ラジオボタンで選択している軸の取得

        :return: 軸
        """
        if self.ui.radio_button_x.isChecked():
            axis = 'x'
        elif self.ui.radio_button_y.isChecked():
            axis = 'y'
        else:
            axis = 'z'
        return axis

    def _get_mode_from_ui(self):
        u"""ラジオボタンで選択している実行モードの取得

        :return: モード
        """
        if self.ui.radio_button_pose.isChecked():
            mode = 'pose'
        else:
            mode = 'motion'
        return mode

    def _change_type_event(self, *args):
        u"""Typeのラジオボタン変更時に実行されるコマンド"""
        if self.ui.radio_button_local.isChecked():
            self.ui.radio_button_x.setEnabled(False)
            self.ui.radio_button_z.setEnabled(False)
        else:
            self.ui.radio_button_x.setEnabled(True)
            self.ui.radio_button_z.setEnabled(True)

    def _change_mode_event(self, *args):
        u"""Modeのラジオボタン変更時に実行されるコマンド"""
        if self.ui.radio_button_pose.isChecked():
            self.ui.checkbox_can_bake.setEnabled(False)
            self.ui.checkbox_can_save.setEnabled(False)
            self.ui.line_edit_dirname.setEnabled(False)
        else:
            self.ui.checkbox_can_bake.setEnabled(True)
            self.ui.checkbox_can_save.setEnabled(True)
            self.ui.line_edit_dirname.setEnabled(True)

    def _is_checked_qcheckbox(self, qcheckbox):
        u"""QCheckBoxのstateをbool値に変換して返す

        :param qcheckbox: QCheckBox
        :return: bool
        """
        if qcheckbox.checkState() == Qt.CheckState.Checked:
            return True
        else:
            return False

    def _apply_scene(self, *args):
        u"""「現在のシーンを反転」ボタンのコマンド"""
        typ = self._get_type_from_ui()
        axis = self._get_axis_from_ui()
        right_id = self.ui.line_edit_right_id.text()
        left_id = self.ui.line_edit_left_id.text()

        mode = self._get_mode_from_ui()
        can_bake = self._is_checked_qcheckbox(self.ui.checkbox_can_bake)
        can_save = self._is_checked_qcheckbox(self.ui.checkbox_can_save)
        dirpath = self.ui.line_edit_dirname.text()

        if mode == 'pose':
            # ctrl_sets = cmds.ls(sl=True, typ='objectSet')
            # if not ctrl_sets:
            #     logger.warning(u"コントローラーセットを選択してください")
            #     return
            # self._apply_pose(ctrl_sets, typ, axis, right_id, left_id)
            selections = cmds.ls(sl=True)
            self._apply_pose(selections, typ, axis, right_id, left_id)
        else:
            # ctrl_sets = cmds.ls(sl=True, typ='objectSet')
            # if not ctrl_sets:
            #     logger.warning(u"コントローラーセットを選択してください")
            #     return
            # self._apply_motion(ctrl_sets, typ, axis, right_id, left_id, can_bake, can_save, dirpath)
            selections = cmds.ls(sl=True)
            self._apply_motion(selections, typ, axis, right_id, left_id, can_bake, can_save, dirpath)

    def _get_workfiler_widget(self, name):
        u"""objectNameからwidgetを取得

        :param name: 名前(文字列)
        :return: QWidget
        """
        widgets = QApplication.allWidgets()
        for widget in widgets:
            if widget.objectName() == name:
                return widget

    def _get_maya_file_paths_from_workfier(self):
        u"""workfilerからMayaファイルを取得

        :return: Mayaファイルのパスのリスト
        """
        dir_view = self._get_workfiler_widget('MtkExplorerDirView')
        if not dir_view:
            dir_view = self._get_workfiler_widget('mtkWorkFilerDirView')

        file_view = self._get_workfiler_widget('MtkExplorerFileView')
        if not file_view:
            file_view = self._get_workfiler_widget('mtkWorkFilerFileView')

        dir_model = dir_view.model()
        file_proxy_model = file_view.model()
        file_model = file_proxy_model.sourceModel()

        file_paths = []
        dirpath = dir_model.filePath(dir_view.currentIndex())
        indices = file_view.selectionModel().selectedRows(0)

        for index in indices:
            name = file_model.itemFromIndex(file_proxy_model.mapToSource(index)).text()
            file_paths.append(u'{}/{}'.format(dirpath, name))

        return file_paths

    def _apply_workfiler(self, *args):
        u"""「WorkFilerで選択したファイルを反転」ボタンのコマンド"""
        typ = self._get_type_from_ui()
        axis = self._get_axis_from_ui()
        right_id = self.ui.line_edit_right_id.text()
        left_id = self.ui.line_edit_left_id.text()

        mode = self._get_mode_from_ui()
        can_bake = self._is_checked_qcheckbox(self.ui.checkbox_can_bake)
        dirpath = self.ui.line_edit_dirname.text()

        if mode == 'pose':
            logger.warning(u'Pose反転はWorkFilerからの出力に対応していません')
            return
            # ctrl_sets = cmds.ls(sl=True, typ='objectSet')
            # if not ctrl_sets:
            #     logger.warning(u"コントローラーセットを選択してください")
            #     return
            # self._apply_pose(ctrl_sets, typ, axis, right_id, left_id)
        else:
            can_save = True
            maya_scenes = self._get_maya_file_paths_from_workfier()
            if not maya_scenes:
                logger.warning(u"WorkFilerでシーンファイルを選択してください")
                return
            self._apply_background(
                maya_scenes, typ, axis, right_id, left_id, can_bake, can_save, dirpath,
            )

    def _apply_pose(self, ctrl_sets, typ, axis, right_id, left_id):
        u"""ポーズ反転の実行

        :param ctrl_sets: コントローラーのセットのリスト
        :param axis: 軸
        :param right_id: 右側のノードの識別子
        :param left_id: 左側のノードの識別子
        """
        logger.debug('Apply: Pose')
        # for ctrl_set in ctrl_sets:
        #     ReverseMotionCmd.main(ctrl_set, typ, axis, right_id, left_id, False, 0)
        ReverseMotionCmd.main(ctrl_sets, typ, axis, right_id, left_id, False, 0)

        cmds.select(ctrl_sets, ne=True)

    def _apply_motion(self, ctrl_sets, typ, axis, right_id, left_id, can_bake, can_save, dirpath):
        u"""モーション反転をGUI上で実行

        :param ctrl_sets: コントローラーのセットのリスト
        :param axis: 軸
        :param right_id: 右側のノードの識別子
        :param left_id: 左側のノードの識別子
        :param can_bake: アニメーションをベイクするか
        :param can_save: 保存するかどうか
        :param dirpath: 出力先のディレクトリ
        """
        logger.debug('Apply: Motion')
        # for ctrl_set in ctrl_sets:
        #     ReverseMotionCmd.main(ctrl_set, typ, axis, right_id, left_id, can_bake, 1)
        ReverseMotionCmd.main(ctrl_sets, typ, axis, right_id, left_id, can_bake, 1)

        if can_save:
            maya_scene = getCurrentSceneFilePath()
            if ReverseMotionCmd.is_ignore_file(maya_scene):
                cmds.warning(u'除外対象のファイルだったため処理をスキップしました')
                cmds.select(ctrl_sets, ne=True)
                return

            save_scene_path = ReverseMotionCmd.get_reverse_file_path(maya_scene)
            if save_scene_path:
                ReverseMotionCmd.save_scene(save_scene_path, dirpath)
            else:
                cmds.warning(u'右側モーションだったため保存をスキップしました')

        cmds.select(ctrl_sets, ne=True)

    def _apply_background(self, maya_scenes, typ, axis, right_id, left_id, can_bake, can_save, dirpath):
        u"""mayabatchで実行

        :param maya_scenes: mayaシーンのパスのリスト
        :param axis: 軸
        :param right_id: 右側のノードの識別子
        :param left_id: 左側のノードの識別子
        :param can_bake: アニメーションをベイクするか
        :param can_save: 保存するかどうか
        :param dirpath: 出力先のディレクトリ
        """
        bat_file = self._write_bat(
            maya_scenes, typ, axis, right_id, left_id, can_bake, can_save, dirpath,
        )
        logger.debug('system("start {0}")'.format(bat_file))
        mel.eval('system("start {0}")'.format(bat_file))

    def _connect(self):
        u"""UIとコマンドの接続"""
        self.ui.radio_button_local.toggled.connect(self.save_settings)
        self.ui.radio_button_local.toggled.connect(self._change_type_event)

        self.ui.radio_button_x.toggled.connect(self.save_settings)
        self.ui.line_edit_right_id.textChanged.connect(self.save_settings)
        self.ui.line_edit_left_id.textChanged.connect(self.save_settings)

        self.ui.radio_button_pose.toggled.connect(self.save_settings)
        self.ui.radio_button_pose.toggled.connect(self._change_mode_event)
        self.ui.checkbox_can_save.stateChanged.connect(self.save_settings)
        self.ui.line_edit_dirname.textChanged.connect(self.save_settings)

        self.ui.dirname_browse_btn.clicked.connect(self._dirname_browse_btn_command)

    def _script_browse_btn_command(self, *args):
        u"""script_browse_btnを押したときに実行されるコマンド"""
        file_filter = "Script File (*.mel *.py);; Python (*.py);; MEL (*.mel)"
        files = cmds.fileDialog2(ff=file_filter, ds=2, fm=1)
        if files:
            self.ui.script_line.setText(files[0])

    def _dirname_browse_btn_command(self, *args):
        u"""dirname_browse_btnを押したときに実行されるコマンド"""
        dirs = cmds.fileDialog2(ds=2, fm=3, okc='Set')
        if dirs:
            self.ui.line_edit_dirname.setText(dirs[0])

    def _write_bat(self, maya_scenes, typ, axis, right_id, left_id, can_bake, can_save, dirpath):
        u"""mayabatch実行用のbatファイルの生成

        :param maya_scenes: mayaシーンのパスのリスト
        :param typ: 'local' リグの軸基準, 'world' worldOffsetのみ反転, 'both' リグ基準反転後、worldoffset反転
        :param axis: 軸
        :param right_id: 右側のノードの識別子
        :param left_id: 左側のノードの識別子
        :param can_bake: ベイクするか
        :param can_save: 保存するか
        :param dirpath: 出力先のディレクトリ
        :return: batファイル名
        """
        bat_file = '{temp}/reversemotion_{timestamp}.bat'.format(
            temp=mayabatch.get_temp_dir(),
            timestamp=mayabatch.get_timestamp(),
        )
        # modulename = re.sub('gui', 'command', __name__)
        with codecs.open(bat_file, 'w', 'cp932') as f:
            for i, maya_scene in enumerate(maya_scenes):
                func_args = "'{}', '{}', '{}', '{}', '{}', {}, {}, '{}'".format(
                    maya_scene, typ, axis, right_id, left_id, can_bake, can_save, dirpath,
                )
                logger.debug(func_args)

                py_command = u'from mtku.maya.menus.animation.reversemotion import ReverseMotionCmd;'
                py_command += u'ReverseMotionCmd.exec_standalone({})'.format(func_args)
                logger.debug(py_command)

                mel_command = 'python("""{command}""")'.format(command=py_command)

                f.write(mayabatch.get_command_description(mel_command, i))
            f.write('pause\r\n')
            f.write(mayabatch.delete_self_description())

        return bat_file
