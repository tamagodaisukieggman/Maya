# -*- coding=utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pymel.core as pmc


def set_color_space(color_space='Raw'):
    spaces = pmc.colorManagementPrefs(query=True, viewTransformNames=True)
    current_space = get_color_space()

    if color_space == current_space:
        return

    if color_space in spaces:
        try:
            pmc.colorManagementPrefs(edit=True, viewTransformName=color_space)
        except RuntimeError as err:
            pmc.system.warning(err)
        else:
            print('Preference > Set color space: {}'.format(color_space))
    else:
        pass


def get_color_space():
    current_space = pmc.colorManagementPrefs(query=True, viewTransformName=True)
    print('Preference > Current color space: {}'.format(current_space))
    return current_space


def is_srgb():
    return 'sRGB gamma' == get_color_space()


def is_raw():
    return 'Raw' == get_color_space()


def convert_color(color=[0.5, 0.5, 0.5]):
    return pmc.colorManagementConvert(toDisplaySpace=color)


def undo_chunk(fnc):
    """Decorator."""

    def wrapper(*args, **kwargs):
        pmc.undoInfo(openChunk=True)
        result = fnc(*args, **kwargs)
        pmc.undoInfo(closeChunk=True)
        return result

    return wrapper
