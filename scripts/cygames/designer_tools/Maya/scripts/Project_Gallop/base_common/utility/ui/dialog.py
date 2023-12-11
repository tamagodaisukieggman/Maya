# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from functools import partial

import maya.cmds as cmds

try:
    # Maya 2022-
    from builtins import str
except Exception:
    pass

_g_ok_text = 'OK'
_g_cancel_text = 'Cancel'


# ===============================================
def open_ok(title, info, parent=None):

    _create_dialog(title, info, None, False, parent)


# ===============================================
def open_ok_with_scroll(title, info, info_for_scroll, parent=None):

    _create_dialog(title, info, info_for_scroll, False, parent)


# ===============================================
def open_ok_cancel(title, info, parent=None):

    if _create_dialog(title, info, None, True, parent) != _g_ok_text:
        return False

    return True


# ===============================================
def open_ok_cancel_with_scroll(title, info, info_for_scroll, parent=None):

    if _create_dialog(title, info, info_for_scroll, True, parent) != _g_ok_text:
        return False

    return True


# ===============================================
def _create_dialog(title, info, info_for_scroll, show_cancel, parent):

    result_value = None

    if parent:

        result_value = cmds.layoutDialog(
            title=title,
            parent=parent,
            ui=partial(__create_dialog_base, info, info_for_scroll, show_cancel, parent)
        )

    else:

        result_value = cmds.layoutDialog(
            title=title,
            ui=partial(__create_dialog_base, info, info_for_scroll, show_cancel, parent)
        )

    return result_value


# ===============================================
def __create_dialog_base(info, info_for_scroll, show_cancel, parent):

    # ------------------
    # インフォの整形

    fix_info = ''

    if info:

        try:
            fix_info = str(info)
        except Exception:
            fix_info = info

    # ------------------
    # リスト用インフォの整形

    fix_info_for_scroll_str = ''
    fix_info_for_scroll_count = -1

    if info_for_scroll:

        info_for_scroll_type = type(info_for_scroll)

        if info_for_scroll_type == list or info_for_scroll_type == tuple:

            count = -1
            for info_value in info_for_scroll:
                count += 1

                try:
                    fix_info_for_scroll_str += str(info_value)
                except Exception:
                    fix_info_for_scroll_str = info_value

                if count < len(info_for_scroll) - 1:
                    fix_info_for_scroll_str += '\n'

            fix_info_for_scroll_count = len(info_for_scroll)

        else:

            try:
                fix_info_for_scroll_str = str(info_for_scroll)
            except Exception:
                fix_info_for_scroll_str = info_for_scroll

    # ------------------
    # レイアウト取得

    this_formlayout = cmds.setParent(q=True)

    # ------------------
    # テキスト

    this_text_field = None

    if fix_info:

        this_text_field = cmds.text(
            label=fix_info, wordWrap=True
        )

    this_scroll_field = None
    this_subtext_field = None

    if fix_info_for_scroll_str:

        if this_text_field:
            cmds.text(this_text_field, e=True, align='left')

        this_scroll_field = cmds.scrollField(
            wordWrap=True, editable=False, text=fix_info_for_scroll_str
        )

        if fix_info_for_scroll_count >= 0:

            this_subtext_field = cmds.text(
                label='リスト数 : {0}'.format(fix_info_for_scroll_count),
                wordWrap=True, align='right'
            )

    # ------------------
    # ボタン

    button_width = 100

    default_button = None
    cancel_button = None

    default_button = cmds.button(
        label=_g_ok_text, w=button_width,
        c='cmds.layoutDialog(dismiss="{0}")'.format(_g_ok_text))

    if show_cancel:

        cancel_button = cmds.button(
            label=_g_cancel_text, w=button_width,
            c='cmds.layoutDialog(dismiss="{0}")'.format(_g_cancel_text))

    # ------------------
    # テキストアタッチ

    if this_scroll_field:

        cmds.formLayout(this_formlayout, e=True, w=400, h=300)

        scroll_top_value = 10
        scroll_bottom_value = 50

        if this_text_field:

            scroll_top_value = 30

            cmds.formLayout(this_formlayout, e=True,
                            attachForm=[
                                (this_text_field, 'top', 10),
                                (this_text_field, 'left', 10),
                                (this_text_field, 'right', 10)
                            ])

        if this_subtext_field:

            scroll_bottom_value = 70

            cmds.formLayout(this_formlayout, e=True,
                            attachForm=[
                                (this_subtext_field, 'left', 10),
                                (this_subtext_field, 'right', 10),
                                (this_subtext_field, 'bottom', 50),
                            ])

        cmds.formLayout(this_formlayout, e=True,
                        attachForm=[
                            (this_scroll_field, 'top', scroll_top_value),
                            (this_scroll_field, 'left', 10),
                            (this_scroll_field, 'right', 10),
                            (this_scroll_field, 'bottom', scroll_bottom_value)
                        ])

    else:

        if this_text_field:

            cmds.formLayout(this_formlayout, e=True,
                            attachForm=[
                                (this_text_field, 'top', 10),
                                (this_text_field, 'left', 10),
                                (this_text_field, 'right', 10),
                                (this_text_field, 'bottom', 50)
                            ])

    # ------------------
    # ボタンアタッチ

    if cancel_button:

        cmds.formLayout(this_formlayout, e=True,
                        attachForm=[
                            (default_button, 'left', 20),
                            (default_button, 'bottom', 15),
                            (cancel_button, 'right', 20),
                            (cancel_button, 'bottom', 15)
                        ])

    else:

        cmds.formLayout(this_formlayout, e=True,
                        attachForm=[
                            (default_button, 'left', 20),
                            (default_button, 'right', 20),
                            (default_button, 'bottom', 15),
                        ])
