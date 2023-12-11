# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------
#   SaveGeometry
#-------------------------------------------------------------------------------------------

import os
import subprocess
import shutil
import maya.cmds as cmds

#======================================================================
# Maya2013にの場合はPySideをサーバからコピー
#======================================================================
def get_pyside_for_maya2013(overwrite=False):
    version = cmds.about(v=True)
    if version.find("2013") > -1:
        destination_dir = os.path.normpath(cmds.internalVar(userScriptDir=True))
        if os.path.exists(destination_dir + "\\PySide") == False or overwrite:
            source_dir = "\\\\cygames-fas01\\100_projects\\056_designer_tools\\99_other\\tools\\cygame_designer_tools\\plugin\\PySide"
            cmd = "xcopy " + source_dir + " " + destination_dir + " /E/Y/I"
            subprocess.check_call(cmd)

#======================================================================
# アプリケーションの実行
#======================================================================
def main():
    get_pyside_for_maya2013()
    try:
        import CyAnimationCopy
        reload(CyAnimationCopy)
        CyAnimationCopy.main()
    except ImportError as e:
        get_pyside_for_maya2013(True)
        import CyAnimationCopy
        reload(CyAnimationCopy)
        CyAnimationCopy.main()
