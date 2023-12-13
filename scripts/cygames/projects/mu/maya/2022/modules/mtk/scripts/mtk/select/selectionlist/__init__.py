# -*- coding: utf-8 -*-
u"""Selection List (GUI)

..
    BEGIN__CYGAMES_MENU
    label=Selection List ...
    command=main()
    order=1000
    END__CYGAMES_MENU

"""

from . import gui
from mtk import logger


def main():
    u"""main関数"""
    logger.send_launch('Selection List')

    ui = gui.SelectionListGUI()
    ui.show()
