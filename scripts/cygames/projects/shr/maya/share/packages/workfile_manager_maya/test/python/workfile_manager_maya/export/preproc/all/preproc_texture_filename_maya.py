# -*- coding: utf-8 -*-
from __future__ import annotations
from workfile_manager.plugin_utils import Application
from workfile_manager.export.preproc.preproc_texture_filename import PluginBase

class Plugin(PluginBase):
    def application(self) -> Application:
        return Application.Maya
    
    def apps_executable_on(self) -> list[Application]:
        return [Application.Maya]
    
    def get_texture_node_names_and_paths(self) -> list[tuple[str, str]]:
        from workfile_manager_maya import assetutils_maya
        dccutils = assetutils_maya.MayaUtils.get_instance()
        return dccutils.get_texture_node_names_and_paths()
    