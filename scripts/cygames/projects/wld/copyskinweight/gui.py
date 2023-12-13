# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging

import maya.cmds as cmds

from . import command

logger = logging.getLogger('copyskinweight')


class CopySkinWeightGUI(object):
    """CopySkinWeight GUI
    """

    copy_method_labels = [
        'Closest point on surface',
        'Closest component',
        'UV space',
    ]

    copy_methods = [
        'closestPoint',
        'closestComponent',
        'uvspace',
    ]

    copy_target_method_labels = [
        'by Name',
        'by Hierarchy'
    ]

    copy_target_methods = [
        'name',
        'hierarchy'
    ]

    copy_target_method_annotates = [
        u'同名のオブジェクト同士でウェイトのコピーを行います。',
        u'オブジェクトの階層順でウェイトのコピーを行います。'
    ]

    def __init__(self, *args, **kwargs):
        super(CopySkinWeightGUI, self).__init__(*args, **kwargs)

        self._tool_name = 'copyskinweight'
        self.title = 'Copy Skin Weight'

        self.width = 300
        self.height = 100
        self.margin = 2

        self.copy_method = None
        self.copy_target_method = None

    def show(self):
        """GUIの表示
        """

        self.close()

        win = cmds.window(self._tool_name, title=self.title, mb=True, w=self.width, h=self.height)

        # Main Layout
        main_lay = cmds.formLayout(p=win, nd=100)
        main_column_lay = cmds.columnLayout(rs=4, adj=True, p=main_lay)

        cmds.text(label=u'コピー元 / コピー先 の順に対象を選択して下さい。',
                  fn='boldLabelFont',
                  h=30, p=main_column_lay, bgc=[0.4, 0.4, 0.4])

        col = cmds.columnLayout(adj=True, p=main_column_lay)
        cmds.text(label='    Surface Association',
                  fn='boldLabelFont', al='left', p=col, h=20)
        self.copy_method = cmds.radioCollection(p=col)
        for _method, _method_label in zip(self.copy_methods, self.copy_method_labels):
            _row = cmds.rowLayout(
                nc=2, cw2=[50, 100], cl2=['right', 'left'], ct2=['both', 'left'], p=col)
            cmds.text(label='', w=50, p=_row)
            cmds.radioButton('copy_{}'.format(_method), label=_method_label, p=_row, collection=self.copy_method)

        col = cmds.columnLayout(adj=True, p=main_column_lay)
        cmds.text(label='    Target specification method',
                  fn='boldLabelFont', al='left', p=col, h=20)
        self.copy_target_method = cmds.radioCollection(p=col)
        for _method, _method_label, _method_ann in \
                zip(self.copy_target_methods, self.copy_target_method_labels, self.copy_target_method_annotates):

            _row = cmds.rowLayout(
                nc=2, cw2=[50, 100], cl2=['right', 'left'], ct2=['both', 'left'], p=col)
            cmds.text(label='', w=50, p=_row)
            cmds.radioButton(
                'copytarget_{}'.format(_method),
                ann=_method_ann, label=_method_label, p=_row, collection=self.copy_target_method)

        cmds.button(label='Execute Copy Weights', c=self._on_copy_btn, p=main_column_lay)

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

    def close(self):
        """GUIを閉じる
        """

        if cmds.window(self._tool_name, q=True, ex=True):
            cmds.deleteUI(self._tool_name)

    def read_settings(self, *args):
        """optionVarから設定をロード
        """

        read_values = command.load_optionvar('%s__ui_options' % self._tool_name)
        if read_values:
            try:
                if 'copy_method' in read_values:
                    cmds.radioCollection(
                        self.copy_method, e=True, sl=read_values.get('copy_method', 'closestPoint'))

                if 'copy_target_method' in read_values:
                    cmds.radioCollection(
                        self.copy_target_method, e=True, sl=read_values.get('copy_target_method', 'name'))

            except Exception as e:
                cmds.error(e)
                self.reset_settings()

    def save_settings(self, *args):
        """設定の保存
        """
        settings = self.get_settings()
        command.save_optionvar('%s__ui_options' % self._tool_name, settings)

    def reset_settings(self, *args):
        """設定のリセット
        """

        cmds.radioCollection(self.copy_method, e=True, sl='copy_closestPoint')
        cmds.radioCollection(self.copy_target_method, e=True, sl='copytarget_name')

    def remove_settings(self, *args):
        """設定の削除
        """

        command.remove_optionvar('%s__ui_options' % self._tool_name)

    def get_settings(self, *args):
        """bind_copyの設定を取得
        :return: bind_copy設定の辞書
        :rtype: dict
        """

        return {
            'copy_method': cmds.radioCollection(self.copy_method, q=True, sl=True),
            'copy_target_method': cmds.radioCollection(self.copy_target_method, q=True, sl=True),
        }

    @staticmethod
    def _copy_by_name(src_geos, dst_geos, copy_method='closestPoint'):
        ret = []

        with command.ProgressWindowBlock(title='Copy Weights Progress', maxValue=len(src_geos)) as prg:
            prg.status = 'Copy Weights Start'
            prg.step(1)

            for src_geo in src_geos:
                prg.status = src_geo
                prg.step(1)

                src_geo_shortname = src_geo.rsplit('|', 1)[-1]

                found_geo = None
                for dst_geo in dst_geos:
                    dst_geo_shortname = dst_geo.rsplit('|', 1)[-1]
                    if src_geo_shortname == dst_geo_shortname:
                        found_geo = dst_geo
                        break

                if not found_geo:
                    logger.info('[ Copy Weights ] : Skip : {}'.format(src_geo))
                    continue

                logger.info('[ Copy Weights ] : {} to {}'.format(src_geo, found_geo))
                command.bind_and_copy(
                    src_geo, found_geo,
                    bind=True,
                    method=copy_method
                )

                ret.append(found_geo)

                if prg.is_cancelled():
                    break

        return ret

    @staticmethod
    def _copy_by_hierarchy(src_geos, dst_geos, copy_method='closestPoint'):
        ret = []

        with command.ProgressWindowBlock(title='Copy Weights Progress', maxValue=len(src_geos)) as prg:
            prg.status = 'Copy Weights Start'
            prg.step(1)

            for src_geo, dst_geo in zip(src_geos, dst_geos):
                prg.status = src_geo
                prg.step(1)

                logger.info('[ Copy Weights ] : {} to {}'.format(src_geo, dst_geo))
                command.bind_and_copy(
                    src_geo, dst_geo,
                    bind=True,
                    method=copy_method,
                )

                ret.append(dst_geo)

                if prg.is_cancelled():
                    break

        return ret

    def _on_copy_btn(self, *args):
        """copy weights
        """

        sels = cmds.ls(sl=True, et='transform') or []
        if len(sels) < 2:
            logger.warning(u'コピー元 / コピー先ジオメトリを選択して下さい。')
            return

        bind_copy_settings = self.get_settings()

        method = bind_copy_settings.get('copy_method', 'closestPoint').replace('copy_', '')
        copy_target_method = bind_copy_settings.get('copy_target_method', 'name').replace('copytarget_', '')

        src_shapes = cmds.ls(cmds.listRelatives(sels[0], ad=True, pa=True), ni=True, type='controlPoint')
        if not src_shapes:
            logger.warning(u'コピー元ジオメトリが見つかりません。')
            return

        src_geos = cmds.listRelatives(src_shapes, p=True, pa=True)

        dst_shapes = cmds.ls(cmds.listRelatives(sels[1], ad=True, pa=True), ni=True, type='controlPoint')
        if not dst_shapes:
            logger.warning(u'コピー先ジオメトリが見つかりません。')
            return
        dst_geos = cmds.listRelatives(dst_shapes, p=True, pa=True)

        if copy_target_method == 'name':
            self._copy_by_name(src_geos, dst_geos, copy_method=method)

        elif copy_target_method == 'hierarchy':
            self._copy_by_hierarchy(src_geos, dst_geos, copy_method=method)

        cmds.select(sels, r=True)

        self.save_settings()
