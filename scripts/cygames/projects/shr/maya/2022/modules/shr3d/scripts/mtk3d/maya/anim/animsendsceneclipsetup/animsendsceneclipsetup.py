import maya.cmds as mc
import cyllistaClipConfigSetup as cs
import os

def main():
    currentPath = mc.file(q=True, sn=True)
    currentDir = os.path.dirname(currentPath)
    files = mc.fileDialog2(startingDirectory=currentDir, fileMode=4, okCaption="Select", fileFilter="Maya Files (*.ma *.mb)")

    if files is None:
        print("Had Cancel")
    else:
        cs.setupDefaultConfigs(files)
