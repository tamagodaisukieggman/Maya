# -*- coding: utf-8 -*-
u"""選択したエッジの隣接ポリゴンを指定した距離で分割 (GUI)

:詳細: file:///Z:/mtku/tools/maya/doc/manual/sources/modeling/insertedges.rst

..
    BEGIN__CYGAMES_MENU
    label=CyInsertEdges ... : 選択したエッジの隣接ポリゴンを分割 ...
    command=main()
    order=1000
    END__CYGAMES_MENU

    END__CYGAMES_DESCRIPTION
"""
from mtku.maya.mtklog import MtkLog

from .gui import InsertEdges
from .command import InsertEdgesCmd


__all__ = ('InsertEdges', 'InsertEdgesCmd')

logger = MtkLog(__name__)


def main():
    u"""InsertEdgesの実行"""
    logger.debug(u'InsertEdges')
    logger.usage()

    win = InsertEdges()
    win.width = 485
    win.height = 285
    win.show()
