# -*- coding: utf-8 -*-
import sys
from importlib import reload
from . import window
from . import command
reload(window)
reload(command)
from .window import MiniMapRenderWindow
from .command import MiniMapRender

sys.dont_write_bytecode = True

__all__ = (
    'MiniMapRenderWindow',
    'MiniMapRender',
)


def main():
    win = MiniMapRenderWindow()
    win.show()
