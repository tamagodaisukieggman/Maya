# -*- coding: utf-8 -*-

from __future__ import absolute_import

import functools
import os

import maya.cmds as cmds

from . import command


class RetargetSceneSetupUI(object):

    def __init__(self, *args, **kwargs):
        super(RetargetSceneSetupUI, self).__init__(*args, **kwargs)

        self._tool_name = 'retarget_scene_setup'
        self.title = 'Facial Retarget Scene Setup'
        self._help_url = 'https://wisdom.cygames.jp/pages/viewpage.action?pageId=28523860'

        self.width = 550
        self.height = 100
        self.margin = 2

        self.performance_file = None
        self.character_setting_file = None
        self.camera = None

    def show(self):
        self.close()

        win = cmds.window(self._tool_name, title=self.title, mb=True, w=self.width, h=self.height)

        # Menu
        editMenu = cmds.menu(l='Edit', p=win)
        cmds.menuItem(l='Save Settings', p=editMenu, c=functools.partial(self.save_settings))
        cmds.menuItem(l='Reset Settings', p=editMenu, c=functools.partial(self.reset_and_save_settings))

        # Help
        help_menu = cmds.menu(label='Help', p=win)
        cmds.menuItem(label='Help on Retargeter Scene Setup', p=help_menu, c=self.help)

        mainLay = cmds.formLayout(p=win, nd=100)
        mainColumn = cmds.columnLayout(adj=True, p=mainLay, rs=2)

        # plugin
        row = cmds.rowLayout(nc=2, cw2=(100, 100), cl2=['center', 'left'], adj=2,
                             ct2=['right', 'left'], p=mainColumn)
        cmds.text(label='Plugin : ', p=row)
        form = cmds.formLayout(nd=100, p=row)
        load_btn = cmds.button(label='Load', w=50, h=20, p=form, c=self.on_load_plugin)
        unload_btn = cmds.button(label='Unload', w=50, h=20, p=form, c=self.on_unload_plugin)
        cmds.formLayout(form, e=True,
                        af=[[load_btn, 'left', self.margin],
                            [load_btn, 'top', self.margin],
                            [load_btn, 'bottom', self.margin],
                            [unload_btn, 'right', self.margin],
                            [unload_btn, 'top', self.margin],
                            [unload_btn, 'bottom', self.margin],
                            ],
                        ap=[[load_btn, 'right', self.margin, 50],
                            [unload_btn, 'left', self.margin, 50],
                            ])

        cmds.separator(style='in', h=6, p=mainColumn)

        # window
        row = cmds.rowLayout(nc=2, cw2=(100, 100), cl2=['center', 'left'], adj=2,
                             ct2=['right', 'left'], p=mainColumn)
        cmds.text(label='Window : ', p=row)
        form = cmds.formLayout(nd=100, p=row)
        retarger_btn = cmds.button(label='Retargeter', w=50, h=20, p=form, c=self.on_show_retargeter)
        charactersetup_btn = cmds.button(label='Character Settings', w=50, h=20, p=form, c=self.on_show_charactersetup)
        cmds.formLayout(form, e=True,
                        af=[[retarger_btn, 'left', self.margin],
                            [retarger_btn, 'top', self.margin],
                            [retarger_btn, 'bottom', self.margin],
                            [charactersetup_btn, 'right', self.margin],
                            [charactersetup_btn, 'top', self.margin],
                            [charactersetup_btn, 'bottom', self.margin],
                            ],
                        ap=[[retarger_btn, 'right', self.margin, 50],
                            [charactersetup_btn, 'left', self.margin, 50],
                            ])

        cmds.separator(style='in', h=6, p=mainColumn)

        # character settings
        cmds.text(label='Performance', p=mainColumn)

        row = cmds.rowLayout(nc=3, cw3=(130, 100, 50), cl3=['center', 'left', 'left'], adj=2,
                             ct3=['right', 'left', 'left'], p=mainColumn)
        cmds.text(label='Character Setting (.xml) : ', p=row)
        self.character_setting_file = cmds.textField(p=row, w=100)
        cmds.textField(self.character_setting_file, e=True,
                       ec=functools.partial(self.on_pathfield_enter, self.character_setting_file))
        cmds.button(label='Set...', c=self.on_set_charactersettings)

        # performance file
        row = cmds.rowLayout(nc=3, cw3=(130, 100, 50), cl3=['center', 'left', 'left'], adj=2,
                             ct3=['right', 'left', 'left'], p=mainColumn)
        cmds.text(label='Performance (.fwr) : ', p=row)
        self.performance_file = cmds.textField(p=row, w=100)
        cmds.textField(self.performance_file, e=True,
                       ec=functools.partial(self.on_pathfield_enter, self.performance_file))
        cmds.button(label='Set...', c=self.on_set_performance)

        cmds.button(label='Open Performance',
                    ann=u'パフォーマンスファイルを開きます。',
                    c=self.on_open_performance, p=mainColumn)

        cmds.separator(style='in', h=6, p=mainColumn)

        cmds.text(label='Work space setting', p=mainColumn)

        # camera
        row = cmds.rowLayout(nc=3, cw3=(100, 100, 30), cl3=['center', 'left', 'left'], adj=2,
                             ct3=['right', 'left', 'left'], p=mainColumn)
        cmds.text(label='Camera : ', p=row)
        self.camera = cmds.textField(p=row, w=100)
        btn = cmds.iconTextButton(image='popupMenuIcon.png', p=row, w=30, h=20, bgc=[0.35, 0.35, 0.35])
        self.camera_menu = cmds.popupMenu(
            b=1, pmc=functools.partial(self.populate_camera_menu), p=btn)

        row = cmds.rowLayout(nc=2, cw2=(100, 100), cl2=['center', 'left'], adj=2,
                             ct2=['right', 'left'], p=mainColumn)
        cmds.text(label='', p=row)
        cmds.button(label='Fit Video Image Plane',
                    ann=u'イメージプレーンの簡易位置合わせを行います。',
                    p=row, c=self.on_fit_video_plane)

        # facial panel
        row = cmds.rowLayout(nc=2, cw2=(100, 100), cl2=['center', 'left'], adj=2,
                             ct2=['right', 'left'], p=mainColumn)
        cmds.text(label='Facial Panel : ', p=row)
        form = cmds.formLayout(nd=100, p=row)
        facial_view_btn = cmds.button(label='Change Main View Layout', p=form,
                                      ann=u'カレントビューポートをフェイシャル用のレイアウトに変更します。',
                                      c=self.on_setup_vertical3_pane)
        facial_win_btn = cmds.button(label='Show Facial Window', p=form,
                                     ann=u'フェイシャル用のウィンドウを立ち上げます。',
                                     c=self.on_show_facial_window)

        facial_diagonal_btn = cmds.button(label='Tear off Faical Panel', p=form,
                                          ann=u'フェイシャル用のウィンドウを立ち上げます。\n'
                                              u'回転コントロールの中心座標を取得するオブジェクトを選択して下さい。',
                                          c=self.on_show_facial_single_panel)

        cmds.formLayout(form, e=True,
                        af=[[facial_view_btn, 'left', 0],
                            [facial_view_btn, 'top', 0],
                            [facial_view_btn, 'bottom', 0],
                            [facial_win_btn, 'top', 0],
                            [facial_win_btn, 'bottom', 0],
                            [facial_diagonal_btn, 'right', 0],
                            [facial_diagonal_btn, 'top', 0],
                            [facial_diagonal_btn, 'bottom', 0],
                            ],
                        ap=[[facial_view_btn, 'right', self.margin, 33],
                            [facial_win_btn, 'left', self.margin, 33],
                            [facial_win_btn, 'right', self.margin, 67],
                            [facial_diagonal_btn, 'left', self.margin, 67],
                            ])

        cmds.formLayout(mainLay, e=True,
                        af=[[mainColumn, 'top', self.margin],
                            [mainColumn, 'left', self.margin],
                            [mainColumn, 'right', self.margin],
                            [mainColumn, 'bottom', self.margin],
                            ],
                        )

        cmds.showWindow(win)
        cmds.window(win, e=True, w=self.width, h=self.height)

        self.reset_settings()
        self.read_settings()

    def close(self):
        if cmds.window(self._tool_name, q=True, ex=True):
            cmds.deleteUI(self._tool_name)

    def get_settings(self, *args):
        u"""設定の取得"""

        return {
            'performance_file': cmds.textField(self.performance_file, q=True, tx=True).strip(' '),
            'character_setting_file': cmds.textField(self.character_setting_file, q=True, tx=True).strip(' '),
            'camera': cmds.textField(self.camera, q=True, tx=True),
        }

    def read_settings(self, *args):
        """optionVarから設定をロード
        """

        read_values = command.load_optionvar('%s__ui_options' % self._tool_name)
        if read_values:
            try:
                if 'performance_file' in read_values:
                    cmds.textField(self.performance_file, e=True, tx=read_values['performance_file'])

                if 'character_setting_file' in read_values:
                    cmds.textField(self.character_setting_file, e=True, tx=read_values['character_setting_file'])

                if 'camera' in read_values:
                    cmds.textField(self.camera, e=True, tx=read_values['camera'])

            except Exception as e:
                cmds.error(e)
                self.reset_settings()

    def save_settings(self, *args):
        u"""設定の保存
        """
        settings = self.get_settings()
        command.save_optionvar('%s__ui_options' % self._tool_name, settings)

    def reset_settings(self, *args):
        u"""設定のリセット"""

        cmds.textField(self.performance_file, e=True, tx='')
        cmds.textField(self.character_setting_file, e=True, tx='')
        cmds.textField(self.camera, e=True, tx='')

    def reset_and_save_settings(self, *args):
        """設定のリセット＆保存
        """

        self.reset_settings()
        self.save_settings()

    def help(self, *args):
        """ヘルプの表示
        """
        cmds.showHelp(self._help_url, a=True)

    def check_retargeter_plugin(self):
        if not cmds.pluginInfo(command.PLUGIN_NAME, q=True, loaded=True):
            ret = cmds.confirmDialog(title='Load Plugin Confirm', p=self._tool_name,
                                     message=u'Retargeterプラグインをロードしますか？',
                                     button=['OK', 'Cancel'])
            if ret == 'OK':
                command.load_retargeter()

        return cmds.pluginInfo(command.PLUGIN_NAME, q=True, loaded=True)

    def on_load_plugin(self, *args):
        if cmds.pluginInfo(command.PLUGIN_NAME, q=True, loaded=True):
            cmds.warning(u'Retargeterプラグインはロード済みです。')

        command.load_retargeter()

    def on_unload_plugin(self, *args):
        if cmds.pluginInfo(command.PLUGIN_NAME, q=True, loaded=True):
            ret = cmds.confirmDialog(title='Unload Confirm', p=self._tool_name,
                                     message=u'同一セッションでRetargeterプラグインの再読み込みが出来なくなります。\n'
                                             u'Retargeterプラグインのアンロードを行いますか？',
                                     button=['OK', 'Cancel'])

            if ret == 'OK':
                command.unload_retargeter()

    def on_show_retargeter(self, *args):
        if not self.check_retargeter_plugin():
            return

        command.retargeter()

    def on_show_charactersetup(self, *args):
        if not self.check_retargeter_plugin():
            return

        command.show_charactersetupwindow()

    def on_pathfield_enter(self, ctl, *args):
        cmds.textField(ctl, e=True, tx=cmds.textField(ctl, q=True, tx=True).replace(os.sep, '/').rstrip('/'))

    def on_set_charactersettings(self, *args):
        current = cmds.textField(self.character_setting_file, q=True, tx=True).replace(os.sep, '/')
        if os.path.isfile(current):
            current_dir = os.path.dirname(current)
        else:
            current_dir = current

        items = cmds.fileDialog2(caption='Character Setting File (.xml)', ds=1, fm=1, okc='Set',
                                 ff=u'キャラクター設定ファイル (*.xml)', dir=current_dir)
        if items:
            cmds.textField(self.character_setting_file, e=True, tx=items[0].replace(os.sep, '/'))

        self.save_settings()

    def on_set_performance(self, *args):
        current = cmds.textField(self.performance_file, q=True, tx=True).replace(os.sep, '/')
        if os.path.isfile(current):
            current_dir = os.path.dirname(current)
        else:
            current_dir = current

        items = cmds.fileDialog2(caption='Performance File (.fwr)', ds=1, fm=1, okc='Set',
                                 ff=u'Facewareリターゲッティングファイル (*.fwr)', dir=current_dir)
        if items:
            cmds.textField(self.performance_file, e=True, tx=items[0].replace(os.sep, '/'))

        self.save_settings()

    def on_open_performance(self, *args):
        if not self.check_retargeter_plugin():
            return

        settings = self.get_settings()

        fwr = settings.get('performance_file', '')
        xml = settings.get('character_setting_file', '')

        with command.WaitCursorBlock():
            command.ftiOpenPerformance(fwr, xml)

        self.save_settings()

    def list_cameras(self):
        return cmds.listRelatives(cmds.ls(cameras=True), p=True, pa=True)

    def populate_camera_menu(self, *args):
        cmds.popupMenu(self.camera_menu, e=True, dai=True)

        for camera in self.list_cameras():
            cmds.menuItem(p=self.camera_menu, label=camera,
                          c=functools.partial(self.update_camera, camera))

    def update_camera(self, camera, *args):
        cmds.textField(self.camera, e=True, tx=camera)
        self.save_settings()

    def on_fit_video_plane(self, *args):
        camera = cmds.textField(self.camera, q=True, tx=True)
        if not cmds.objExists(camera):
            cmds.warning(u'シーン内のカメラを指定して下さい。')
            return
        nodes = cmds.ls(cmds.listRelatives(cmds.ls(sl=True), s=True) or [], type=['mesh', 'imagePlane'])
        if not nodes:
            cmds.warning(u'リターゲターで作成されたVideoPlaneを選択して下さい。')
            return

        plane = cmds.listRelatives(nodes, p=True)[0]
        command.fit_videoplane(plane, camera)

    def on_set_facial_work_panel(self, *args):
        camera = cmds.textField(self.camera, q=True, tx=True)
        if not cmds.objExists(camera):
            cmds.warning(u'シーン内のカメラを指定して下さい。')
            return

        panel = cmds.getPanel(wf=True)

        camera_shape = cmds.listRelatives(camera, s=True, type='camera')[0]
        cmds.modelEditor(panel, e=True, camera=camera_shape)
        cmds.modelEditor(panel, e=True, cmEnabled=True, allObjects=False, imagePlane=True)

    def on_show_facial_window(self, *args):
        camera = cmds.textField(self.camera, q=True, tx=True)
        if not cmds.objExists(camera):
            cmds.warning(u'シーン内のカメラを指定して下さい。')
            return

        command.facial_window(camera)

    def on_setup_vertical3_pane(self, *args):
        camera = cmds.textField(self.camera, q=True, tx=True)
        if not cmds.objExists(camera):
            cmds.warning(u'シーン内のカメラを指定して下さい。')
            return

        ret = cmds.confirmDialog(title='Change Main View Settings Confirm', p=self._tool_name,
                                 message=u'カレントビューポートの設定を変更します。',
                                 button=['OK', 'Cancel'])
        if ret == 'OK':
            command.setup_vertical3_panel(camera)

    def on_show_facial_single_panel(self, *args):
        camera = cmds.textField(self.camera, q=True, tx=True)
        if not cmds.objExists(camera):
            cmds.warning(u'シーン内のカメラを指定して下さい。')
            return

        sels = cmds.ls(sl=True, o=True)
        if not sels:
            cmds.warning(u'回転ピボット指定用のオブジェクトを選択して下さい。')
            return

        if sels:
            pivot = cmds.xform(sels[0], q=True, ws=True, t=True)
        else:
            pivot = [0.0, 0.0, 0.0]

        command.facial_single_panel(camera, pivot)
