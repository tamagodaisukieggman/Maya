# -*- coding: utf-8 -*-

"""
Gallop BG用エクスポートツール
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

from . import commands
from . import constants
from . import gui

reload(commands)
reload(constants)
reload(gui)


def main():
    """
    on main

    """

    # 必要なプラグインをチェック
    commands.check_plugin()

    gui.MainWindow().show()


if __name__ == '__main__':
    main()
