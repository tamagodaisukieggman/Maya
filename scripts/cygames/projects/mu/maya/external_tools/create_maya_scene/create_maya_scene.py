# -*- coding: utf-8 -*-

import os
import sys
import maya.standalone
import maya.cmds as cmds

try:
    sys.path.append("Z:/cyllista/tools/maya/modules/cyllista/scripts/")
    import cyllista.config_node as config_node
except Exception:
    print('can\'t import "config_node"')
    exit(1)


class CreateMayaScene:
    """Maya scene を作成するクラス"""

    def __init__(self):
        """コンストラクタ"""
        self.is_init = False

    def create_file(self, filename):
        """グループノードを作成してファイル作成"""

        # ファイルが存在していたら終了
        if os.path.exists(filename):
            print('file is exists ! : ' + filename)
            return

        if not self.is_init:
            # Mayaのイニシャライズは一回だけ
            maya.standalone.initialize(name='python')
            self.is_init = True

        cmds.file(f=True, new=True)

        # グループノードを作成
        root_gr = os.path.basename(filename).split('.')[0]
        if root_gr.find('mdl_') != 0:
            root_gr = 'mdl_' + root_gr

        cmds.group(name=root_gr, empty=True, world=True)
        cmds.group(name='model', empty=True, parent=root_gr)
        cmds.joint(name='jnt_0000_skl_root')
        cmds.parent('jnt_0000_skl_root', root_gr)
        cmds.group(name='lod1', empty=True, parent=root_gr)
        cmds.group(name='lod2', empty=True, parent=root_gr)
        cmds.group(name='collision', empty=True, parent=root_gr)

        # config node 設定
        config = {"cyExportGfx": True, "cyExportPhy": True}
        config_node.prepare_default_config()
        config_node.update_config(config)

        # ディレクトリが存在しない場合は作成
        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            os.makedirs(path)

        # ファイル書き出し
        cmds.file(rename=filename)
        savename = cmds.file(save=True, type='mayaAscii')

        print('create file : ' + savename)


def main(args):
    create_maya = CreateMayaScene()

    for arg in args:
        create_maya.create_file(arg + '.ma')


if __name__ == "__main__":
    main(sys.argv[1:])
