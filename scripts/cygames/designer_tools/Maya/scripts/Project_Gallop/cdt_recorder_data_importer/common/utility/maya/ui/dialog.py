# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds


# ===============================================
def open_yes_no(title, info, parent=None):

    result = ''

    yes_text = 'Yes'
    no_text = 'No'

    if parent is None:

        result = cmds.confirmDialog(
            title=title,
            message=info,
            button=[yes_text, no_text],
            defaultButton=yes_text,
            cancelButton=no_text,
            dismissString=no_text,
            ma='center'
        )

    else:

        result = cmds.confirmDialog(
            title=title,
            message=info,
            button=[yes_text, no_text],
            defaultButton=yes_text,
            cancelButton=no_text,
            dismissString=no_text,
            ma='center',
            parent=parent
        )

    if result == no_text:
        return False

    return True


# ===============================================
def open_ok(title, info, parent=None):

    ok_text = 'Ok'

    fix_info = ''
    if type(info) == list:

        for this_info in info:
            fix_info += this_info + '\n'
    else:
        fix_info = info

    if parent is None:

        cmds.confirmDialog(
            title=title,
            message=fix_info,
            button=ok_text,
            ma='center'
        )

    else:

        cmds.confirmDialog(
            title=title,
            message=fix_info,
            button=ok_text,
            ma='center',
            parent=parent
        )
