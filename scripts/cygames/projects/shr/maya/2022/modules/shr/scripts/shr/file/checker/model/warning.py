# -*- coding: utf-8 -*-
u"""警告ウィンドウ"""
from functools import partial
from pprint import pprint
import sys

import maya.cmds as cmds

from mtku.maya.base.window import BaseWindow
# from mtku.maya.mtklog import MtkLog
from .utils import ModelCheckerUtils

config_node = None
CYLISTA_SCRIPT_PATH = "Z:/cyllista/tools/maya/modules/cyllista/scripts/"

if CYLISTA_SCRIPT_PATH not in sys.path:
    sys.path.append(CYLISTA_SCRIPT_PATH)

try:
    import cyllista.config_node as config_node
except Exception:
    print('can\'t import "config_node"')
    exit(1)

# logger = MtkLog(__name__)


class WarningWindow(BaseWindow):

    def __init__(self, *args, **kwargs):
        u"""初期化"""
        super(WarningWindow, self).__init__(*args, **kwargs)
        # self._typ = 2
        self.window = 'MtkCheckerWarning'
        self.width = 800
        self.height = 400

        self._infos = kwargs.setdefault('info', [])
        # logger.debug(self._infos)

        self.common_checkbox_values = {}

        self.inf_num = 4
        

    def get_cylista_config_node_data(self):
        if config_node:
            config = config_node.get_config()
            self.inf_num = config.get("cySkinInfluenceCountMax", 4)

    def create(self):
        u"""Windowのレイアウト作成"""
        self.common_checkbox_values = self.add_layout('Result')

    def add_layout(self, label):
        u"""レイアウトを追加

        :param label: ラベル
        :return: {checkbox: values}
        """

        self.get_cylista_config_node_data()
        checkbox_values = {}

        cmds.frameLayout(l=label, cl=False, cll=True)

        form = cmds.formLayout(nd=100)

        column = cmds.columnLayout(adj=1)

        for info in self._infos:
            visible = True
            enable = True
            if not info.get('modifier'):
                info['modifier'] = None
                enable = False
            deletes_history = int(info['history']) if info.get('history') else 0
            all_ = int(info['history']) if info.get('history') else 0

            sub_form = cmds.formLayout()
            # text = cmds.text(l=error_text,  h=26, w=380, al='left')
            # cmds.rowLayout(numberOfColumns=2, columnWidth2=[200,200])
            if info['checker'] == "has_many_bind":
                checkbox = cmds.checkBox(l=u"{}".format(info['error_text'].format(self.inf_num)), h=26, w=580, v=enable, en=enable)
            else:
                checkbox = cmds.checkBox(l=u"{}".format(info['error_text']), h=26, w=580, v=enable, en=enable)
            # checkbox = cmds.checkBox(l=u"{}     [  {}  ]個のエラー".format(info['error_text'], len(info['error_nodes'])), h=26, w=580, v=enable, en=enable)
            _text = cmds.text(label=u"[  {}  ]  個のエラー".format(len(info['error_nodes'])))
            # cmds.setParent("..")
            select_btn = cmds.button(l=u'選択', w=75, c=partial(self._select, info['error_nodes']))
            modify_btn = cmds.button(
                l=u'修正', w=75,
                c=partial(
                    self._modify,
                    info['modifier'], info['error_nodes'],
                    deletes_history=deletes_history, all=all_,
                ),
                en=enable, vis=visible,
            )

            checkbox_values[checkbox] = info

            cmds.formLayout(
                sub_form, e=True,
                af=(
                    [checkbox, 'top', 0],
                    [checkbox, 'left', 0],
                    [_text, 'top', 7],
                    [_text, 'left', 80],
                    [select_btn, 'top', 0],
                    [modify_btn, 'top', 0],
                    [modify_btn, 'right', 0],
                ),
                ac=(
                    [checkbox, 'right', 4, select_btn],
                    [_text, 'right', 4, select_btn],
                    [select_btn, 'right', 4, modify_btn],
                ),
            )
            cmds.setParent('..')  # sub_form

        cmds.formLayout(
            form, e=True,
            af=(
                [column, 'top', 10],
                [column, 'left', 25],
                [column, 'bottom', 10],
            ),
        )
        cmds.setParent('..')  # columnLayout

        cmds.setParent('..')  # formLayout

        cmds.setParent('..')  # frameLayout

        return checkbox_values

    def _select(self, nodes, *args):
        u"""選択

        :param nodes: 選択
        """
        try:
            cmds.select(nodes)
        except:pass
        # print('{0:=<79}'.format(''))
        # pprint(nodes)

    def _modify(self, modifier, nodes, *args, **kwargs):
        u"""修正用関数の実行


        :param nodes: ノードのリスト
        :param modifier: 修正用関数の文字列
        """
        cmds.warning(u"現在自動修正には対応しておりません")
        return

        deletes_history = kwargs.setdefault('deletes_history', False)
        all = kwargs.setdefault('all', False)
        dialog = kwargs.setdefault('dialog', True)

        ModelCheckerUtils.modify(
            modifier, nodes,
            deletes_history=deletes_history,
            all=all,
        )

        if dialog:
            cmds.confirmDialog(m=u'修正しました\n\n詳細はScriptEditorをご覧ください', b=['OK'])

        # WarningWindowの
        for info in self._infos:
            if info['modifier'] == modifier:
                self._infos.remove(info)
                break
        # print(self._infos)
        self.close()
        if self._infos:
            self.show()

    def apply_(self, *args):
        u"""一括修正"""
        cmds.warning(u"現在自動修正には対応しておりません")
        return
        
        for checkbox, values in sorted(self.common_checkbox_values.items()):
            if not cmds.checkBox(checkbox, q=True, v=True):
                continue

            ModelCheckerUtils.modify(
                values['modifier'], values['error_nodes'],
                deletes_history=int(values['history']),
                all=values['all'],
                dialog=False,
            )

        cmds.confirmDialog(m=u'修正しました\n\n詳細はScriptEditorをご覧ください', b=['OK'])
        self.close()


def main(info):
    u"""main関数"""
    win = WarningWindow(info=info)
    win.show()
