import maya.cmds as cmds

OFFSET_TRANS_NAME = "offSet"


class PropOffsetManager:
    def __init__(self, asset_type):
        self.asset_type = asset_type

    def create_offset(self):
        """選択したジョイントの位置を保持するオフセットの作成
        Args:
            asset_type(str): アセットの種類
        """
        selected_joint = self._get_selected_joint()
        root_joint = self._get_selected_root_joint()
        if root_joint:
            self.move_joint_transform_to_new_group(selected_joint, self.asset_type)
        else:
            cmds.warning("有効なjointを選択して実行してください")
        cmds.select(selected_joint, r=True)

    def reset_transform(self):
        """選択したジョイントの位置をオフセットで保持している位置にセット"""
        selected_joint = self._get_selected_joint()
        root_joint = self._get_selected_root_joint()
        if root_joint:
            self.return_joint_to_original_transform(selected_joint, self.asset_type)
        else:
            cmds.warning("有効なjointを選択して実行してください")

    @classmethod
    def _get_selected_joint(cls) -> str:
        """選択したジョイントの最初に選択したもののみ返す

        Raises:
            ValueError: _description_

        Returns:
            str: 選択したジョイント名
        """
        selected_joints = cmds.ls(sl=True, type="joint")
        if selected_joints:
            return selected_joints[0]
        else:
            raise ValueError("対象となる単一の骨を選択して実行してください。")

    @classmethod
    def _get_selected_root_joint(cls) -> str:
        """選択したジョイントのルートとなる骨を返す"""
        selected_joints = cmds.ls(sl=True, type="joint")
        if selected_joints:
            root_joint = cls.get_root_joint(selected_joints)
            return root_joint

    @classmethod
    def get_current_offset_name(cls, joint: str, asset_type: str) -> str:
        """ジョイントと対になるオフセットノードの取得

        Args:
            joint (str): 対象となるoffsetのtarget joint

        Returns:
            str: _description_
        """
        joint_short_name = cls.get_short_name(joint)
        root_group = cls.get_root_transform(joint)
        offset_trans = (
            f"{root_group}|{asset_type}_{OFFSET_TRANS_NAME}_{joint_short_name}"
        )
        print(offset_trans)
        return offset_trans

    @staticmethod
    def get_short_name(path: str):
        return path.split("|")[-1]

    @classmethod
    def move_joint_transform_to_new_group(cls, joint: str, asset_type: str) -> str:
        """
        Args:
            joint(str): 対象のジョイント名
        Returns:
            str: 新規に作成した空のトランスフォームの名前
        """

        root_group = cls.get_root_transform(joint)

        if not root_group:
            cmds.warning(f"{joint}の親階層が存在しません。階層ルールと現在のデータに誤りがあります。")
            return

        # 新規に空のtransformを作成
        offset_trans = cls.get_current_offset_name(joint, asset_type)
        if cmds.objExists(offset_trans):
            cmds.delete(offset_trans)

        offset_trans_short_name = cls.get_short_name(offset_trans)
        new_transform = cmds.group(
            em=True, name=offset_trans_short_name, parent=root_group
        )

        # ジョイントのワールド座標を取得
        joint_world_translate = cmds.xform(joint, q=True, t=True, ws=True)
        joint_world_rotate = cmds.xform(joint, q=True, ro=True, ws=True)
        joint_world_scale = cmds.xform(joint, q=True, s=True, ws=True)

        # 新規に作成したtransformにジョイントのワールド座標を適応
        cmds.xform(
            new_transform,
            t=joint_world_translate,
            ro=joint_world_rotate,
            s=joint_world_scale,
            ws=True,
        )

        # ジョイントを原点に移動
        cmds.xform(joint, t=(0, 0, 0), ro=(0, 0, 0), s=(1, 1, 1))

        return new_transform

    @classmethod
    def return_joint_to_original_transform(cls, joint: str, asset_type: str) -> str:
        """
        Args:
            joint(str): 対象のjointの名前
            transform(str): 対象のjointを元の座標に戻すためのtransformの名前
        Return:
            str: 入力として与えられたjointの名前
        """
        offset_trans = PropOffsetManager.get_current_offset_name(joint, asset_type)
        # transformのワールド座標を取得
        transform_world_translate = cmds.xform(offset_trans, q=True, t=True, ws=True)
        transform_world_rotate = cmds.xform(offset_trans, q=True, ro=True, ws=True)
        transform_world_scale = cmds.xform(offset_trans, q=True, s=True, ws=True)
        # ジョイントへtransformのワールド座標を適応
        cmds.xform(
            joint,
            t=transform_world_translate,
            ro=transform_world_rotate,
            s=transform_world_scale,
            ws=True,
        )

    @staticmethod
    def get_root_joint(joint: str) -> str:
        """
        選択したジョイントのルートジョイントを取得します。
        Args:
            selected_joint (str): ルートを調査したいジョイントの名前
        Returns:
            str: 選択されたジョイントのルートジョイントの名前
        """
        while True:
            parent_joint = cmds.listRelatives(
                joint, parent=True, type="joint", fullPath=True
            )
            if not parent_joint:
                return joint
            joint = parent_joint[0]

    @staticmethod
    def get_root_transform(node: str) -> str:
        """
        選択されたノードのルートを返します。
        Args:
            node (str): ルートを検索したいノードの名前
        Returns:
            str: 選択されたノードのルートの名前
        """
        while True:
            parent_node = cmds.listRelatives(node, parent=True, fullPath=True)
            if not parent_node:
                return node
            node = parent_node[0]
