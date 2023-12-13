# -*- coding: utf-8 -*-
u"""Anim Store

..
    BEGIN__CYGAMES_MENU
    label=Anim Copy && Paste ...
    command=anim_copy_paste()
    order=2000
    END__CYGAMES_MENU

    END__CYGAMES_DESCRIPTION

"""
# TODO: Maya2022対応時に無効。tatoolに置き換える
# from mtku.maya.mtklog import MtkLog

from .ui import animcopypaste

# logger = MtkLog(__name__)


def anim_copy_paste():
    u"""main関数"""
    # logger.usage()

    ui = animcopypaste.AnimCopyPaste()
    ui.show()
