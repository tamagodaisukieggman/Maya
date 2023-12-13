from workfile_manager.plugin_utils import ImportPostprocBase, PluginType, Application
from cylibassetdbutils import assetdbutils

db = assetdbutils.DB.get_instance()

class Plugin(ImportPostprocBase):
    def application(self):
        return Application.UnrealEngine

    def getlabel(self):
        return 'Refresh collision in referencing objects'

    def execute(self, args):
        if 'imported_object' in args:
            imported_object = args['imported_object']
            print(('>> imported_object: ', imported_object))
        else:
            return False
            
        asset = args['asset']
        tags = db.get_assigned_tags(asset)
        for t in tags:
            if t['tag_type'] == 'environment-type' and t['name'] == 'col':
                break
        else:
            return False
        print('This is collision asset.')

        import unreal
        alib = unreal.EditorAssetLibrary()

        for obj_path in imported_object:
            adata = alib.find_asset_data(obj_path)
            if adata.asset_class != 'StaticMesh':
                continue
            refs = unreal.WorkMan.get_referencing_objects(obj_path)
            for ref in refs:
                refdata = alib.find_asset_data(ref)
                if refdata.asset_class != 'StaticMesh':
                    continue
                refmesh = refdata.get_asset()
                parm = 'complex_collision_mesh'
                if refmesh.get_editor_property(parm) == adata.get_asset():
                    # refresh
                    print(('>> Refreshing staticMesh: ', ref))
                    refmesh.set_editor_property(parm, None)
                    refmesh.set_editor_property(parm, adata.get_asset())
                    print('>> Refresh done.')

        return True

    def apps_executable_on(self):
        return [Application.UnrealEngine]

    def is_asset_eligible(self, asset):
        return True
