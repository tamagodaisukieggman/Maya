# -*- coding: utf-8 -*-
import maya.cmds as cmds
from time import time
import webbrowser
from .command import CheckUVPaddingCmd
from logging import getLogger

logger = getLogger(__name__)

class CheckUVPaddingGUI(object):

    def __init__(self, *args, **kwargs):
        self.window = self.__class__.__name__
        self.close()

        self.title = kwargs.setdefault('title', self.window)
        self.width = 300
        self.height = 170

        self.edit_menu = None
        self.help_menu = None
        self.main_layout = None
        self.column_layout = None

        self.url = 'https://wisdom.cygames.jp/display/designersmanual/Maya:+CheckUVPadding'

        self._resolution_field = None
        self._shell_padding_field = None
        self._tile_padding_field = None

        self.resolution = 1024
        self.shell_padding = 8.0
        self.tile_padding = 4.0
        
        self._key_resolution = '{}.resolution'.format(__package__)
        self._key_shell_padding = '{}.shell_padding'.format(__package__)
        self._key_tile_padding = '{}.tile_padding'.format(__package__)

    def create(self):
        u"""Windowのレイアウト作成"""
        cmds.frameLayout(l='Settings')

        # 解像度
        self._resolution_field = cmds.intFieldGrp(
            l='Texture Map Size',
            cw2=[100, 100],
            v1=self.resolution,
            cc=self.save_settings,
            ann=u'ピクセルのパディング値を計算するためにUV 空間に表示する解像度を決定します。',
        )

        # UVシェル間隔
        self._shell_padding_field = cmds.floatFieldGrp(
            l='Shell Padding',
            cw2=[100, 100],
            pre=2,
            v1=self.shell_padding,
            cc=self.save_settings,
            ann=u'UV シェル間(アイランド間)の空間量を決定します。',
        )

        # マップ境界間隔
        self._tile_padding_field = cmds.floatFieldGrp(
            l='Tile Padding',
            cw2=[100, 100],
            pre=2,
            v1=self.tile_padding,
            cc=self.save_settings,
            ann=u'UV タイルのエッジ間の空間量を決定します。',
        )

        self.read_settings()

    def _initialize_window(self):
        u"""Windowの初期化"""
        if not cmds.window(self.window, ex=True):
            self.window = cmds.window(self.window, mb=True)

    def save_settings(self, *args):
        u"""設定の保存"""
        settings = {
            self._key_resolution: cmds.intFieldGrp(self._resolution_field, q=True, v1=True),
            self._key_shell_padding: cmds.floatFieldGrp(self._shell_padding_field, q=True, v1=True),
            self._key_tile_padding: cmds.floatFieldGrp(self._tile_padding_field, q=True, v1=True),
        }
        # Maya Preferences 保存
        [cmds.optionVar(sv=(k, v)) for k, v in settings.items()]
        return settings

    def reset_settings(self, *args):
        u"""設定のリセット"""
        cmds.intFieldGrp(self._resolution_field, e=True, v1=self.resolution)
        cmds.floatFieldGrp(self._shell_padding_field, e=True, v1=self.shell_padding)
        cmds.floatFieldGrp(self._tile_padding_field, e=True, v1=self.tile_padding)
        self.save_settings()

    def read_settings(self):
        """設定の読み込み"""
        resolution = int(cmds.optionVar(q=self._key_resolution))
        shell_padding = float(cmds.optionVar(q=self._key_shell_padding))
        tile_padding = float(cmds.optionVar(q=self._key_tile_padding))
        if resolution is not None:
            cmds.intFieldGrp(self._resolution_field, e=True, v1=resolution)
        if shell_padding is not None:
            cmds.floatFieldGrp(self._shell_padding_field, e=True, v1=shell_padding)
        if tile_padding is not None:
            cmds.floatFieldGrp(self._tile_padding_field, e=True, v1=tile_padding)

    def show(self, *args):
        u"""Windowの表示"""
        self._initialize_window()
        self._add_baselayout()

        cmds.showWindow(self.window)
        cmds.window(self.window, e=True, t=self.title, wh=(self.width, self.height))

    def close(self, *args):
        u"""Windowのclose"""
        if cmds.window(self.window, ex=True):
            cmds.deleteUI(self.window)

    def help(self, *args):
        u"""help表示"""
        try:
            webbrowser.open(self.url)
        except Exception as e:
            return
            logger.info(u'ヘルプの URL が見つかりません: {}'.format(e))

    def _add_edit_menu(self):
        u"""menu「Edit」を追加"""
        self.edit_menu = cmds.menu(l='Edit')
        cmds.menuItem(l='Save Settings', c=self.save_settings)
        cmds.menuItem(l='Reset Settings', c=self.reset_settings)

    def _add_help_menu(self):
        u"""menu「Help」を追加"""
        self.help_menu = cmds.menu(l='Help', hm=True)
        cmds.menuItem(l='Help on {0}'.format(self.title), c=self.help)

    def _add_baselayout(self):
        u"""基本レイアウトの追加"""
        # メニューバー
        self._add_edit_menu()
        self._add_help_menu()

        mainform = cmds.formLayout(nd=100)
        maintab = cmds.tabLayout(tv=False, scr=True, cr=True, h=1)
        self.main_layout = cmds.columnLayout(adj=1)

        self.column_layout = cmds.columnLayout(adj=1, cat=('left', 10), rs=5)
        self.create()
        cmds.setParent('..')

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
        execute_form = cmds.formLayout(nd=100)
        # ボタン
        apply_btn = cmds.button(l='Apply', h=26, c=self.apply_)
        close_btn = cmds.button(l='Close', h=26, c=self.close)
        # レイアウト
        cmds.formLayout(
            execute_form, e=True,
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

        return execute_form

    @staticmethod
    def _confirm_dialog(title, result, *args):

        messages = u'{}\n'.format(result)

        cmds.confirmDialog(
            t=u'{}'.format(title),
            message=messages,
            button='OK',
            db='OK',
            messageAlign='top',
        )

    def apply_(self, *args):
        u"""Apply ボタンの実行コマンド"""

        start = time()

        error_nodes = []

        resolution = cmds.intFieldGrp(self._resolution_field, q=True, v=True)
        shell_padding = cmds.floatFieldGrp(self._shell_padding_field, q=True, v1=True)
        tile_padding = cmds.floatFieldGrp(self._tile_padding_field, q=True, v1=True)

        selection = cmds.ls(sl=True)

        if not selection:
            cmds.warning(u'何も選択されていません')
            return

        result = CheckUVPaddingCmd.execute_(selection, resolution[0], shell_padding, tile_padding)

        if not result:
            cmds.select(selection, r=True)
            logger.info(u'処理を中断しました')
            return

        logger.info(u'{:-^79}'.format('RESULT'))

        if result['error_shells']:
            error_shells = list(set(result['error_shells']))
            logger.info(u'{} 個の隣接する UV フェイスがあります'.format(len(error_shells)))
            error_nodes.extend(error_shells)

        if result['error_tiles']:
            error_tiles = list(set(result['error_tiles']))
            logger.info(u'{} 個のマップ境界間隔がオーバーしたフェイスがあります'.format(len(error_tiles)))
            error_nodes.extend(error_tiles)

        if error_nodes:
            cmds.select(error_nodes, r=True)
        else:
            cmds.select(selection, r=True)
            message = u'問題がある隣接 UV フェイス又はマップ境界間隔がオーバーした UV フェイスはありません。'
            self._confirm_dialog(u'確認', message)

        if result['error_meshes']:
            cmds.warning(u'{} の UV シェルが取得出来ませんでした'.format(result['error_meshes']))

        elapsed = time() - start
        logger.info(u'処理時間: {} [sec]'.format(elapsed))

        logger.info(u'{:-<79}'.format(''))
