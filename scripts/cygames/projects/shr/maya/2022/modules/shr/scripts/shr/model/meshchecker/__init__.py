# -*- coding: utf-8 -*-
u"""メッシュチェッカー

:詳細: file:///Z:/mtku/tools/maya/doc/manual/sources/window/meshchecker.rst

..
    BEGIN__CYGAMES_MENU
    label=CyMeshChecker ...: メッシュチェッカー ...
    command=main()
    order=6000
    END__CYGAMES_MENU

    END__CYGAMES_DESCRIPTION
"""
from mtku.maya.mtklog import MtkLog

from .gui import MeshChecker

logger = MtkLog(__name__)
UI_NAME = 'CyMeshChecker'


def main():
    u"""main関数"""
    logger.usage()
    win = MeshChecker(title=UI_NAME, typ=2)
    win.height = 300
    win.width = 450
    win.show()
