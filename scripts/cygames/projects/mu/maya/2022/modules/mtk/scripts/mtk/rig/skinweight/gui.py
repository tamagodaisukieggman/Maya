# -*- coding: utf-8 -*-

from __future__ import absolute_import

import functools
import os

import maya.cmds as cmds

import logging
# from mtku.maya.mtklog import MtkLog
from . import command

# logger = MtkLog(__name__)
logger = logging.getLogger("Skin Weight ... : スキンウェイトツール")


class SkinWeightGUI(object):
    """SkinWeight GUI
    """

    # Import method label.
    import_method_labels = [
        'Index',
        'Closest Position',
        'Closest Component',
        'UV Space',
    ]

    # Import method name.
    import_methods = [
        'index',
        'closestPoint',
        'closestComponent',
        'uvspace',
    ]

    # Copy method label
    copy_method_labels = import_method_labels[::]

    # Copy method name
    copy_methods = import_methods[::]

    max_recent_directories = 10

    def __init__(self, *args, **kwargs):
        super(SkinWeightGUI, self).__init__(*args, **kwargs)

        self._tool_name = 'skinweight_tool'
        self.title = 'Skin Weight'

        self.width = 400
        self.height = 180
        self.margin = 2

        self.directory = None
        self.directory_ctl_menu = None

        self.import_scroll_lay = None
        self.export_scroll_lay = None

        self.tab_lay = None

        self.import_method = None
        self.force_rebind = None
        self.export_file_name = None

        self.copy_method = None

        self.prune_value = None
        self.round_value = None

        self.weight_file_list_lay = None
        self.weight_file_list_label = None
        self.weight_file_list = None

        self.recent_directories = []

        self._help_url = 'https://wisdom.cygames.jp/pages/viewpage.action?pageId=30420182'

    def show(self):
        """GUIの表示
        """

        self.close()

        win = cmds.window(self._tool_name, title=self.title, mb=True, w=self.width, h=self.height)

        # Menu
        edit_menu = cmds.menu(label='Edit', p=win)
        cmds.menuItem(label='Save Settings', p=edit_menu, c=self.save_settings)
        cmds.menuItem(label='Reset Settings', p=edit_menu, c=self.reset_and_save_settings)
        cmds.menuItem(d=True)
        cmds.menuItem(label='Remove Settings', p=edit_menu, c=self.remove_settings)

        help_menu = cmds.menu(label='Help', p=win)
        cmds.menuItem(label='Help on Skin Weight', p=help_menu, c=self.show_help)

        # Main Layout
        main_lay = cmds.formLayout(p=win, nd=100)
        main_column_lay = cmds.columnLayout(rs=4, adj=True, p=main_lay)

        # Directory
        directory_lay = cmds.rowLayout(nc=3, cw3=(100, 100, 50), cl3=['center', 'left', 'left'], adj=2,
                                       ct3=['right', 'left', 'left'], p=main_column_lay)

        cmds.text('Weight directory : ', p=directory_lay)
        self.directory = cmds.textField(ed=True, p=directory_lay,
                                        ec=self.on_directory_enter,
                                        cc=self.on_directory_enter)

        directory_set_btn = cmds.button(label='Set', w=50, p=directory_lay)
        self.directory_ctl_menu = cmds.popupMenu(
            b=1, pmc=self.populate_directory_menu, p=directory_set_btn)

        cmds.separator(style='in', p=main_column_lay, h=10)

        self.tab_lay = cmds.tabLayout(p=main_column_lay, cr=True, imw=5, imh=5, cc=self.tab_changed)

        # Import
        import_frame_lay = cmds.frameLayout('import_frame', p=self.tab_lay, lv=False, cll=True)
        import_lay = cmds.columnLayout(rs=2, adj=True, p=import_frame_lay)
        self.import_scroll_lay = cmds.columnLayout(rs=4, adj=True, p=import_lay)
        cmds.button(l='Select influences from Weight file', p=import_lay,
                    ann=u'ウェイトデータを元にインフルエンスを選択します。',
                    c=self.on_select_influences_from_weight_file)

        cmds.button(l='Select geometry from Weight file', p=import_lay,
                    ann=u'ウェイトデータを元にジオメトリを選択します。',
                    c=self.on_select_geometry_from_weight_file)

        import_method_radio_lay = cmds.columnLayout(adj=True, p=import_lay, ann=u'\'UV Space\' は meshの場合のみ有効')
        cmds.text(l='    Import Methods {}'.format('-' * 30),
                  fn='boldLabelFont', al='left', p=import_method_radio_lay, h=20)
        self.import_method = cmds.radioCollection(p=import_method_radio_lay)
        for _method, _method_label in zip(self.import_methods, self.import_method_labels):
            _row = cmds.rowLayout(
                nc=2, cw2=[50, 100], cl2=['right', 'left'], ct2=['both', 'left'], p=import_method_radio_lay)
            cmds.text(l='', w=50, p=_row)
            cmds.radioButton('import_{}'.format(_method), l=_method_label, p=_row, collection=self.import_method)

        cmds.separator(style='in', p=import_lay)

        force_bind_lay = cmds.rowLayout(
            nc=2, cw2=[50, 100], cl2=['right', 'left'], ct2=['both', 'left'], p=import_lay)
        cmds.text(l='', w=50, p=force_bind_lay)
        self.force_rebind = cmds.checkBox(
            l=u'Force re-bind by Weight data influences',
            ann=u'ウェイトデータのインフルエンス情報で強制的に再バインドしウェイトをインポートします。',
            v=True, p=force_bind_lay)

        import_btn_lay = cmds.formLayout(nd=100, p=import_lay)
        import_weight_btn = cmds.button(
            l='Import Weight', h=40, p=import_btn_lay,
            ann=u'選択ジオメトリにウェイトをインポートします。\n'
                u'GUIでウェイトファイルを選択して下さい。\n'
                u'ジオメトリを複数選択していた場合は、\n'
                u'ウェイトのインポートを選択ジオメトリに全てに適用します。',
            bgc=[0.45, 0.45, 0.45],
            c=self.on_import_weight_btn)

        import_weights_btn = cmds.button(
            l='Import Weight (Multi)\nsearch file by gometry name', h=40, p=import_btn_lay,
            ann=u'選択ジオメトリ名にマッチするウェイトファイルを自動で取得してウェイトをインポートします。\n'
                u'ネームスペース、ジオメトリ名の重複がある場合、\n'
                u'[ "|" → "__", ":" → "_" ] に変換してファイルを調査します。',
            bgc=[0.45, 0.45, 0.45],
            c=self.on_import_weights_btn)

        cmds.formLayout(import_btn_lay, e=True,
                        af=[[import_weight_btn, 'left', self.margin],
                            [import_weight_btn, 'top', self.margin],
                            [import_weight_btn, 'bottom', self.margin],
                            [import_weights_btn, 'right', self.margin],
                            [import_weights_btn, 'top', self.margin],
                            [import_weights_btn, 'bottom', self.margin],
                            ],
                        ap=[[import_weight_btn, 'right', 2, 50],
                            [import_weights_btn, 'left', 2, 50],
                            ]
                        )

        # Export
        export_frame_lay = cmds.frameLayout('export_frame', p=self.tab_lay, lv=False, cll=True)
        export_lay = cmds.columnLayout(rs=2, adj=True, p=export_frame_lay)
        self.export_scroll_lay = cmds.columnLayout(rs=4, adj=True, p=export_lay)
        export_file_name_lay = cmds.rowLayout(
            nc=2, cw2=[100, 100], cl2=['right', 'left'], ct2=['both', 'left'], p=export_lay, adj=2)
        cmds.text(l='Export Name : ', w=50, p=export_file_name_lay)
        self.export_file_name = cmds.textField(tx='', p=export_file_name_lay)
        export_btn_lay = cmds.formLayout(nd=100, p=export_lay)
        export_weight_btn = cmds.button(
            l='Export Weight', h=40, p=export_btn_lay,
            ann=u'選択ジオメトリ(１つ)のウェイトをエクスポートします。\n'
                u'Export Name を指定して下さい。',
            bgc=[0.45, 0.45, 0.45],
            c=self.on_export_weight_btn)

        export_weights_btn = cmds.button(
            l='Export Weight (Multi)\nAuto naming', h=40, p=export_btn_lay,
            ann=u'選択ジオメトリのウェイトをエクスポートします。\n'
                u'ファイル名はノード名から自動設定します。\n'
                u'ネームスペース、ジオメトリ名の重複がある場合、\n'
                u'[ "|" → "__", ":" → "_" ] に変換したファイルが自動で設定されます。',
            bgc=[0.45, 0.45, 0.45],
            c=self.on_export_weights_btn)

        cmds.formLayout(export_btn_lay, e=True,
                        af=[[export_weight_btn, 'left', self.margin],
                            [export_weight_btn, 'top', self.margin],
                            [export_weight_btn, 'bottom', self.margin],
                            [export_weights_btn, 'right', self.margin],
                            [export_weights_btn, 'top', self.margin],
                            [export_weights_btn, 'bottom', self.margin],
                            ],
                        ap=[[export_weight_btn, 'right', 2, 50],
                            [export_weights_btn, 'left', 2, 50],
                            ]
                        )

        # Bind & Copy
        bind_copy_frame_lay = cmds.frameLayout('bind_copy_frame', p=self.tab_lay, lv=False, cll=True)
        bind_copy_lay = cmds.columnLayout(rs=2, adj=True, p=bind_copy_frame_lay)
        bind_copy_bind_lay = cmds.columnLayout(adj=True, p=bind_copy_lay)
        cmds.text(l='    Bind {}'.format('-' * 30),
                  fn='boldLabelFont', al='left', p=bind_copy_bind_lay, h=20)

        bind_btn_row = cmds.rowLayout(
            nc=2, cw2=[50, 100], cl2=['right', 'left'], ct2=['both', 'left'], p=bind_copy_bind_lay, adj=2)
        cmds.text(l='', w=50, p=bind_btn_row)

        bind_form_lay = cmds.formLayout(nd=100, p=bind_btn_row)
        bind_skin_btn = cmds.button(l='Bind Skin', p=bind_form_lay, h=30,
                                    ann=u'Smooth Bind\n'
                                        u'ジオメトリとインフルエンスを選択して下さい。',
                                    c=self.on_bindskin_btn)

        unbind_skin_btn = cmds.button(l='Unbind Skin', p=bind_form_lay, h=30, bgc=[0.3, 0.3, 0.3],
                                      ann=u'Unbind',
                                      c=self.on_unbindskin_btn)

        cmds.formLayout(bind_form_lay, e=True,
                        af=[[bind_skin_btn, 'left', 0],
                            [bind_skin_btn, 'top', 0],
                            [bind_skin_btn, 'bottom', 0],
                            [unbind_skin_btn, 'right', 0],
                            [unbind_skin_btn, 'top', 0],
                            [unbind_skin_btn, 'bottom', 0],
                            ],
                        ap=[[bind_skin_btn, 'right', 2, 50],
                            [unbind_skin_btn, 'left', 2, 50],
                            ]
                        )

        add_infl_row = cmds.rowLayout(
            nc=2, cw2=[50, 100], cl2=['right', 'left'], ct2=['both', 'left'], p=bind_copy_bind_lay, adj=2)
        cmds.text(l='', w=50, p=add_infl_row)
        infls_form_lay = cmds.formLayout(nd=100, p=add_infl_row)
        add_infls_btn = cmds.button(l='Add Influences', p=infls_form_lay, h=30,
                                    ann=u'インフルエンスを追加します。',
                                    c=self.on_add_influences_btn)

        remove_infls_btn = cmds.button(l='Remove unused influences', p=infls_form_lay, h=30, bgc=[0.3, 0.3, 0.3],
                                       ann=u'バインドで未使用のインフルエンスをskinClusterから除外します。',
                                       c=self.on_remove_unuses_influences_btn)

        cmds.formLayout(infls_form_lay, e=True,
                        af=[[add_infls_btn, 'left', 0],
                            [add_infls_btn, 'top', 0],
                            [add_infls_btn, 'bottom', 0],
                            [remove_infls_btn, 'right', 0],
                            [remove_infls_btn, 'top', 0],
                            [remove_infls_btn, 'bottom', 0],
                            ],
                        ap=[[add_infls_btn, 'right', 2, 50],
                            [remove_infls_btn, 'left', 2, 50],
                            ]
                        )

        goto_bindpose_row = cmds.rowLayout(
            nc=2, cw2=[50, 100], cl2=['right', 'left'], ct2=['both', 'left'], p=bind_copy_bind_lay, adj=2)
        cmds.text(l='', w=50, p=goto_bindpose_row)
        cmds.button(l='Go to Bind Pose', p=goto_bindpose_row, h=30,
                    ann=u'バインドポーズに戻します。',
                    c=self.on_goto_bindpose_btn)

        select_related_infl_row = cmds.rowLayout(
            nc=2, cw2=[50, 100], cl2=['right', 'left'], ct2=['both', 'left'], p=bind_copy_bind_lay, adj=2)
        cmds.text(l='', w=50, p=select_related_infl_row)
        cmds.button(l='Select Related Influences', p=select_related_infl_row, h=30,
                    ann=u'バインドに使用しているインフルエンスを選択します。',
                    c=self.on_select_related_influences_btn)

        bind_copy_copy_lay = cmds.columnLayout(adj=True, p=bind_copy_lay, ann=u'\'UV Space\' は meshの場合のみ有効')
        cmds.text(l='    Copy {}'.format('-' * 30),
                  fn='boldLabelFont', al='left', p=bind_copy_copy_lay, h=20)
        self.copy_method = cmds.radioCollection(p=bind_copy_copy_lay)
        for _method, _method_label in zip(self.copy_methods, self.copy_method_labels):
            _row = cmds.rowLayout(
                nc=2, cw2=[50, 100], cl2=['right', 'left'], ct2=['both', 'left'], p=bind_copy_copy_lay)
            cmds.text(l='', w=50, p=_row)
            cmds.radioButton('copy_{}'.format(_method), l=_method_label, p=_row, collection=self.copy_method)

        bind_and_copy_btn_row = cmds.rowLayout(
            nc=2, cw2=[50, 100], cl2=['right', 'left'], ct2=['both', 'left'], p=bind_copy_copy_lay, adj=2)
        cmds.text(l='', w=50, p=bind_and_copy_btn_row)
        cmds.button(l='Smooth Bind and Copy Weights', p=bind_and_copy_btn_row, h=30,
                    ann=u'Smooth Bind と Copy Weight を行います。\n'
                        u'コピー元ジオメトリ(バインド済み) と コピー先ジオメトリを選択して下さい。',
                    c=self.on_bind_and_copy_btn)

        copy_btn_row = cmds.rowLayout(
            nc=2, cw2=[50, 100], cl2=['right', 'left'], ct2=['both', 'left'], p=bind_copy_copy_lay, adj=2)
        cmds.text(l='', w=50, p=copy_btn_row)
        cmds.button(l='Copy Weights', p=copy_btn_row, h=30,
                    ann=u'Copy Weight を行います。\n'
                        u'コピー元ジオメトリとコピー先ジオメトリを選択して下さい。',
                    c=self.on_copy_btn)

        # Weights
        weights_frame_lay = cmds.frameLayout('weights_frame', p=self.tab_lay, lv=False, cll=True)
        weights_lay = cmds.columnLayout(rs=2, adj=True, p=weights_frame_lay)
        cmds.text(l='    Weights {}'.format('-' * 30),
                  fn='boldLabelFont', al='left', p=weights_lay, h=20)

        normalize_weights_row = cmds.rowLayout(
            nc=3, cw3=[50, 100, 30], cl3=['right', 'left', 'left'], ct3=['both', 'left', 'left'], p=weights_lay, adj=2)
        cmds.text(l='', w=50, p=normalize_weights_row)
        cmds.button(l='Normalize weights', p=normalize_weights_row, h=30,
                    c=self.on_normalize_weights_btn)
        cmds.text(l='', w=50, p=normalize_weights_row)

        prune_weights_row = cmds.rowLayout(
            nc=3, cw3=[50, 100, 30], cl3=['right', 'left', 'left'], ct3=['both', 'left', 'left'], p=weights_lay, adj=2)
        cmds.text(l='', w=50, p=prune_weights_row)
        cmds.button(l='Prune Small Weights', p=prune_weights_row, h=30,
                    c=self.on_prune_weights_btn)
        self.prune_value = cmds.floatField(v=0.01, pre=3, min=0.001, max=1.0, step=0.01, p=prune_weights_row, w=50)

        round_weights_row = cmds.rowLayout(
            nc=3, cw3=[50, 100, 30], cl3=['right', 'left', 'left'], ct3=['both', 'left', 'left'], p=weights_lay, adj=2)
        cmds.text(l='', w=50, p=round_weights_row)
        cmds.button(l='Round Weights', p=round_weights_row, h=30,
                    c=self.on_round_weights_btn)
        self.round_value = cmds.intField(v=3, min=1, max=5, step=1, p=round_weights_row, w=50)

        # file_list
        self.weight_file_list_lay = cmds.columnLayout(adj=True, p=self.export_scroll_lay)
        num_file_list_lay = cmds.rowLayout(
            nc=2, cw2=(100, 100), cl2=['center', 'left'], ct2=['right', 'left'], adj=2,
            h=20, p=self.weight_file_list_lay)

        cmds.text(l='Num Weight Files : ', p=num_file_list_lay, w=100)
        self.weight_file_list_label = cmds.text(l='0', p=num_file_list_lay)

        self.weight_file_list = cmds.textScrollList(
            ams=False, fn='plainLabelFont', en=True, h=200, p=self.weight_file_list_lay,
            sc=self.on_scroll_item_selection)

        cmds.tabLayout(self.tab_lay, e=True,
                       tabLabel=(
                           (import_frame_lay, 'Import'),
                           (export_frame_lay, 'Export'),
                           (bind_copy_frame_lay, 'Bind && Copy'),
                           (weights_frame_lay, 'Edit Weights'),
                       ))

        cmds.formLayout(main_lay, e=True,
                        af=[[main_column_lay, 'top', self.margin],
                            [main_column_lay, 'left', self.margin],
                            [main_column_lay, 'right', self.margin],
                            [main_column_lay, 'bottom', self.margin],
                            ],
                        )
        cmds.showWindow(win)
        cmds.window(win, e=True, w=self.width, h=self.height)

        self.reset_settings()
        self.read_settings()
        self.refresh()

    def refresh(self, *args):
        """GUI更新
        """

        self.tab_changed()
        self.update_weight_file_scroll()

    def close(self):
        """GUIを閉じる
        """

        if cmds.window(self._tool_name, q=True, ex=True):
            cmds.deleteUI(self._tool_name)

    def get_import_settings(self, *args):
        """import設定を取得
        :return: import設定の辞書
        :rtype: dict
        """

        return {
            'import_method': cmds.radioCollection(self.import_method, q=True, sl=True),
            'force_rebind': cmds.checkBox(self.force_rebind, q=True, v=True)
        }

    def get_bind_copy_settings(self, *args):
        """bind_copyの設定を取得
        :return: bind_copy設定の辞書
        :rtype: dict
        """

        return {
            'copy_method': cmds.radioCollection(self.copy_method, q=True, sl=True),
        }

    def get_weights_settings(self, *args):
        """weightsの設定を取得
        :return: weights設定の辞書
        :rtype: dict
        """

        return {
            'prune_value': cmds.floatField(self.prune_value, q=True, v=True),
            'round_value': cmds.intField(self.round_value, q=True, v=True),
        }

    def get_settings(self, *args):
        """設定の取得
        :return: GUI設定の辞書
        :rtype: dict
        """

        return {
            'current_tab': cmds.tabLayout(self.tab_lay, q=True, st=True),
            'recent_directories': self.recent_directories,
            'import': self.get_import_settings(),
            'export': {},
            'bind_copy': self.get_bind_copy_settings(),
            'weights': self.get_weights_settings(),
        }

    def read_settings(self, *args):
        """optionVarから設定をロード
        """

        read_values = command.load_optionvar('%s__ui_options' % self._tool_name)
        if read_values:
            try:
                if 'current_tab' in read_values:
                    cmds.tabLayout(self.tab_lay, e=True, st=read_values.get('current_tab', 'import_frame'))

                if 'recent_directories' in read_values:
                    self.recent_directories = read_values.get('recent_directories', [])
                    if self.recent_directories:
                        cmds.textField(self.directory, e=True, tx=self.recent_directories[0])

                if 'import' in read_values:
                    values = read_values.get('import', {})
                    cmds.radioCollection(self.import_method, e=True, sl=values.get('import_method', 'index'))
                    cmds.checkBox(self.force_rebind, e=True, v=values.get('force_rebind', True))

                if 'bind_copy' in read_values:
                    values = read_values.get('bind_copy', {})
                    cmds.radioCollection(self.copy_method, e=True, sl=values.get('copy_method', 'closestPoint'))

                if 'weights' in read_values:
                    values = read_values.get('weights', {})
                    cmds.floatField(self.prune_value, e=True, v=values.get('prune_value', 0.01))
                    cmds.intField(self.round_value, e=True, v=values.get('round_value', 3))

            except Exception as e:
                cmds.error(e)
                # self.remove_settings()
                self.reset_settings()

    def save_settings(self, *args):
        """設定の保存
        """
        settings = self.get_settings()
        command.save_optionvar('%s__ui_options' % self._tool_name, settings)

    def reset_settings(self, *args):
        """設定のリセット"""

        # cmds.tabLayout(self.tab_lay, e=True, st='import_frame')
        cmds.radioCollection(self.import_method, e=True, sl='import_index')
        cmds.checkBox(self.force_rebind, e=True, v=True)
        cmds.radioCollection(self.copy_method, e=True, sl='copy_closestPoint')
        cmds.floatField(self.prune_value, e=True, v=0.01)
        cmds.intField(self.round_value, e=True, v=3)

    def remove_settings(self, *args):
        """設定の削除
        """

        command.remove_optionvar('%s__ui_options' % self._tool_name)

    def reset_and_save_settings(self, *args):
        """設定のリセット＆保存
        """

        self.reset_settings()
        self.save_settings()

    def show_help(self, *args):
        """ヘルプの表示
        """
        cmds.showHelp(self._help_url, a=True)

    def on_directory_enter(self, *args):
        """ディレクトリ指定textFieldの入力決定時の処理
        """

        cmds.textScrollList(self.weight_file_list, e=True, ra=True)
        cmds.text(self.weight_file_list_label, e=True, l='0')

        dir_ = cmds.textField(self.directory, q=True, tx=True).replace(os.sep, '/').rstrip('/')
        if os.path.isdir(dir_):
            cmds.textField(self.directory, e=True, tx=dir_)
            self.add_recent_directory(dir_)
            self.update_weight_file_scroll()
        else:
            cmds.textScrollList(self.weight_file_list, e=True, ra=True)

    def populate_directory_menu(self, *args):
        """ディレクトリセットボタンのメニューの表示
        """

        cmds.popupMenu(self.directory_ctl_menu, e=True, dai=True)

        # カレントワークスペース
        cmds.menuItem(p=self.directory_ctl_menu, label='Current Work Space',
                      c=functools.partial(self.update_directory, 'current_work_space'))

        # cmds.menuItem(d=True, p=self.directory_ctl_menu)

        # ダイアログで選択
        cmds.menuItem(p=self.directory_ctl_menu, label='Set...',
                      c=functools.partial(self.update_directory, 'set'))

        # 最近使用したディレクトリ
        cmds.menuItem(dl='Recent directories', d=True, p=self.directory_ctl_menu)
        for recent_dir in self.recent_directories:
            cmds.menuItem(p=self.directory_ctl_menu, label=recent_dir,
                          c=functools.partial(self.update_directory, recent_dir))

        cmds.menuItem(d=True, p=self.directory_ctl_menu)

        cmds.menuItem(p=self.directory_ctl_menu, label='Clear Recent Directories',
                      c=functools.partial(self.update_directory, 'clear'))

    def update_directory(self, method, *args):
        """ディレクトリセットメニューの処理
        """

        dir_ = ''
        if method == 'current_work_space':
            dir_ = command.get_workspace_weights_dir()

        elif method == 'set':
            root_dir = cmds.textField(self.directory, q=True, tx=True).replace(os.sep, '/')
            if not os.path.isdir(root_dir):
                root_dir = command.get_workspace_weights_dir()

            items = cmds.fileDialog2(caption='Weight Direcotry', ds=1, fm=3, okc='Set', dir=root_dir)
            if items:
                dir_ = items[0]

        elif method == 'clear':
            self.recent_directories = []
            return

        else:
            dir_ = method

        cmds.textField(self.directory, e=True, tx=dir_)
        self.on_directory_enter()

    def add_recent_directory(self, dir_):
        """最近使用(directory text fieldに設定)したパスの追加処理
        """

        path_index = command.is_contain_path(dir_, self.recent_directories)
        if path_index > -1:
            self.recent_directories.pop(path_index)

        if len(self.recent_directories) >= self.max_recent_directories:
            self.recent_directories.pop()

        self.recent_directories.insert(0, dir_)

    def update_weight_file_scroll(self, *args):
        """ウェイトファイルスクロールリストの更新処理
        """

        dir_ = cmds.textField(self.directory, q=True, tx=True)
        items = command.find_items(dir_, name='*' + command.WEIGHT_FILE_EXT, depth=1, find_type='file')
        if items:
            cmds.textScrollList(self.weight_file_list, e=True, a=sorted(items.keys()))
            cmds.text(self.weight_file_list_label, e=True, l='{}'.format(len(items)))

    def on_scroll_item_selection(self, *args):
        """ウェイトファイルスクロールリストのアイテム選択時の処理
        """

        current = cmds.tabLayout(self.tab_lay, q=True, st=True)
        items = cmds.textScrollList(self.weight_file_list, q=True, si=True)
        if items:
            if current == 'export_frame':
                cmds.textField(self.export_file_name, e=True, tx=items[0])

    def tab_changed(self, *args):
        """タブ切り替え時の処理
        """

        children = cmds.tabLayout(self.tab_lay, q=True, ca=True)
        current = cmds.tabLayout(self.tab_lay, q=True, st=True)

        for child in children:
            cmds.frameLayout(child, e=True, cl=current != child)

        if current == 'import_frame':
            cmds.layout(self.weight_file_list_lay, e=True, p=self.import_scroll_lay)
        else:
            cmds.layout(self.weight_file_list_lay, e=True, p=self.export_scroll_lay)

        cmds.evalDeferred(
            '''import maya.cmds as cmds;cmds.window(\'{}\', e=True, h={})'''.format(self._tool_name, self.height),
            lp=True
        )

    def get_import_weight_file(self, *args):
        """GUI設定からインポートファイル名を取得
        """

        dir_ = cmds.textField(self.directory, q=True, tx=True)
        if not os.path.isdir(dir_):
            return ''

        select_items = cmds.textScrollList(self.weight_file_list, q=True, si=True)
        if not select_items:
            return ''

        file_path = os.path.join(dir_, select_items[0] + command.WEIGHT_FILE_EXT).replace(os.sep, '/')

        return file_path if os.path.isfile(file_path) else ''

    def get_export_weight_file(self, *args):
        """GUI設定からエクスポートファイル名を取得
        """

        dir_ = cmds.textField(self.directory, q=True, tx=True)
        export_name = cmds.textField(self.export_file_name, q=True, tx=True)
        if not export_name:
            logger.warning(u'ファイル名を設定して下さい。')
            return ''

        file_path = os.path.join(dir_, export_name + command.WEIGHT_FILE_EXT).replace(os.sep, '/')

        return file_path

    def on_import_weight_btn(self, *args):
        """import weight (one file per geometry)
        選択ジオメトリにGUI上で指定したウェイトファイルからウェイトをインポート
        """

        import_settings = self.get_import_settings()

        sels = cmds.ls(sl=True, o=True, et='transform')
        if not sels:
            logger.warning(u'ジオメトリを選択して下さい。')
            return

        file_path = self.get_import_weight_file()
        if not os.path.isfile(file_path):
            logger.warning(u'ウェイトファイルを選択して下さい。')
            return

        with command.WaitCursorBlock():
            for node in sels:
                ret = command.import_skinCluster_weights(
                    node,
                    file_path,
                    method=import_settings.get('import_method', 'index').replace('import_', ''),
                    set_by_api=True,
                    undoable=True,
                    force_bind=import_settings.get('force_rebind', False)
                )
                if ret:
                    logger.info('[ Import Weights ] : {} : {}'.format(node, file_path))

    def on_import_weights_btn(self, *args):
        """import weights (one file one geometry)
        選択ノード名から指定ディレクトリ下のウェイトファイルを検索しウェイトをインポート
        ファイル名はノード名から自動設定 (ノード名の '|' を '__ に、':' を'_' に変換してファイルを調査します。)
        """

        import_settings = self.get_import_settings()

        sels = cmds.ls(sl=True, o=True, et='transform')
        if not sels:
            logger.warning(u'ジオメトリを選択して下さい。')
            return

        dir_ = cmds.textField(self.directory, q=True, tx=True)
        if not os.path.isdir(dir_):
            logger.warning(u'ディレクトリが見つかりません。')
            return

        with command.ProgressWindowBlock(title='Import Weights', maxValue=len(sels)) as prg:
            prg.status = 'Import Weights Start'
            prg.step(1)

            for node in sels:
                file_path = os.path.join(
                    dir_,
                    '{}{}'.format(node, command.WEIGHT_FILE_EXT).replace('|', '__').replace(':', '_')
                ).replace(os.sep, '/')

                prg.status = node
                prg.step(1)

                if not os.path.isfile(file_path):
                    logger.warning('[ Import Weights Skip ] : {} : {} is not found'.format(node, file_path))
                    continue

                ret = command.import_skinCluster_weights(
                    node,
                    file_path,
                    method=import_settings.get('import_method', 'index').replace('import_', ''),
                    set_by_api=True,
                    undoable=True,
                    force_bind=import_settings.get('force_rebind', False)
                )

                if ret:
                    logger.info('[ Import Weights ] : {} : {}'.format(node, file_path))

                if prg.is_cancelled():
                    break

        self.save_settings()

    def on_export_weight_btn(self, *args):
        """Export weight (one file one geometry)
        GUIで指定したファイル名で選択ジオメトリのウェイトをエクスポート
        """

        sels = cmds.ls(sl=True, o=True, et='transform')
        if not sels:
            logger.warning(u'ジオメトリを選択して下さい。')
            return

        node = sels[0]
        skinclusters = command.list_related_skinClusters(node)
        if not skinclusters:
            logger.warning(u'スキニングされてたジオメトリを選択して下さい。')
            return

        file_path = self.get_export_weight_file()
        if not file_path:
            return

        with command.WaitCursorBlock():
            export_file = command.export_skinCluster_weights(node, file_path)
            logger.info('[ Export Weights ] : {} : {}'.format(node, export_file))

        self.on_directory_enter()
        self.save_settings()

    def on_export_weights_btn(self, *args):
        """Export weights (one file one geometry)
        指定ディレクトリに選択ジオメトリのウェイトをエクスポート
        ファイル名はノード名から自動設定 (ノード名の '|' を '__ に、':' を'_' に変換して出力します。)
        """

        sels = cmds.ls(sl=True, o=True, et='transform')
        if not sels:
            logger.warning(u'ジオメトリを選択して下さい。')
            return

        skinned_nodes = [node for node in sels if command.list_related_skinClusters(node)]
        if not skinned_nodes:
            logger.warning(u'スキニングされてたジオメトリを選択して下さい。')
            return

        dir_ = cmds.textField(self.directory, q=True, tx=True)

        with command.ProgressWindowBlock(title='Export Weights', maxValue=len(sels)) as prg:
            prg.status = 'Export Weights Start'
            prg.step(1)

            for node in skinned_nodes:
                file_path = os.path.join(
                    dir_,
                    '{}{}'.format(node, command.WEIGHT_FILE_EXT).replace('|', '__').replace(':', '_')
                ).replace(os.sep, '/')

                prg.status = node
                prg.step(1)

                export_file = command.export_skinCluster_weights(node, file_path)

                logger.info('[ Export Weights ] : {} : {}'.format(node, export_file))

                if prg.is_cancelled():
                    break

        self.on_directory_enter()
        self.save_settings()

    def on_select_influences_from_weight_file(self, *args):
        """Select influences from weight file.
        """

        file_path = self.get_import_weight_file()
        if not os.path.isfile(file_path):
            logger.warning(u'ウェイトファイルが見つかりません。')
            return

        command.select_influences_from_data(file_path)

    def on_select_geometry_from_weight_file(self, *args):
        """Select geometry from weight file.
        """

        file_path = self.get_import_weight_file()
        if not os.path.isfile(file_path):
            logger.warning(u'ウェイトファイルが見つかりません。')
            return

        command.select_geometry_from_data(file_path)

    def on_bindskin_btn(self, *args):
        """Bind skin
        """
        nodes = cmds.ls(sl=True, et='transform')
        valid_nodes = [node for node in nodes if not command.list_related_skinClusters(node)]
        if not valid_nodes:
            logger.warning(u'バインドできるジオメトリを選択して下さい。')
            return

        influences = cmds.ls(sl=True, et='joint')
        if not influences:
            logger.warning(u'インフルエンスを選択して下さい。')
            return

        clsts = []
        for node in valid_nodes:
            clst = cmds.skinCluster(
                influences,
                node,
                toSelectedBones=True,
                bindMethod=0,
                normalizeWeights=True,
                weightDistribution=0,
                maximumInfluences=6,
                obeyMaxInfluences=False,
                dropoffRate=4,
                removeUnusedInfluence=False,
                name='{}_skinCluster'.format(node.replace('|', '__'))
            )[0]
            clsts.append(clst)

        return clsts

    def on_unbindskin_btn(self, *args):
        """Unbind skin
        """

        nodes = cmds.ls(sl=True, et='transform')
        valid_nodes = [node for node in nodes if command.list_related_skinClusters(node)]
        if not valid_nodes:
            logger.warning(u'skinClusterが接続されているジオメトリを選択して下さい。')
            return

        for node in valid_nodes:
            cmds.skinCluster(node, e=True, unbind=True)
            logger.info('[ Unbind Skin ] : {}'.format(node))

    def on_add_influences_btn(self, *args):
        """Add Influences
        """

        nodes = cmds.ls(sl=True, et='transform')
        if not nodes:
            logger.warning(u'インフルエンスを追加するジオメトリを選択して下さい。')
            return

        influences = cmds.ls(sl=True, et='joint')
        if not influences:
            logger.warning(u'インフルエンスを選択して下さい。')
            return

        command.add_influences(nodes, influences)

    def on_remove_unuses_influences_btn(self, *args):
        """Remove Influences
        """

        nodes = cmds.ls(sl=True, et='transform')
        valid_nodes = [node for node in nodes if command.list_related_skinClusters(node)]
        if not valid_nodes:
            logger.warning(u'skinClusterが接続されているジオメトリを選択して下さい。')
            return

        skinclusters = command.list_related_skinClusters(valid_nodes)
        for skincluster in skinclusters:
            command.remove_unused_influences(skincluster)

    def on_goto_bindpose_btn(self, *args):
        """Go to Bind Pose
        """

        cmds.dagPose(g=True, restore=True, bindPose=True)

    def on_select_related_influences_btn(self, *args):
        """Select related influences.
        """

        nodes = cmds.ls(sl=True)
        command.select_related_influences(nodes)

    def on_bind_and_copy_btn(self, *args):
        """Smooth bind and copy weights
        """

        sels = cmds.ls(sl=True, et='transform') or []
        if len(sels) < 2:
            logger.warning(u'ジオメトリを２つ選択して下さい。')
            return

        bind_copy_settings = self.get_bind_copy_settings()

        src_shapes = cmds.ls(cmds.listRelatives(sels[0], ad=True, pa=True), ni=True, type='controlPoint')
        if not src_shapes:
            return
        src_geos = cmds.listRelatives(src_shapes, p=True, pa=True)

        dst_shapes = cmds.ls(cmds.listRelatives(sels[1], ad=True, pa=True), ni=True, type='controlPoint')
        if not dst_shapes:
            return
        dst_geos = cmds.listRelatives(dst_shapes, p=True, pa=True)

        if len(src_geos) != len(dst_geos):
            return

        for src_geo, dst_geo in zip(src_geos, dst_geos):
            logger.info('[ Copy Weights ] : {} to {}'.format(src_geo, dst_geo))
            command.bind_and_copy(
                src_geo, dst_geo,
                bind=True,
                method=bind_copy_settings.get('copy_method', 'index').replace('copy_', '')
            )

        self.save_settings()

    def on_copy_btn(self, *args):
        """copy weights
        """

        sels = cmds.ls(sl=True, et='transform') or []
        if len(sels) < 2:
            logger.warning(u'ジオメトリを２つ選択して下さい。')
            return

        bind_copy_settings = self.get_bind_copy_settings()

        src_shapes = cmds.ls(cmds.listRelatives(sels[0], ad=True, pa=True), ni=True, type='controlPoint')
        if not src_shapes:
            return
        src_geos = cmds.listRelatives(src_shapes, p=True, pa=True)

        dst_shapes = cmds.ls(cmds.listRelatives(sels[1], ad=True, pa=True), ni=True, type='controlPoint')
        if not dst_shapes:
            return
        dst_geos = cmds.listRelatives(dst_shapes, p=True, pa=True)

        if len(src_geos) != len(dst_geos):
            return

        for src_geo, dst_geo in zip(src_geos, dst_geos):
            logger.info('[ Copy Weights ] : {} to {}'.format(src_geo, dst_geo))
            command.bind_and_copy(
                src_geo, dst_geo,
                bind=False,
                method=bind_copy_settings.get('copy_method', 'index').replace('copy_', '')
            )

        self.save_settings()

    def on_normalize_weights_btn(self, *args):
        """normalize weights
        """

        sels = cmds.ls(sl=True, fl=True) or []
        if not sels:
            return

        with command.WaitCursorBlock():
            objects = command.get_objects(sels)

            for obj in objects:
                comps = command.get_object_filtered_components(obj, sels)
                if not comps:
                    comps = cmds.ls('{}.cp[*]'.format(obj))

                skinclusters = command.list_related_skinClusters(obj)
                if not skinclusters:
                    continue

                command.normalize_weights(skinclusters[0], comps)

        self.save_settings()

    def on_prune_weights_btn(self, *args):
        """prune weights
        """

        sels = cmds.ls(sl=True, fl=True) or []
        if not sels:
            return

        objects = command.get_objects(sels)

        weights_settings = self.get_weights_settings()
        prune_weights = weights_settings.get('prune_value', 0.01)

        with command.WaitCursorBlock():
            for object_name in objects:
                comps = command.get_object_filtered_components(object_name, sels)
                if not comps:
                    comps = cmds.ls('{}.cp[*]'.format(object_name))

                skinclusters = command.list_related_skinClusters(object_name)
                if not skinclusters:
                    continue

                command.prune_weights(skinclusters[0], comps, prune_weights=prune_weights)

        self.save_settings()

    def on_round_weights_btn(self, *args):
        """round weights
        """

        sels = cmds.ls(sl=True, fl=True) or []
        if not sels:
            return

        objects = command.get_objects(sels)
        weights_settings = self.get_weights_settings()
        round_digits = weights_settings.get('round_value', 0.01)

        with command.WaitCursorBlock():
            for object_name in objects:
                comps = command.get_object_filtered_components(object_name, sels)
                if not comps:
                    comps = cmds.ls('{}.cp[*]'.format(object_name))

                skinclusters = command.list_related_skinClusters(object_name)
                if not skinclusters:
                    continue

                command.round_weights(skinclusters[0], comps, round_digits=round_digits)

        self.save_settings()
