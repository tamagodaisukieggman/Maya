# -*- coding: utf-8 -*-

import re
import maya.cmds as cmds

# このimportにしないとCheckTaskBaseの__subclasses__に登録されない
from ....common.maya_checker.task import CheckTaskBase
from ....common.maya_checker.scene_data import MayaSceneDataBase
from ....common.maya_checker.data import ErrorType
from ....common.maya_checker_gui.controller import CheckerMainWindow


class Wiz2EnvNodeHierarchy(CheckTaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checker_info.label_name = 'ノード構成（ツリー構成）'

    def exec_task_method(self):
        non_direct_mesh_children = []
        mesh_transforms = []
        # RootNodeData
        for root in self.maya_scene_data.root_nodes:
            mesh_transforms.extend(root.get_all_mesh_transform())
        if not mesh_transforms:
            self.set_error_data(
                'env_nord_hierarchy_no_mesh',
                None,
                'メッシュがありません',
                is_reset_debug_data=False,
            )
            self.set_error_type(ErrorType.NOCHECKED)
            return
        for mesh in mesh_transforms:
            root = self.get_root_node(mesh)
            parents = cmds.listRelatives(mesh, parent=True, fullPath=True)
            if parents and parents[0] != root:
                non_direct_mesh_children.append(mesh)
        if not non_direct_mesh_children:
            self.set_error_type(ErrorType.NOERROR)
        if non_direct_mesh_children:
            self.set_error_data(
                'env_non_direct_mesh_children',
                non_direct_mesh_children,
                'root直下がメッシュではありません',
                is_reset_debug_data=False,
            )

    def exec_fix_method(self):
        """メッシュTransformをRoot直下にする"""
        try:
            if (
                'env_non_direct_mesh_children'
                in self.debug_data.error_target_info.keys()
            ):
                debug_targets = self.get_debug_target_objects(
                    'env_non_direct_mesh_children'
                )
                debug_targets = list(set(debug_targets))
                for target in debug_targets:
                    root = self.get_root_node(target)
                    if root:
                        cmds.parent(target, root)
                # メッシュの階層が代わり他のdebug_dataのオブジェクトパスが
                # 存在しなくなる可能性があるためリセット
                try:
                    CheckerMainWindow._instance.initialize()
                except Exception:
                    pass
        except Exception:
            cmds.error('Error: ノード構成（ツリー構成） 修正')

    def get_root_node(self, node):
        if not node:
            return
        parents = cmds.listRelatives(node, parent=True, fullPath=True)
        if not parents:
            return node
        else:
            for p in parents:
                return self.get_root_node(p)
