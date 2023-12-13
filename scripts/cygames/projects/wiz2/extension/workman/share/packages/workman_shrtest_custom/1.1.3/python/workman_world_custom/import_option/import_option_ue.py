# -*- coding: utf-8 -*-

from workfile_manager.plugin_utils import ImportOptionBase, PluginType, Application

class Plugin(ImportOptionBase):
    def application(self):
        return Application.UnrealEngine

    def apps_executable_on(self):
        return [Application.UnrealEngine]

    def is_asset_eligible(self, asset):
        return True

    def get_options(self, asset):
        from cylibassetdbutils import assetdbutils
        db = assetdbutils.DB.get_instance()

        tags = db.get_assigned_tags(asset)
        
        for t in tags:
            if t['tag_type'] == 'environment-type' and t['name'] == 'col':
                opt = {'import_materials':False}
                return opt

        return None

