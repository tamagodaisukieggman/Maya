# -*- coding: utf-8 -*-

from __future__ import absolute_import

import maya.cmds as cmds

from . import command


def save_optionvar(key, value, force=True):
    """optionVarに保存

    :param str key: キー名
    :param mixin value: 値
    :param bool force: 強制的に上書きするかのブール値

    :return: 保存できたかどうかのブール値
    :rtype: bool
    """

    v = str(value)
    if force:
        cmds.optionVar(sv=[key, v])
        return True
    else:
        if not cmds.optionVar(ex=key):
            cmds.optionVar(sv=[key, v])
            return True
        else:
            return False


def load_optionvar(key):
    """optionVarを取得

    :param str key: キー名
    :return: 保存された値, キーが見つからない場合は None
    :rtype: value or None
    """

    if cmds.optionVar(ex=key):
        return eval(cmds.optionVar(q=key))
    else:
        return None


class ResurfTool(object):

    def __init__(self, *args, **kwargs):
        super(ResurfTool, self).__init__(*args, **kwargs)

        self._tool_name = 'resurf_tool'
        self.title = 'Resurf Tool'

        self.width = 400
        self.height = 100
        self.margin = 2

        self.apply_translate = None
        self.apply_rotate = None

        self.correct_by_weights = None

        self.base_geometry = None
        self.target_geometry = None
        self.skinned_geometry = None

        self.reset_btn = None
        self.apply_fit_joints = None

        self.button_texts = [
            'Please select target joints',
            'Apply Fit Joints'
        ]

    def show(self):
        self.close()

        win = cmds.window(self._tool_name, title=self.title, mb=True, w=self.width, h=self.height)

        # Menu
        editMenu = cmds.menu(label='Edit', p=win)
        cmds.menuItem(label='Save Settings', p=editMenu, c=self.save_settings)
        cmds.menuItem(label='Reset Settings', p=editMenu, c=self.reset_and_save_settings)

        mainLay = cmds.formLayout(p=win, nd=100)
        mainColumn = cmds.columnLayout(adj=True, p=mainLay, rs=2)

        #
        cmds.text(label='Please set Base and Target Geometry.',
                  p=mainColumn, h=24, fn='boldLabelFont', bgc=[0.4, 0.4, 0.4])

        cmds.separator(style='in', h=10, p=mainColumn)

        # base geometry
        basegeo_lay = cmds.rowLayout(nc=3, cw3=(120, 100, 50), cl3=['center', 'left', 'left'], adj=2,
                                     ct3=['right', 'left', 'left'], p=mainColumn)

        cmds.text(label='Base : ', p=basegeo_lay,
                  ann=u'ベース形状ジオメトリ')

        self.base_geometry = cmds.textField(ed=True, p=basegeo_lay)
        cmds.button(label='Set', w=50, p=basegeo_lay, c=self.set_base_geometry)

        # target geometry
        targetgeo_lay = cmds.rowLayout(nc=3, cw3=(120, 100, 50), cl3=['center', 'left', 'left'], adj=2,
                                       ct3=['right', 'left', 'left'], p=mainColumn)

        cmds.text(label='Target : ', p=targetgeo_lay,
                  ann=u'ターゲットジオメトリ')

        self.target_geometry = cmds.textField(ed=True, p=targetgeo_lay)
        cmds.button(label='Set', w=50, p=targetgeo_lay, c=self.set_target_geometry)

        # skinned geometry
        skinnedgeo_lay = cmds.rowLayout(nc=3, cw3=(120, 100, 50), cl3=['center', 'left', 'left'], adj=2,
                                        ct3=['right', 'left', 'left'], p=mainColumn)

        cmds.text(label='Skinned (option): ', p=skinnedgeo_lay,
                  ann=u'Correct by Weights オプション用 : skinClusterのウェイト取得用')

        self.skinned_geometry = cmds.textField(ed=True, p=skinnedgeo_lay)
        cmds.button(label='Set', w=50, p=skinnedgeo_lay, c=self.set_skinned_geometry)

        # apply target
        apply_target_lay = cmds.rowLayout(nc=3, cw3=(120, 100, 100), cl3=['center', 'left', 'left'],
                                          ct3=['right', 'left', 'left'], p=mainColumn)

        cmds.text(label='Compose Targets : ', p=apply_target_lay, ann=u'Transformを統合するコントローラー')
        self.apply_translate = cmds.checkBox(label='Translate', v=True, p=apply_target_lay)
        self.apply_rotate = cmds.checkBox(label='Rotate', v=False, p=apply_target_lay)

        cmds.checkBox(self.apply_translate, e=True,
                      cc=self.on_apply_target_changed)

        cmds.checkBox(self.apply_rotate, e=True,
                      cc=self.on_apply_target_changed)

        # correct by weight
        correctlay = cmds.rowLayout(nc=2, cw2=(120, 100), cl2=['center', 'left'], adj=2,
                                    ct2=['right', 'left'], p=mainColumn)

        cmds.text(label='', p=correctlay)
        self.correct_by_weights = cmds.checkBox(label='Correct by Weights', v=True, p=correctlay,
                                                ann=u'skinClusterのウェイトを利用して回転値に補正加えます。')

        cmds.separator(style='in', h=10, p=mainColumn)

        btn_lay = cmds.formLayout(nd=100, p=mainColumn)
        self.reset_btn = cmds.button(label='Reset', h=40, p=btn_lay, c=self.on_reset_joints)

        self.apply_fit_joints = cmds.button(label=self.button_texts[0], h=40, bgc=[0.4, 0.4, 0.4],
                                            p=btn_lay, c=self.on_apply_fit_joints)

        cmds.formLayout(btn_lay, e=True,
                        af=[[self.reset_btn, 'top', self.margin],
                            [self.reset_btn, 'left', self.margin],
                            [self.reset_btn, 'bottom', self.margin],
                            [self.apply_fit_joints, 'top', self.margin],
                            [self.apply_fit_joints, 'right', self.margin],
                            [self.apply_fit_joints, 'bottom', self.margin]],
                        ap=[[self.reset_btn, 'right', self.margin, 20],
                            [self.apply_fit_joints, 'left', self.margin, 20]
                            ]
                        )

        cmds.formLayout(mainLay, e=True,
                        af=[[mainColumn, 'top', self.margin],
                            [mainColumn, 'left', self.margin],
                            [mainColumn, 'right', self.margin],
                            [mainColumn, 'bottom', self.margin],
                            ],
                        )

        cmds.showWindow(win)
        cmds.window(win, e=True, w=self.width, h=self.height)

        cmds.scriptJob(e=['SelectionChanged', self.selection_changed], p=win, rp=True)

        self.selection_changed()

        self.reset_settings()
        self.read_settings()

    def close(self):
        if cmds.window(self._tool_name, q=True, ex=True):
            cmds.deleteUI(self._tool_name)

    def get_settings(self, *args):
        """設定の取得"""

        return {
            'target_geometry': cmds.textField(self.target_geometry, q=True, tx=True),
            'base_geometry': cmds.textField(self.base_geometry, q=True, tx=True),
            'skinned_geometry': cmds.textField(self.skinned_geometry, q=True, tx=True),
            'apply_translate': cmds.checkBox(self.apply_translate, q=True, v=True),
            'apply_rotate': cmds.checkBox(self.apply_rotate, q=True, v=True),
            'correct_by_weights': cmds.checkBox(self.correct_by_weights, q=True, v=True)
        }

    def read_settings(self, *args):
        """optionVarから設定をロード
        """

        read_values = load_optionvar('%s__ui_options' % self._tool_name)
        if read_values:
            try:
                if 'target_geometry' in read_values:
                    v = read_values.get('target_geometry', '')
                    cmds.textField(self.target_geometry, e=True, tx=v)

                if 'base_geometry' in read_values:
                    v = read_values.get('base_geometry', '')
                    cmds.textField(self.base_geometry, e=True, tx=v)

                if 'skinned_geometry' in read_values:
                    v = read_values.get('skinned_geometry', '')
                    cmds.textField(self.skinned_geometry, e=True, tx=v)

                if 'apply_translate' in read_values:
                    v = read_values.get('apply_translate', True)
                    cmds.checkBox(self.apply_translate, e=True, v=v)

                if 'apply_rotate' in read_values:
                    v = read_values.get('apply_rotate', True)
                    cmds.checkBox(self.apply_rotate, e=True, v=v)

                if 'correct_by_weights' in read_values:
                    v = read_values.get('correct_by_weights', True)
                    cmds.checkBox(self.correct_by_weights, e=True, v=v)

            except Exception as e:
                cmds.error(e)
                self.reset_settings()

    def save_settings(self, *args):
        """設定の保存
        """
        settings = self.get_settings()
        save_optionvar('%s__ui_options' % self._tool_name, settings)

    def reset_settings(self, *args):
        """設定のリセット"""

        cmds.textField(self.target_geometry, e=True, tx='')
        cmds.textField(self.base_geometry, e=True, tx='')
        cmds.textField(self.skinned_geometry, e=True, tx='')
        cmds.checkBox(self.apply_translate, e=True, v=True)
        cmds.checkBox(self.apply_rotate, e=True, v=True)
        cmds.checkBox(self.correct_by_weights, e=True, v=True)

    def reset_and_save_settings(self, *args):
        """設定のリセット＆保存
        """

        self.reset_settings()
        self.save_settings()

    def on_apply_target_changed(self, *args):
        settings = self.get_settings()
        cmds.button(
            self.apply_fit_joints, e=True,
            en=settings.get('apply_translate') or settings.get('apply_rotate'))

        cmds.checkBox(self.correct_by_weights, e=True, en=settings.get('apply_rotate'))

    def set_base_geometry(self, *args):
        cmds.textField(self.base_geometry, e=True, tx='')

        sels = cmds.ls(sl=True, o=True)
        if not sels:
            return

        shapes = cmds.listRelatives(sels, s=True, pa=True, type='mesh')
        if not shapes:
            return

        geo = cmds.listRelatives(shapes, p=True, pa=True)[0]
        cmds.textField(self.base_geometry, e=True, tx=geo)

    def set_target_geometry(self, *args):
        cmds.textField(self.target_geometry, e=True, tx='')

        sels = cmds.ls(sl=True, o=True)
        if not sels:
            return

        shapes = cmds.listRelatives(sels, s=True, pa=True, type='mesh')
        if not shapes:
            return

        geo = cmds.listRelatives(shapes, p=True, pa=True)[0]
        cmds.textField(self.target_geometry, e=True, tx=geo)

    def set_skinned_geometry(self, *args):
        cmds.textField(self.skinned_geometry, e=True, tx='')

        sels = cmds.ls(sl=True, o=True)
        if not sels:
            return

        shapes = cmds.listRelatives(sels, s=True, pa=True, type='mesh')
        if not shapes:
            return

        geo = cmds.listRelatives(shapes, p=True, pa=True)[0]
        skinclusters = command.list_related_skinClusters([geo])
        if not skinclusters:
            return

        cmds.textField(self.skinned_geometry, e=True, tx=geo)

    def selection_changed(self, *args):
        joints = cmds.ls(sl=True, et='joint')
        enable = bool(joints)
        cmds.button(self.apply_fit_joints, e=True,
                    label=self.button_texts[enable],
                    en=enable)
        cmds.button(self.reset_btn, e=True, en=enable)

    def on_reset_joints(self, *args):
        joints = cmds.ls(sl=True, et='joint')
        if not joints:
            cmds.warning(u'移動させるジョイントを選択して下さい。')
            return

        command.reset_joints(joints)

        # settings = self.get_settings()
        #
        # command.reset_joints(
        #     joints,
        #     reset_translate=settings.get('apply_translate', True),
        #     reset_rotate=settings.get('apply_rotate', True)
        # )

    def on_apply_fit_joints(self, *args):
        """
        """

        settings = self.get_settings()

        joints = cmds.ls(sl=True, et='joint')
        if not joints:
            cmds.warning(u'移動させるジョイントを選択して下さい。')
            return

        # print('fit_joints({}, {})'.format(joints, settings))

        command.fit_joints(
            joints,
            **settings
        )

        self.save_settings()
