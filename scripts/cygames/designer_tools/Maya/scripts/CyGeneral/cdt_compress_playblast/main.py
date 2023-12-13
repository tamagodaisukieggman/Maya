# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import maya.cmds as cmds

try:
    from builtins import object
except Exception:
    pass


class Main(object):
    def show_ui(self):
        # 内部で使用しているffmpegが社内規定によりPJごとの申請が必要なためGeneralのメニューからは削除
        # gallopから情報やコードの提供は行えるので、問い合わせがあった場合はffmpegの申請を行ったうえでgallopのTAまで相談ください
        message = '本ツールは内部ソフトの社内規定によりgallop限定となりました\n使用したい方はPJのテクニカルアーティストに相談してください'
        cmds.confirmDialog(m=message)
