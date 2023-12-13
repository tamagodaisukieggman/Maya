# -*- coding: utf-8 -*-

import maya.cmds as cmds


# ===============================================
def open_yes_no(title, info, parent=None):
    result = ''

    yes_text = u'Yes'
    no_text = u'No'

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
    result = ''

    ok_text = u'Ok'

    if parent is None:

        cmds.confirmDialog(
            title=title,
            message=info,
            button=ok_text,
            ma='center'
        )

    else:

        cmds.confirmDialog(
            title=title,
            message=info,
            button=ok_text,
            ma='center',
            parent=parent
        )
