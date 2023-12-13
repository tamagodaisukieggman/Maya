# -*- coding: utf-8 -*-
u"""moveCtrlベイクツール

..
    END__CYGAMES_DESCRIPTION
"""

import functools

import maya.cmds as cmds

import logging
# from mtku.maya.mtklog import MtkLog
from mtk.animation.animstore import lib_maya
from mtk.utils.decoration import keep_selections

from . import command


# logger = MtkLog(__name__)
logger = logging.getLogger(__name__)


class BakeMoveCtrl(object):

    def __init__(self, *args, **kwargs):
        super(BakeMoveCtrl, self).__init__(*args, **kwargs)

        self._tool_name = 'bakemovectrl'
        self.title = 'Bake Move Ctrl'

        self.width = 320
        self.height = 100
        self.margin = 2

        self._restore_translateX = None
        self._restore_translateZ = None
        self._restore_rotateY = None

        self._bake_translateX = None
        self._bake_translateZ = None
        self._bake_rotateY = None

    def show(self):
        self.close()

        win = cmds.window(self._tool_name, title=self.title, mb=True, w=self.width, h=self.height)

        # Menu
        editMenu = cmds.menu(l='Edit', p=win)
        cmds.menuItem(l='Save Settings', p=editMenu, c=functools.partial(self.save_settings))
        cmds.menuItem(l='Reset Settings', p=editMenu, c=functools.partial(self.reset_and_save_settings))

        mainLay = cmds.formLayout(p=win, nd=100)
        mainColumn = cmds.columnLayout(adj=True, p=mainLay, rs=2)

        #
        cmds.text(l='Please select controller.', p=mainColumn, h=24, fn='boldLabelFont', bgc=[0.4, 0.4, 0.4],
                  ann=u'選択ノードからネームスペースを取得します。\nリグアセットのコントローラーを選択してください。')

        # Restore Constraint
        restore_frame = cmds.frameLayout(l='Restore Constraint', lv=True, mw=2, mh=2, cll=False, p=mainColumn)
        restore_column = cmds.columnLayout(adj=True, p=restore_frame)

        restore_attrs_lay = cmds.rowLayout(nc=4, cw4=(40, 100, 100, 90), cl4=['center', 'left', 'left', 'left'],
                                           ct4=['right', 'left', 'left', 'left'], p=restore_column)
        cmds.text(l='', p=restore_attrs_lay)
        self._restore_translateX = cmds.checkBoxGrp(l='TranslateX : ', v1=True, p=restore_attrs_lay, h=24, cw2=[80, 20])
        self._restore_translateZ = cmds.checkBoxGrp(l='TranslateZ : ', v1=True, p=restore_attrs_lay, h=24, cw2=[80, 20])
        self._restore_rotateY = cmds.checkBoxGrp(l='RotateY : ', v1=True, p=restore_attrs_lay, h=24, cw2=[70, 20])
        cmds.button(l='Execute Restore Constraint', h=40,
                    p=restore_column, c=functools.partial(self.restore_move_ctrl_constraint))

        # Bake Move Ctrl
        bake_frame = cmds.frameLayout(l='Bake Move Ctrl', lv=True, mw=2, mh=2, cll=False, p=mainColumn)
        bake_column = cmds.columnLayout(adj=True, p=bake_frame)
        bake_attrs_lay = cmds.rowLayout(nc=4, cw4=(40, 100, 100, 90), cl4=['center', 'left', 'left', 'left'],
                                        ct4=['right', 'left', 'left', 'left'], p=bake_column)
        cmds.text(l='', p=bake_attrs_lay)
        self._bake_translateX = cmds.checkBoxGrp(l='TranslateX : ', v1=True, p=bake_attrs_lay, h=24, cw2=[80, 20])
        self._bake_translateZ = cmds.checkBoxGrp(l='TranslateZ : ', v1=True, p=bake_attrs_lay, h=24, cw2=[80, 20])
        self._bake_rotateY = cmds.checkBoxGrp(l='RotateY : ', v1=True, p=bake_attrs_lay, h=24, cw2=[70, 20])

        cmds.button(l='Apply Bake', h=40,
                    p=bake_column, c=functools.partial(self.bake_move_ctrl))

        cmds.formLayout(mainLay, e=True,
                        af=[[mainColumn, 'top', self.margin],
                            [mainColumn, 'left', self.margin],
                            [mainColumn, 'right', self.margin],
                            [mainColumn, 'bottom', self.margin],
                            ],
                        )

        # Restore Constraint を非表示
        cmds.frameLayout(restore_frame, e=True, vis=False)

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
            'bakeTranslateX': cmds.checkBoxGrp(self._bake_translateX, q=True, v1=True),
            'bakeTranslateZ': cmds.checkBoxGrp(self._bake_translateZ, q=True, v1=True),
            'bakeRotateY': cmds.checkBoxGrp(self._bake_rotateY, q=True, v1=True),
            'restoreTranslateX': cmds.checkBoxGrp(self._restore_translateX, q=True, v1=True),
            'restoreTranslateZ': cmds.checkBoxGrp(self._restore_translateZ, q=True, v1=True),
            'restoreRotateY': cmds.checkBoxGrp(self._restore_rotateY, q=True, v1=True),
        }

    def read_settings(self, *args):
        """optionVarから設定をロード
        """

        read_values = lib_maya.load_optionvar('%s__ui_options' % self._tool_name)
        if read_values:
            try:
                if 'restoreTranslateX' in read_values:
                    v = read_values.get('restoreTranslateX', True)
                    cmds.checkBoxGrp(self._restore_translateX, e=True, v1=v)

                if 'restoreTranslateZ' in read_values:
                    v = read_values.get('restoreTranslateZ', True)
                    cmds.checkBoxGrp(self._restore_translateZ, e=True, v1=v)

                if 'restoreRotateY' in read_values:
                    v = read_values.get('restoreRotateY', True)
                    cmds.checkBoxGrp(self._restore_rotateY, e=True, v1=v)

                if 'bakeTranslateX' in read_values:
                    v = read_values.get('bakeTranslateX', True)
                    cmds.checkBoxGrp(self._bake_translateX, e=True, v1=v)

                if 'bakeTranslateZ' in read_values:
                    v = read_values.get('bakeTranslateZ', True)
                    cmds.checkBoxGrp(self._bake_translateZ, e=True, v1=v)

                if 'bakeRotateY' in read_values:
                    v = read_values.get('bakeRotateY', True)
                    cmds.checkBoxGrp(self._bake_rotateY, e=True, v1=v)

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

        cmds.checkBoxGrp(self._restore_translateX, e=True, v1=True)
        cmds.checkBoxGrp(self._restore_translateZ, e=True, v1=True)
        cmds.checkBoxGrp(self._restore_rotateY, e=True, v1=True)
        cmds.checkBoxGrp(self._bake_translateX, e=True, v1=True)
        cmds.checkBoxGrp(self._bake_translateZ, e=True, v1=True)
        cmds.checkBoxGrp(self._bake_rotateY, e=True, v1=True)

    def reset_and_save_settings(self, *args):
        """設定のリセット＆保存
        """

        self.reset_settings()
        self.save_settings()

    @keep_selections
    def restore_move_ctrl_constraint(self, *args):
        """moveCtrlのコンストレインを復元（リグの初期状態のコネクションを再現）
        """

        settings = self.get_settings()

        namespace = self.get_namespace()

        namespaces = lib_maya.list_namespaces()
        if ':' + namespace not in namespaces:
            cmds.warning(u'リグアセットのコントローラーを選択してください。')
            return

        restoreTranslateX = settings.get('restoreTranslateX', True)
        restoreTranslateZ = settings.get('restoreTranslateZ', True)
        restoreRotateY = settings.get('restoreRotateY', True)

        if not (restoreTranslateX or restoreTranslateZ or restoreRotateY):
            cmds.warning('Invalid restore constraint options.\nPlease turn on restore target checkbox.')
            return

        options = {
            'restoreTranslateX': restoreTranslateX,
            'restoreTranslateZ': restoreTranslateZ,
            'restoreRotateY': restoreRotateY,
        }

        logger.info('Restore moveCtrl constraint : namespace = {}, options = {}'.format(namespace, str(options)))

        command.restore_move_ctrl_constraint(
            namespace=namespace, **options
        )

        self.save_settings()

    @keep_selections
    def bake_move_ctrl(self, *args):
        """moveCtrlのベイク
        | translateは hipBindJtの直下に配置、rotateはリグの初期状態(コンストレイン)の値を取得
        """

        settings = self.get_settings()

        namespace = self.get_namespace()

        namespaces = lib_maya.list_namespaces()
        if ':' + namespace not in namespaces:
            cmds.warning(u'リグアセットのコントローラーを選択してください。')
            return

        bakeTranslateX = settings.get('bakeTranslateX', True)
        bakeTranslateZ = settings.get('bakeTranslateZ', True)
        bakeRotateY = settings.get('bakeRotateY', True)

        if not (bakeTranslateX or bakeTranslateZ or bakeRotateY):
            cmds.warning('Invalid bake options.\nPlease turn on bake target checkbox.')
            return

        options = {
            'bakeTranslateX': bakeTranslateX,
            'bakeTranslateZ': bakeTranslateZ,
            'bakeRotateY': bakeRotateY,
        }

        logger.info('Bake moveCtrl : namespace = {}, options = {}'.format(namespace, str(options)))

        # options['bakeTranslateY'] = True
        # options['useBBox'] = True

        command.bake_move_ctrl(
            namespace=namespace, **options
        )

        self.save_settings()

    def get_namespace(self):
        """選択ノードからネームスペースを取得
        """

        sels = cmds.ls(sl=True)
        if not sels:
            # cmds.warning(u'選択ノードからネームスペースを取得します。\nリグアセットのコントローラーを選択してください。')
            return ''

        return lib_maya.get_object_namespace(sels[0]).strip(':').split(':', 1)[0]
