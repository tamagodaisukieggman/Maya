# -*- coding: utf-8 -*-
"""アニメーション追加機能
"""
from __future__ import annotations

import os
import typing as tp

from maya import cmds
from shr.cutscene.sequencer.lib import reference

from ..config import ActorConfigData
from ..maya_reference_controller import MayaReferenceController
from ..screen_writer import ObjectType, ScreenWriterConnector


class InsertAnimator(object):
    def __init__(self, actor_config: ActorConfigData, screen_writer) -> None:
        self.actor_config = actor_config
        self.screen_writer = screen_writer

        self.screen_writer_connector = ScreenWriterConnector(self.screen_writer)

    def connect_animation(self, clip_name, path):
        ref_name = MayaReferenceController().import_(clip_name, path)
        ref_node = cmds.referenceQuery(ref_name, referenceNode=True)
        ref_namespace = cmds.referenceQuery(ref_name, namespace=True, shortName=True)

        index = self.connect_to_input(ref_namespace)

        # Animation import時に全RootNodeを非表示にする
        self._hide_all_root_node(ref_node)

        return ref_name, index

    def _hide_all_root_node(self, ref_node):
        # auto_keyをOffにしないとHideがキーフレームとしてカウントされる
        is_auto_key = cmds.autoKeyframe(query=True, state=True)

        cmds.autoKeyframe(edit=True, state=False)
        nodes = reference.root_node(ref_node)
        cmds.hide(nodes)

        cmds.autoKeyframe(edit=True, state=is_auto_key)

    def connect_to_input(self, name_space: str):
        self._check_node()

        clip_index = self.screen_writer_connector.get_can_input_index()

        self._bind_transform(name_space, clip_index)
        self._bind_extra(name_space, clip_index)
        return clip_index

    def _check_node(self, comapre_node="ScreenWriter"):
        if cmds.nodeType(self.screen_writer) != comapre_node:
            raise ValueError("invalid screen writer")

    def _bind_transform(self, name_space: str, clip_index: int):
        binding_node_list = self.screen_writer_connector.create_binding_list(name_space, self.actor_config.binding_data)

        for i, binding_node in enumerate(binding_node_list):
            self.screen_writer_connector.connect_input(ObjectType.Matrix, play_data_index=clip_index, index=i, target=binding_node)

    def _bind_extra(self, name_space: str, clip_index: int):
        extra_attr_list = self.actor_config.binding_data.extra_attrs

        binding_node_list = self.screen_writer_connector.create_binding_list(name_space, self.actor_config.binding_data)

        for i, binding_node in enumerate(binding_node_list):
            for j, extra_attr in enumerate(extra_attr_list):
                self.screen_writer_connector.connect_input(ObjectType.Extra, play_data_index=clip_index, index=i + j, target=binding_node, name=extra_attr)

    def compare_actor_and_motion(self, actor_ref, motion_ref):
        """アクターとモーションと比較する

        Args:
            actor_ref (str)): アクターのReference Path
            motion_ref (str): モーションのReference Path
            track (MotionTrack): Track情報

        Returns:
            bool: 一致するかどうか
        """
        actor_name_space = cmds.referenceQuery(actor_ref, namespace=True, shortName=True)
        motion_name_space = cmds.referenceQuery(motion_ref, namespace=True, shortName=True)

        actor_binding_list = self.screen_writer_connector.create_binding_list(actor_name_space, self.actor_config.binding_data)
        motion_binding_list = self.screen_writer_connector.create_binding_list(motion_name_space, self.actor_config.binding_data)

        # namespaceの除去
        actor_binding_list = [_.rsplit(":")[-1] for _ in actor_binding_list]
        motion_binding_list = [_.rsplit(":")[-1] for _ in motion_binding_list]

        compare_data = set(actor_binding_list) - set(motion_binding_list)

        if (len(compare_data) == 0):
            return True
        else:
            return False


def open_dialog(start_dir) -> str:
    return cmds.fileDialog2(startingDirectory=start_dir, fileMode=1)


def collect_files(dir_path):
    list_data = os.listdir(dir_path)
    list_data = [os.path.join(dir_path, _) for _ in list_data]

    file_list = [f for f in list_data if os.path.isfile(f)]
    return file_list


def collect_file_basenames(file_list):
    base_name_list = [os.path.splitext(os.path.basename(_))[0] for _ in file_list]
    return base_name_list
