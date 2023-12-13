# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import os

import maya.cmds as cmds

from shr.base.window import BaseWindow

from .. import config
from .. import lib_animation
from .. import lib_maya

logger = logging.getLogger(__name__)


def get_icon_path(icon_name):
    """アイコンパスを取得
    :param str icon_name:
    :return: アイコンパス
    :rtype: str
    """
    icon_path = os.path.join(os.path.dirname(__file__), 'icons', icon_name).replace(os.sep, '/')
    return icon_path if os.path.isfile(icon_path) else ''


class AnimCopyPaste(BaseWindow):

    UI_FILE = os.path.join(os.path.dirname(__file__), 'animcopypaste.ui').replace(os.sep, '/')

    def __init__(self, *args, **kwargs):
        super(AnimCopyPaste, self).__init__(*args, **kwargs)

        self._tool_name = 'animcopypaste'
        self.title = 'Anim Copy Paste'

        self.width = 520
        self.height = 450
        self._option_ui = None
        self._current_data = None

        self._help_url = 'https://wisdom.cygames.jp/display/mutsunokami/Anim+Copy+Paste'

    def _add_baselayout(self):
        u"""基本レイアウトの追加"""
        # メニューバー
        self._add_editmenu()
        self._add_helpmenu()

        mainform = cmds.formLayout(nd=100)
        maintab = cmds.tabLayout(tv=False, scr=True, cr=True, h=1)
        self.main_layout = cmds.columnLayout(adj=1)
        # レイアウト作成 ====
        self.create()
        # ====
        cmds.setParent('..')

        cmds.setParent(mainform)
        cmds.formLayout(
            mainform, e=True,
            af=(
                [maintab, 'top', 0],
                [maintab, 'left', 2],
                [maintab, 'right', 2],
                [maintab, 'bottom', 0]

            ),
        )
        cmds.setParent(self.main_layout)

    def _connect(self):
        u"""コマンドの接続"""
        self._option_ui.copy_copyanimation.clicked.connect(self.copy_animation)
        self._option_ui.paste_animation.clicked.connect(self.paste_animation)

        self._option_ui.copy_timerange_group.buttonClicked.connect(self._copy_timerange_changed)
        self._option_ui.paste_timerange_group.buttonClicked.connect(self._paste_timerange_changed)
        self._option_ui.paste_method_group.buttonClicked.connect(self._paste_method_changed)

    def _copy_timerange_changed(self, *args):
        copy_timerange = self._option_ui.copy_timerange_group.checkedButton().objectName().split('_')[-1]
        self._option_ui.copy_startframe.setEnabled(copy_timerange == 'startend')
        self._option_ui.copy_endframe.setEnabled(copy_timerange == 'startend')

    def _paste_timerange_changed(self, *args):
        paste_timerange = self._option_ui.paste_timerange_group.checkedButton().objectName().split('_')[-1]
        self._option_ui.paste_startframe.setEnabled(paste_timerange in ['startend', 'start'])
        self._option_ui.paste_endframe.setEnabled(paste_timerange == 'startend')

    def _paste_method_changed(self, *args):
        paste_method = self._option_ui.paste_method_group.checkedButton().objectName().split('_')[-1]
        self._option_ui.pasterange_widgetA.setEnabled(paste_method != 'replacecompletely')
        self._option_ui.pasterange_widgetB.setEnabled(paste_method != 'replacecompletely')

    def _set_time_range_tooltip(self, *args):
        self._option_ui.copyrange_timeslider.setToolTip('''\
        <html><head/><body><p>Scene playback range.</p><p><img src="{}"/></p></body></html>
        '''.format(get_icon_path('timerange_timeslider.png')))

        self._option_ui.copyrange_timecontrol.setToolTip('''\
        <html><head/><body><p>Timeslider highlight selection range.</p><p><img src="{}"/></p></body></html>
        '''.format(get_icon_path('timerange_timecontrol.png')))

    def _set_paste_methos_tooltip(self, *args):

        self._option_ui.pastemethod_replacecompletely.setToolTip('''\
        <html><head/><body><p>Replace entire curve range.<br>help > pasteKey command.</p><p><img src="{}"/></p></body></html>
        '''.format(get_icon_path('pastemethod_replaceCompletely.png')))

        self._option_ui.pastemethod_replace.setToolTip('''\
        <html><head/><body><p>Replace specify curve range.<br>help > pasteKey command.</p><p><img src="{}"/></p></body></html>
        '''.format(get_icon_path('pastemethod_replace.png')))

        self._option_ui.pastemethod_insert.setToolTip('''\
        <html><head/><body><p>Insert specify curve range.<br>help > pasteKey command.</p><p><img src="{}"/></p></body></html>
        '''.format(get_icon_path('pastemethod_insert.png')))

    def get_settings(self, *args):
        u"""設定の取得"""
        copy_timerange = self._option_ui.copy_timerange_group.checkedButton().objectName()
        copy_startframe = self._option_ui.copy_startframe.value()
        copy_endframe = self._option_ui.copy_endframe.value()
        copy_include_static = self._option_ui.copy_include_static.isChecked()
        copy_bakemethod = self._option_ui.copy_bakemethod_group.checkedButton().objectName()

        paste_timerange = self._option_ui.paste_timerange_group.checkedButton().objectName()
        paste_startframe = self._option_ui.paste_startframe.value()
        paste_endframe = self._option_ui.paste_endframe.value()
        paste_channels = self._option_ui.paste_channels_group.checkedButton().objectName()
        paste_namespace = self._option_ui.paste_namespace_group.checkedButton().objectName()
        paste_method = self._option_ui.paste_method_group.checkedButton().objectName()

        return {
            'copy_timerange': copy_timerange.split('_')[-1],
            'copy_startframe': copy_startframe,
            'copy_endframe': copy_endframe,
            'copy_bakemethod': copy_bakemethod.split('_')[-1],
            'copy_includestatic': bool(copy_include_static),

            'paste_timerange': paste_timerange.split('_')[-1],
            'paste_startframe': paste_startframe,
            'paste_endframe': paste_endframe,
            'paste_channels': paste_channels.split('_')[-1],
            'paste_namespace': paste_namespace.split('_')[-1],
            'paste_method': paste_method.split('_')[-1],
        }

    def read_settings(self, *args):
        read_values = lib_maya.load_optionvar('%s__ui_options' % self._tool_name)
        if read_values:
            try:
                # copy options
                if 'copy_timerange' in read_values:
                    v = read_values.get('copy_timerange', '')
                    if v == 'all':
                        self._option_ui.copyrange_all.setChecked(True)
                    elif v == 'startend':
                        self._option_ui.copyrange_startend.setChecked(True)
                    elif v == 'timeslider':
                        self._option_ui.copyrange_timeslider.setChecked(True)
                    elif v == 'timecontrol':
                        self._option_ui.copyrange_timecontrol.setChecked(True)

                if 'copy_bakemethod' in read_values:
                    v = read_values.get('copy_bakemethod', '')
                    if v == 'none':
                        self._option_ui.bake_none.setChecked(True)
                    elif v == 'all':
                        self._option_ui.bake_all.setChecked(True)

                if 'copy_includestatic' in read_values:
                    v = read_values.get('copy_includestatic', True)
                    self._option_ui.copy_include_static.setChecked(v)

                # paste options
                if 'paste_method' in read_values:
                    v = read_values.get('paste_method', '')
                    if v == 'replacecompletely':
                        self._option_ui.pastemethod_replacecompletely.setChecked(True)
                    elif v == 'replace':
                        self._option_ui.pastemethod_replace.setChecked(True)
                    elif v == 'insert':
                        self._option_ui.pastemethod_insert.setChecked(True)

                if 'paste_timerange' in read_values:
                    v = read_values.get('paste_timerange', '')
                    if v == 'current':
                        self._option_ui.pasterange_current.setChecked(True)
                    elif v == 'start':
                        self._option_ui.pasterange_start.setChecked(True)
                    elif v == 'startend':
                        self._option_ui.pasterange_startend.setChecked(True)

                if 'paste_namespace' in read_values:
                    v = read_values.get('paste_namespace', '')
                    if v == 'original':
                        self._option_ui.targetnamespace_original.setChecked(True)
                    elif v == 'select':
                        self._option_ui.targetnamespace_select.setChecked(True)

                if 'paste_channels' in read_values:
                    v = read_values.get('paste_channels', '')
                    if v == 'all':
                        self._option_ui.pastechannels_all.setChecked(True)
                    elif v == 'select':
                        self._option_ui.pastechannels_select.setChecked(True)
                    elif v == 'transform':
                        self._option_ui.pastechannels_transform.setChecked(True)

            except Exception as e:
                cmds.error(e)
                self.reset_settings()

    def save_settings(self, *args):
        u"""設定の保存
        """
        settings = self.get_settings()
        lib_maya.save_optionvar('%s__ui_options' % self._tool_name, settings)

    def reset_settings(self, *args):
        u"""設定のリセット"""

        self._option_ui.copyrange_timeslider.setChecked(True)
        self._option_ui.bake_all.setChecked(True)
        self._option_ui.copy_include_static.setChecked(True)

        self._option_ui.pastemethod_replace.setChecked(True)
        self._option_ui.pasterange_start.setChecked(True)
        self._option_ui.targetnamespace_original.setChecked(True)
        self._option_ui.pastechannels_all.setChecked(True)

        # リセット後に設定を保存
        self.save_settings()

    def create(self):
        layout = cmds.columnLayout(adj=True, p=self.main_layout)

        # Option
        option_layout = cmds.columnLayout(adj=True, p=layout)
        self._option_ui = self.load_file(self.UI_FILE, parent=option_layout)

        self.read_settings()

        start, end = lib_maya.get_timeslider_timerange()
        self._option_ui.copy_startframe.setValue(start)
        self._option_ui.copy_endframe.setValue(end)
        self._option_ui.paste_startframe.setValue(start)
        self._option_ui.paste_endframe.setValue(end)

        self._set_paste_methos_tooltip()
        self._set_time_range_tooltip()
        self._copy_timerange_changed()
        self._paste_timerange_changed()
        self._paste_method_changed()

        self._connect()

    def help(self, *args):
        """ヘルプの表示
        """
        cmds.showHelp(self._help_url, a=True)

    def get_temp_animation_file(self):
        anim_data_dir = os.path.join(config.get_clipboard_dir(), config.TEMP_ANIMDATA_NAME).replace(os.sep, '/')
        anim_data_file = os.path.join(
            anim_data_dir, '{}{}'.format(config.TEMP_ANIMDATA_NAME, config.ANIM_DATA_EXT)).replace(os.sep, '/')

        return anim_data_file

    def copy_animation(self):
        """
        """

        settings = self.get_settings()

        anim_data_file = self.get_temp_animation_file()
        anim_data_dir = os.path.dirname(anim_data_file)
        if not os.path.isdir(anim_data_dir):
            os.makedirs(anim_data_dir)

        write_success = False
        cmds.waitCursor(state=True)
        cmds.undoInfo(ock=True, cn='write_animation_data')
        try:
            write_success = lib_animation.write_animation(
                anim_data_file,
                hirarchy=settings.get('copy_target', 'select'),
                channels=settings.get('copy_channels', 'all'),
                contain_static_channels=settings.get('copy_includestatic', True),
                timerange=settings.get('copy_timerange', 'timeslider'),
                startframe=settings.get('copy_startframe', 0),
                endframe=settings.get('copy_endframe', 0),
                method=settings.get('copy_method', 'curve'),
                bakemethod=settings.get('copy_bakemethod', 'none'),
            )

        finally:
            cmds.undoInfo(cck=True, cn='write_animation_data')
            cmds.waitCursor(state=False)

            if write_success and cmds.undoInfo(q=True, undoName=True) == 'write_animation_data':
                cmds.undo()

        self.save_settings()

    def paste_animation(self):
        """
        """

        settings = self.get_settings()

        anim_data_file = self.get_temp_animation_file()
        if not os.path.isfile(anim_data_file):
            cmds.warning('Paste data is not found.')
            return

        cmds.waitCursor(state=True)
        cmds.undoInfo(ock=True)
        try:
            paste_anim_options = {
                'target': settings.get('paste_target', 'all'),
                'channels': settings.get('paste_channels', 'all'),
                'timerange': settings.get('paste_timerange', 'timeslider'),
                'startframe': settings.get('paste_startframe', 0),
                'endframe': settings.get('paste_endframe', 0),
                'method': settings.get('paste_method', 'replacecompletely'),
                'namespace': settings.get('paste_namespace', 'original'),
                'breakdown': settings.get('paste_breakdown', False),
                'connect': settings.get('paste_connect', False),
            }

            logging.debug('read_animation(\'{}\', {})'.format(
                anim_data_file, ', '.join('{!s}={!r}'.format(k, v) for k, v in paste_anim_options.items())))

            pasted_plugs = lib_animation.read_animation(
                anim_data_file, **paste_anim_options
            )

            if pasted_plugs:
                pasted_nodes = list(set([plug.split('.', 1)[0] for plug in pasted_plugs]))
                cmds.select(pasted_nodes, r=True)

        finally:
            cmds.undoInfo(cck=True)
            cmds.waitCursor(state=False)

        self.save_settings()
