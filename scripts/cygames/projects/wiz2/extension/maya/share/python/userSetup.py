# -*- coding: utf-8 -*-

import sys
import maya.utils

sys.dont_write_bytecode = True


def create_menu():
    world_menu_builder.core.main()


if __name__ == '__main__':
    import world_menu_builder.core
    maya.utils.executeDeferred(create_menu)
