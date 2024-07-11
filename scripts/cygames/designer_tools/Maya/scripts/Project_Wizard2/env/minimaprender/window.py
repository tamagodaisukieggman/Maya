# -*- coding: utf-8 -*-
from distutils.util import strtobool
from logging import getLogger
import os
import re
import traceback
from importlib import reload
from PySide2 import QtGui
import maya.cmds as cmds
import webbrowser
from . import command
reload(command)
from .command import MiniMapRender

logger = getLogger(__name__)


class MiniMapRenderWindow(object):
    u"""ベースウインドウクラス"""

    def __init__(self, *args, **kwargs):
        self.window = self.__class__.__name__
        self.close()

        self.title = kwargs.setdefault('title', self.window)
        self.width = 600
        self.height = 240

        self.edit_menu = None
        self.help_menu = None
        self.main_layout = None
        self.column_layout = None

        # self.url = 'https://wisdom.tkgpublic.jp/x/fcT6B'
        self.url = 'https://wisdom.tkgpublic.jp/pages/viewpage.action?pageId=857199267'

        self._output_directory_field = ''
        self._output_file_field = ''
        self._resolution_field = None
        self._resolution_width_field = 4096
        self._resolution_height_field = 4096
        self._image_formats = ['tif', 'jpg', 'tga', 'psd', 'png']
        self._lighting_modes = ['Default', 'All', 'None', 'Active', 'Full Ambient']
        self._image_format_selection = None
        self._lighting_mode_selection = None
        self._fill_percent = None
        self._fill_percent = 100
        self._fill_check_box = None

        self._key_output_file = '{}.output_file'.format(__package__)
        self._key_resolution_width = '{}.resolution_width'.format(__package__)
        self._key_resolution_height = '{}.resolution_height'.format(__package__)
        self._key_fill_percent = '{}.fill_percent'.format(__package__)
        self._key_image_format = '{}.image_format'.format(__package__)
        self._key_lighting_mode = '{}.lighting_mode'.format(__package__)
        self._key_fill_check_box = '{}.fill'.format(__package__)

    def _browse_directory(self, *args):
        starting_directory = cmds.textField(self._output_directory_field, q=True, tx=True)
        directory = cmds.fileDialog2(ds=2, fm=2, okc='Set', dir=starting_directory)
        if directory:
            cmds.textField(self._output_directory_field, e=True, tx=directory[0])

    def _get_output_dir_from_scene(self):
        u"""Mayaシーンから出力フォルダを取得

        :return: 出力フォルダのパス
        """
        maya_scene_path = cmds.file(q=True, sn=True)

        if not maya_scene_path:
            return ''

        maya_scene_directory = os.path.dirname(maya_scene_path)
        maya_root = os.path.dirname(maya_scene_directory)

        maya_images = '{}/images'.format(maya_root)
        if not os.path.exists(maya_images):
            os.mkdir(maya_images)

        return maya_images

    def _get_output_file_name(self):
        u"""出力ファイル名

        :param directory:
        :param file_name:
        :return:
        """
        minimap_file_name = os.path.basename(cmds.file(q=True, sn=True))
        if minimap_file_name:
            minimap_file_name = minimap_file_name.split('.')[0]
        return minimap_file_name

    def create(self):
        u"""Windowのレイアウト作成"""
        cmds.frameLayout(l='Settings', cl=False, cll=True)

        # Output Directory
        cmds.columnLayout()
        cmds.rowLayout(adj=2, nc=3)
        cmds.text(l='Output Directory', width=150)
        self._output_directory_field = cmds.textField(width=364, tx=self._get_output_dir_from_scene())
        cmds.button(l=u'...', width=50, height=26, c=self._browse_directory)
        cmds.setParent('..')

        # Output File
        cmds.columnLayout()
        cmds.rowLayout(adj=2, nc=2)
        cmds.text(l='Output File Name', width=150)
        self._output_file_field = cmds.textField(width=165, tx=self._get_output_file_name(), cc=self._verify_text_field)
        cmds.setParent('..')

        # Resolution
        cmds.rowLayout(adj=2, nc=2)
        cmds.text(l='Resolution', width=150)
        self._resolution_field = cmds.intFieldGrp(
            nf=2,
            w=200,
            v1=self._resolution_width_field,
            v2=self._resolution_height_field,
        )
        cmds.setParent('..')

        # Fill %
        cmds.columnLayout()
        cmds.rowLayout(adj=3, nc=3)
        self._fill_check_box = cmds.checkBox(
            l='Fill % (1~100)',
            w=150,
            v=False,
            cc=self._change_fill
        )
        self._fill_percent = cmds.intFieldGrp(
            nf=1,
            w=360,
            v1=self._fill_percent,
            ann=u'FitFactor',
            enable=False
        )
        cmds.setParent('..')
        # Image Format
        cmds.rowLayout(adj=3, nc=2)
        cmds.text(l='Image Format', width=150)
        self._image_format_selection = cmds.optionMenu(l='', w=160)
        for image_format in self._image_formats:
            cmds.menuItem(l=image_format)
        cmds.optionMenu(self._image_format_selection, e=True, v=self._image_formats[4])
        cmds.setParent('..')

        # Lighting Mode
        cmds.rowLayout(adj=3, nc=2)
        cmds.text(l='Lighting Mode', width=150)
        self._lighting_mode_selection = cmds.optionMenu(l='', w=160)
        for lighting_mode in self._lighting_modes:
            cmds.menuItem(l=lighting_mode)
        cmds.optionMenu(self._lighting_mode_selection, e=True, v=self._lighting_modes[4])
        cmds.setParent('..')

        self.read_settings()
        self.event_scene_opened()

    def _initialize_window(self):
        u"""Windowの初期化"""
        if not cmds.window(self.window, ex=True):
            self.window = cmds.window(self.window, mb=True)

    def save_settings(self, *args):
        u"""設定の保存"""

        settings = {
            self._key_resolution_width: cmds.intFieldGrp(self._resolution_field, q=True, v1=True),
            self._key_resolution_height: cmds.intFieldGrp(self._resolution_field, q=True, v2=True),
            self._key_fill_percent: cmds.intFieldGrp(self._fill_percent, q=True, v1=True),
            self._key_image_format: cmds.optionMenu(self._image_format_selection, q=True, v=True),
            self._key_lighting_mode: cmds.optionMenu(self._lighting_mode_selection, q=True, v=True),
            self._key_fill_check_box: cmds.checkBox(self._fill_check_box, q=True, v=True),
        }

        # mayaPrefsに保存
        [cmds.optionVar(sv=(k, v)) for k, v in settings.items()]

        return settings

    def reset_settings(self, *args):
        u"""設定のリセット"""
        cmds.textField(self._output_directory_field, e=True, tx=self._get_output_dir_from_scene())
        cmds.textField(self._output_file_field, e=True, tx=self._get_output_file_name())
        cmds.intFieldGrp(self._resolution_field, e=True, v1=self._resolution_width_field, v2=self._resolution_height_field)
        cmds.intFieldGrp(self._fill_percent, e=True, v1=self._fill_percent)
        cmds.optionMenu(self._image_format_selection, e=True, v=self._image_formats[4])
        cmds.optionMenu(self._lighting_mode_selection, e=True, v=self._lighting_modes[4])
        cmds.checkBox(self._fill_check_box, e=True, v=True),

    def read_settings(self):
        u"""設定の読み込み"""

        # 解像度
        resolution_width = int(cmds.optionVar(q=self._key_resolution_width))
        resolution_height = int(cmds.optionVar(q=self._key_resolution_width))

        if resolution_width:
            cmds.intFieldGrp(self._resolution_field, e=True, v1=resolution_width)
        if resolution_height:
            cmds.intFieldGrp(self._resolution_field, e=True, v2=resolution_height)

        # Fill%
        fill_percent = int(cmds.optionVar(q=self._key_fill_percent))
        if fill_percent:
            cmds.intFieldGrp(self._fill_percent, e=True, v1=fill_percent)

        # 画像形式
        image_format = cmds.optionVar(q=self._key_image_format)
        if image_format:
            cmds.optionMenu(self._image_format_selection, e=True, v=image_format)

        # ライトモード
        lighting_mode = cmds.optionVar(q=self._key_lighting_mode)
        if lighting_mode:
            cmds.optionMenu(self._lighting_mode_selection, e=True, v=lighting_mode)

        # Fill%チェックボックス
        can_fill = strtobool(str(cmds.optionVar(q=self._key_fill_check_box)))
        if can_fill:
            cmds.checkBox(self._fill_check_box, e=True, v=can_fill)
            self._change_fill()

    def _verify_text_field(self, *args):
        u""" Output File Name フィールドの名前確認"""
        output_file_field = cmds.textField(self._output_file_field, q=True, tx=True)
        if len(output_file_field) == 0:
            cmds.textField(self._output_file_field, e=True, bgc=(0.49, 0.0, 0.0))
            logger.warning(u'出力ファイル名を入力してください')
        else:
            cmds.textField(self._output_file_field, e=True, bgc=(0.169, 0.169, 0.169))

    def _change_fill(self, *args):
        u"""チェックボタン変更時の挙動

        :param args:
        :return:
        """
        fill = cmds.checkBox(self._fill_check_box, q=True, v=True)
        if fill:
            cmds.intFieldGrp(self._fill_percent, e=True, en=True)
        else:
            cmds.intFieldGrp(self._fill_percent, e=True, en=False)

    def show(self, *args):
        u"""Windowの表示"""
        self._initialize_window()
        self._add_baselayout()
        cmds.showWindow(self.window)
        cmds.window(self.window, e=True, t=self.title, wh=(self.width, self.height), cc=self.save_settings)

    def close(self, *args):
        u"""Windowのclose"""
        if cmds.window(self.window, ex=True):
            cmds.deleteUI(self.window)

    def _add_editmenu(self):
        u"""menu「Edit」を追加"""
        self.edit_menu = cmds.menu(l='Edit')
        cmds.menuItem(l='Save Settings', c=self.save_settings)
        cmds.menuItem(l='Reset Settings', c=self.reset_settings)

    def _add_help_menu(self):
        u"""menu「Help」を追加"""
        self.help_menu = cmds.menu(l='Help', hm=True)
        cmds.menuItem(l='Help on {0}'.format(self.title), c=self.help)

    def _add_other_menus(self):
        u"""メニューを追加"""
        # Others
        others_menu = cmds.menu(l='Others', p=self.window, to=True)
        cmds.menuItem(l=u'batフォルダを開く', p=others_menu, enable=False, c=self._open_bat_dir)

    def _open_bat_dir(self, *args):
        u"""batフォルダを開く"""
        root_directory = os.path.dirname(__file__)
        for i in range(6):
            root_directory = os.path.dirname(root_directory)
        root_directory = '{}/{}/bat/rendering'.format(root_directory, cmds.about(version=True))
        batch_directtory = re.sub('/', r'\\', root_directory)
        QtGui.QDesktopServices.openUrl('file:///{}'.format(batch_directtory))

    def _add_baselayout(self):
        u"""基本レイアウトの追加"""
        # メニューバー
        self._add_editmenu()
        self._add_other_menus()
        self._add_help_menu()

        mainform = cmds.formLayout(nd=100)
        maintab = cmds.tabLayout(tv=False, scr=True, cr=True, h=1)
        self.main_layout = cmds.columnLayout(adj=1)
        # レイアウト作成 ====
        self.column_layout = cmds.columnLayout(adj=1, cat=('left', 10), rs=5)
        self.create()
        cmds.setParent('..')
        # ====
        cmds.setParent('..')

        cmds.setParent(mainform)
        execform = self._add_execform()
        cmds.formLayout(
            mainform, e=True,
            af=(
                [maintab, 'top', 0],
                [maintab, 'left', 2],
                [maintab, 'right', 2],
                [execform, 'left', 2],
                [execform, 'right', 2],
                [execform, 'bottom', 0],
            ),
            ac=(
                [maintab, 'bottom', 5, execform],
            ),
        )
        cmds.setParent(self.main_layout)

    def _add_execform(self):
        u"""Apply Closeボタンの追加

        :return: フォーム名
        """
        execform = cmds.formLayout(nd=100)
        # ボタン
        apply_btn = cmds.button(l='Apply', h=26, c=self.apply_)
        close_btn = cmds.button(l='Close', h=26, c=self.close)
        # レイアウト
        cmds.formLayout(
            execform, e=True,
            af=(
                [apply_btn, 'left', 0],
                [apply_btn, 'bottom', 5],
                [close_btn, 'bottom', 5],
                [close_btn, 'right', 0],
            ),
            ap=(
                [apply_btn, 'right', 1, 50],
                [close_btn, 'left', 0, 50],
            ),
        )

        return execform

    def help(self, *args):
        u"""help表示"""
        try:
            webbrowser.open(self.url)
        except Exception as e:
            logger.error(u'ヘルプの URL が見つかりません: {}'.format(e))

    def _event_set_line_edit_directory(self, *args):
        directory = self._get_output_dir_from_scene()
        if not directory:
            return
        cmds.textField(self._output_directory_field, e=True, tx=directory)
        file_name = self._get_output_file_name()
        if not file_name:
            return
        cmds.textField(self._output_file_field, e=True, tx=file_name)

    def event_scene_opened(self):
        u"""MayaシーンOpen時に実行されるイベント"""
        # 出力先を自動でセット
        cmds.scriptJob(e=['SceneOpened', self._event_set_line_edit_directory], p=self.window)

    def _confirm_dialog(self, title, result, *args):

        messages = u'{}\n'.format(result)

        cmds.confirmDialog(
            t=u'{}'.format(title),
            message=messages,
            button='OK',
            db='OK',
            messageAlign='top',
        )

    def _confirm_dialog_branch(self, messages):
        u"""確認ダイアログ

        :param messages:
        :return:
        """

        confirm = cmds.confirmDialog(
            t=u'確認',
            message=messages,
            button=['Yes', 'No'],
            db='Yes',
            cb='No',
            ds='No',
        )
        return confirm

    def _rename_file(self, file_path, *args):
        u"""レンダリグしたファイル名末尾の _tmp を除外してリネームする"""

        image_dir = os.path.dirname(file_path)
        filename, ext = os.path.splitext(os.path.basename(file_path))
        filename = filename[:filename.find('_tmp')]
        output_saved_file = '{}/{}{}'.format(image_dir, filename, ext)
        cmds.sysFile(file_path, rename=output_saved_file)
        return output_saved_file

    def apply_(self, *args):
        u"""Applyボタンの実行コマンド"""

        output_directory = cmds.textField(self._output_directory_field, q=True, tx=True)
        output_file = cmds.textField(self._output_file_field, q=True, tx=True)
        resolution_width = cmds.intFieldGrp(self._resolution_field, q=True, v1=True)
        resolution_height = cmds.intFieldGrp(self._resolution_field, q=True, v2=True)
        image_format = cmds.optionMenu(self._image_format_selection, q=True, v=True)
        lighting_mode = cmds.optionMenu(self._lighting_mode_selection, q=True, v=True)
        fill = cmds.checkBox(self._fill_check_box, q=True, v=True)
        fill_percent = cmds.intFieldGrp(self._fill_percent, q=True, v1=True)

        # 出力ファイル
        output = '{}/{}'.format(output_directory, output_file)
        output_file = '{}/{}.{}'.format(output_directory, output_file, image_format)

        minimap_mesh = MiniMapRender._get_minimap_mesh()

        if not minimap_mesh:
            messages = u'ミニマップ用コリジョンメッシュが見つかりません(xxx_colグループ配下のground)'
            self._confirm_dialog(u'エラー', messages)
            return

        if os.path.exists(output_file):
            messages = u'以下のファイルを上書きします\n'
            messages += output_file
            confirm = self._confirm_dialog_branch(messages)
            if confirm != 'Yes':
                logger.info(u'中断')
                return

        cmds.undoInfo(ock=True)
        # 処理実行
        saved_file = ''
        try:
            result = MiniMapRender.minimap_render_exec_(
                output,
                resolution_width,
                resolution_height,
                image_format,
                lighting_mode,
                fill_percent,
                minimap_mesh,
                fill,
            )

            # ファイル名リネーム
            if not result:
                logger.error('レンダリング失敗')
                return
            saved_file = self._rename_file(result['saved_file'])
            self.save_settings()
            if saved_file:
                messages = u'ファイルを保存しました\n'
                messages += saved_file
                self._confirm_dialog(u'確認', messages)
        except Exception as e:
            logger.error('{}'.format(e))
            logger.error(traceback.format_exc())
        finally:
            cmds.undoInfo(cck=True)
            # cmds.undo()  # minimapグループを残すため
