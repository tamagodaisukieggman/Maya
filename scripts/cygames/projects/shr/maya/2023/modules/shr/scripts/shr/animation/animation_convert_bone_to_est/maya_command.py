import maya.cmds as cmds

def exec_get_filepath_dialog():
    path = cmds.fileDialog2(fm=1,ds=1)
    return path