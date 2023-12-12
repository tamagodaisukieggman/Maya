import os
import sys
import glob
from functools import partial

from maya import cmds
from maya import mel
import maya.api.OpenMaya as om

mel.eval("eST3start")
import eST3

class bindpose_check():
    def __init__(self):
        self.shelf_path = r'C:\cygames\shrdev\shr_art\tool_resources\eST\user\projects\shenron\assets\other\shelf'
        self.eST_shelf_path = r'shelf|projects/shenron/other'
        # GET FILE PATH
        self.filepath = None
        self.dirname = None
        self.basename = None
        self.name = None
        self.getFolder(cmds.file(q=True, sn=True))

        self.bindPosePath = None
        self.defPosePath = None

    def getFolder(self, filepath):
        self.filepath = filepath
        self.dirname = os.path.dirname(self.filepath)
        self.basename = os.path.basename(self.filepath)
        self.name = self.basename.split('.')[0]
        self.charaTag = self.name.split('_')[0]
        self.ERROR = []

    def go_bindpose(self):
        shelf_path = os.path.join(self.shelf_path, self.charaTag, "*.epose")
        posefiles = glob.glob(shelf_path)
        print(shelf_path)
        if posefiles:
            posefiles = [f for f in posefiles if os.path.isfile(f)]
            for o in posefiles:
                filename = os.path.basename(o)
                dirname = os.path.dirname(o).split("\\")[-1]
                estAssetPath = self.eST_shelf_path + "/" + dirname + "/" + filename
                asset = eST3.asAsset(estAssetPath)
                label = asset.getProperty('label')
                if "bindPose" in label:
                    self.bindPosePath = estAssetPath
                    eST3.rCmds.AssetMethod(
                        assets=[eST3.asAsset(estAssetPath, type='eSTpose')],
                        method='apply',
                        option={'echoCode': True, 'restoreByChooser': True, 'echo': False, 'echoMessage': True,
                                'applyToSelection': False, 'setKeyframes': False, 'noKeyframeOnReset': True})
                elif "defaultPose" in label:
                    self.defPosePath = estAssetPath
            return True
        else:
            return False


    def main(self):
        bindpose = cmds.ls("bindPose*")  # シーン内のバインドポーズを取得
        print("bindPoseの再登録を行います。")

        # ここでバインドポーズに戻す処理
        if self.go_bindpose():
            cmds.delete(bindpose)

            skincluster = cmds.ls(type="skinCluster")
            for o in skincluster:
                influences = cmds.skinCluster(o, query=True, influence=True)
                shape = cmds.skinCluster(o, query=True, geometry=True)[0]
                cmds.skinCluster(o, e=True, unbindKeepHistory=True)

                cmds.skinCluster(influences, shape, toSelectedBones=True)
                cmds.setAttr(o + '.envelope', 1)

            eST3.rCmds.AssetMethod(
                assets=[eST3.asAsset(self.defPosePath, type='eSTpose')],
                method='apply',
                option={'echoCode': True, 'restoreByChooser': True, 'echo': False, 'echoMessage': True,
                        'applyToSelection': False, 'setKeyframes': False, 'noKeyframeOnReset': True})
            cmds.select(clear = True)
        else:
            print("Poseの登録がありません")


def main():
    bpc = bindpose_check()
    bpc.main()

# デバック用
if __name__ == '__main__':
    main()
