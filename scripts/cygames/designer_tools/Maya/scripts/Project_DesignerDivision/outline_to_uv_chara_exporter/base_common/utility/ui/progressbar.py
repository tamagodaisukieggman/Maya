# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds


# ===============================================
def start(title):

    end()

    cmds.progressWindow(title=title, status="",
                         isInterruptable=True, min=0, max=100)


# ===============================================
def update(info, current_count, max_count, whole_current_count, whole_max_count):

    value = current_count / max_count * 100

    fix_info = None

    if whole_max_count > 1:

        fix_info = '{0}  {1}/{2}  ({3}/{4})'.format(
            info, current_count, max_count, whole_current_count, whole_max_count)

    else:

        fix_info = '{0}  {1}/{2}'.format(
            info, current_count, max_count)

    cmds.progressWindow(
        edit=True, progress=value, status=fix_info)

    if cmds.progressWindow(query=True, isCancelled=True):
        end()
        return False

    return True


# ===============================================
def end():

    cmds.progressWindow(endProgress=True)
