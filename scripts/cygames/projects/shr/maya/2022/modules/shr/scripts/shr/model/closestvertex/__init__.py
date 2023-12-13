# -*- coding: utf-8 -*-
u"""クロースドバーテクッス(GUI)

..
    BEGIN__CYGAMES_MENU
    label=ClosestVertex ... : メッシュの近傍頂点へ各頂点を移動...
    command=main()
    order=1000
    END__CYGAMES_MENU

"""

from mtku.maya.mtklog import MtkLog
from .gui import ClosestVertex
from .command import get_closest_point
from .command import get_mesh
from .command import run_vertex
from .command import run_surface


__all__ = ('get_closest_point', 'get_mesh', 'run_vertex', 'run_surface')
logger = MtkLog(__name__)


def main():
    u"""Window表示"""
    logger.usage()
    win = ClosestVertex(typ=2)
    win.width = 320
    win.height = 180
    win.show()
