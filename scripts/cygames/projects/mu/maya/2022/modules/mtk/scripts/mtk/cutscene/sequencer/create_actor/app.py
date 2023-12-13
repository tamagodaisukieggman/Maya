# -*- coding: utf-8 -*-
from __future__ import annotations

from maya import cmds

# from ..config_collector.app import ActorConfigData
from ..config import ActorConfigData
from ..screen_writer import ObjectType, ScreenWriterConnector


class BaseActorCreator(object):
    def __init__(self, actor_config: ActorConfigData, screen_writer) -> None:
        self.actor_config = actor_config
        self.screen_writer = screen_writer
        self.screen_writer_connector = ScreenWriterConnector(self.screen_writer)

    def create_actor(self, actor_name: str) -> str:
        actor_path = self.actor_config.actor_import_path
        if cmds.namespace(exists=actor_name):
            raise ValueError("既に存在するNamespace")

        ref_node = cmds.file(actor_path, reference=True, mergeNamespacesOnClash=False, namespace=actor_name)
        ref_node = cmds.referenceQuery(ref_node, filename=True, withoutCopyNumber=True)

        bind_data = self.screen_writer_connector.create_binding_list(actor_name, self.actor_config.binding_data)
        self._connect_to_output(bind_data)

        return ref_node

    def _connect_to_output(self, binding_node_list) -> None:
        if cmds.nodeType(self.screen_writer) != "ScreenWriter":
            raise ValueError("invalid screen writer")

        self._bind_transform(binding_node_list)
        self._bind_extra(binding_node_list)

    def _bind_transform(self, binding_node_list):
        for i, binding_node in enumerate(binding_node_list):
            self.screen_writer_connector.connect_output(ObjectType.Position, index=i, target=binding_node)
            self.screen_writer_connector.connect_output(ObjectType.Rotation, index=i, target=binding_node)

    def _bind_extra(self, binding_node_list):
        extra_attr_list = self.actor_config.binding_data.extra_attrs
        connector = ScreenWriterConnector(self.screen_writer)
        for i, binding_node in enumerate(binding_node_list):
            for j, extra_attr in enumerate(extra_attr_list):
                connector.connect_output(ObjectType.Extra, index=i + j, target=binding_node, name=extra_attr)


class ActorCreator(BaseActorCreator):
    def __init__(self, actor_config: ActorConfigData, screen_writer) -> None:
        super().__init__(actor_config, screen_writer)

    def create_actor(self, actor_name: str) -> str:
        return super().create_actor(actor_name)
