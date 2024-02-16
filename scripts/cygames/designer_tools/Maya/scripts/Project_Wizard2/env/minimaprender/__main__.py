# -*- coding: utf-8 -*-
# from batch import MiniMapRenderBatch
from importlib import reload
from . import batch
reload(batch)
from .batch import MiniMapRenderBatch


if __name__ == '__main__':
    import sys

    import maya.standalone

    args = sys.argv
    if len(args) < 2:
        sys.exit(1)

    maya.standalone.initialize(name='python')

    maya_file_paths = args[1:]

    MiniMapRenderBatch.exec_(maya_file_paths)

    maya.standalone.uninitialize()
    sys.exit(0)
