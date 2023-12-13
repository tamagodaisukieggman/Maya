# -*- coding: utf-8 -*-

import os
import sys
import maya.standalone
import maya.cmds as cmds

TEAM_TYPES = ["characters", "environments"]


class CreateMayaScene:
    """Maya scene を作成するクラス"""

    def __init__(self):
        """コンストラクタ"""
        self.is_init = False

    def _create_lod_grp(self, used_transform_node: bool, root_gr: str) -> str:
        """lodgroupの作成

        Args:
            tf_node(str):
            root_gr (str): _description_

        Returns:
            str: _description_
        """
        if used_transform_node:
            lod_gr = cmds.createNode("transform", name="mesh", parent=root_gr)
            return lod_gr
        else:
            # キャラ、背景の初期構成構築
            lod_gr = cmds.createNode("lodGroup", name="mesh", parent=root_gr)
            camera = cmds.ls("perspShape", type="camera")[0]

            # cameraとのコネクションをしないとshowが効かない
            cmds.connectAttr(
                "{}.worldMatrix".format(camera), "{}.cameraMatrix".format(lod_gr)
            )
            cmds.connectAttr(
                "{}.focalLength".format(camera), "{}.focalLength".format(lod_gr)
            )
            return lod_gr

    def _create_lod_transform(self, lod_gr):
        max_lod_num = 0
        for i in range(max_lod_num + 1):
            _current_lod = cmds.createNode("transform", n="lod{}".format(i))

            # createNodeのparentだとlodgroup側でlodとして認識されないためparentを挟む
            cmds.parent(_current_lod, lod_gr)

            # lod groupの場合のみ、displayLevelの設定
            if cmds.objectType(lod_gr) == "lodGroup":
                cmds.setAttr("{0}.displayLevel[{1}]".format(lod_gr, i), 1)

    def create_file(self, filename):
        """グループノードを作成してファイル作成"""

        # ファイルが存在していたら終了
        if os.path.exists(filename):
            print("file is exists ! : " + filename)
            return

        dir = os.path.dirname(filename)
        current_team_type = ""
        for team_type in TEAM_TYPES:
            if team_type in dir:
                current_team_type = team_type

        if not self.is_init:
            # Mayaのイニシャライズは一回だけ
            maya.standalone.initialize(name="python")
            self.is_init = True

        cmds.file(f=True, new=True)

        # 背景でもキャラでもない場合は一旦mayasceneの保存のみ実行
        if current_team_type == "":
            cmds.file(rename=filename)
            cmds.file(save=True, type="mayaBinary")
            return

        root_gr = cmds.createNode(
            "transform", n=os.path.basename(filename).split(".")[0]
        )

        if current_team_type == "characters":
            is_transform = True
            lod_gr = self._create_lod_grp(is_transform, root_gr)
            self._create_lod_transform(lod_gr)

        # 背景にだけcollisionグループの作成
        if current_team_type == "environments":
            is_transform = False
            lod_gr = self._create_lod_grp(is_transform, root_gr)
            self._create_lod_transform(lod_gr)
            cmds.group(name="collision", empty=True, parent=root_gr)

        # ディレクトリが存在しない場合は作成
        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            os.makedirs(path)

        # ファイル書き出し
        cmds.file(rename=filename)
        savename = cmds.file(save=True, type="mayaBinary")

        print("create file : " + savename)


def main(args):
    create_maya = CreateMayaScene()
    print(args)

    for arg in args:
        create_maya.create_file(arg + ".mb")


if __name__ == "__main__":
    main(sys.argv[1:])
