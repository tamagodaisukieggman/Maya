#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# CySceneOpener.py
#

u"""
    BEGIN__CYGAMES_MENU
    label=CySceneOpener
    command=main()
    order=3000
    author=taketani_ken
    version=2.1.1
    END__CYGAMES_MENU
"""

import os
import sys
import subprocess
import maya.cmds as cmds

try:
    from importlib import reload
except Exception:
    pass


def get_pyside_for_maya2013(overwrite=False):
    '''
    Maya2013にの場合はPySideをサーバからコピー
    '''
    version = cmds.about(v=True)
    if version.find("2013") > -1:
        destination_dir = os.path.normpath(os.environ.get("MAYA_APP_DIR"))+"\\PySide"
        sys.path.append(destination_dir)
        if os.path.exists(destination_dir + "\\PySide") == False or overwrite:
            source_dir = "\\\\cygames-fas01\\100_projects\\056_designer_tools\\99_other\\tools\\cygame_designer_tools\\plugin\\PySide"
            cmd = "xcopy " + source_dir + " " + destination_dir + " /E/Y/I"
            subprocess.check_call(cmd)


def main():
    '''
    アプリケーションの実行
    '''
    get_pyside_for_maya2013()

    try:
        import Qt_CySceneOpener
        reload(Qt_CySceneOpener)
        Qt_CySceneOpener.main()
    except ImportError:
        get_pyside_for_maya2013(True)
        Qt_CySceneOpener.main()
