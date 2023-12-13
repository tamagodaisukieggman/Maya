from workfile_manager.plugin_utils import ImportPostprocBase, PluginType, Application
from cylibassetdbutils import assetdbutils

db = assetdbutils.DB.get_instance()

class Plugin(ImportPostprocBase):
    def application(self):
        return Application.UnrealEngine

    def getlabel(self):
        return 'Set Flip Green Channel Flag'

    def execute(self, args):
        if 'imported_object' in args:
            imported_object = args['imported_object']
        else:
            return False

        import unreal
        alib = unreal.EditorAssetLibrary()

        for obj_path in imported_object:
            adata = alib.find_asset_data(obj_path)
            if adata.asset_class != 'Texture2D':
                continue
            if "_nrm" in str(adata.asset_name):
                texture = adata.get_asset()
                texture.set_editor_property("flip_green_channel",1) 

    def apps_executable_on(self):
        return [Application.UnrealEngine]

    def is_asset_eligible(self, asset):
        if asset.assetgroup == 'character':
            return True
        else:
            return False

