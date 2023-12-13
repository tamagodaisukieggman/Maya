import maya.cmds as mc
import cyllistaClipConfigSetup as cs
import mtk.utils.wrapper as wrapper
import os

def main():

    try:
        currentPath = wrapper.getCurrentSceneFilePath() #currentPath = mc.file(q=True, sn=True)
        currentDir = os.path.dirname(currentPath)
    except:
        currentDir = 'Z:\\mtk\\work\\resources\\animations'

    files = mc.fileDialog2(startingDirectory=currentDir, fileMode=4, okCaption="Select", fileFilter="Maya Files (*.ma *.mb)")

    if files is None:
        print("Had Cancel")
    else:
        cs.setupDefaultConfigs(files)
