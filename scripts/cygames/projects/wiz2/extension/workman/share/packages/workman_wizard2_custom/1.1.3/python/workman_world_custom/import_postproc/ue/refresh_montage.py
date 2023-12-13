from __future__ import print_function
from workfile_manager.plugin_utils import ImportPostprocBase, Application
from cylibassetdbutils import assetdbutils

db = assetdbutils.DB.get_instance()

class Plugin(ImportPostprocBase):
    def application(self):
        return Application.UnrealEngine

    def getlabel(self):
        return 'Refresh montage framerange'

    def execute(self, args):
        if 'imported_object' in args:
            imported_object = args['imported_object']
            print('>> imported_object: ', imported_object)
        else:
            return False
            
        import unreal
        alib = unreal.EditorAssetLibrary()

        for obj_path in imported_object:
            print('> obj_path: ' + obj_path)
            adata = alib.find_asset_data(obj_path)
            print('> asset_class: ' + str(adata.asset_class))
            if adata.asset_class != 'AnimSequence':
                continue
            refs = unreal.WorkMan.get_referencing_objects(obj_path)
            print('refs: ', refs)
            for ref in refs:
                print('> ref: ' + ref)
                refdata = alib.find_asset_data(ref)
                if refdata.asset_class != 'AnimMontage':
                    continue
                ref = '%s.%s' % (ref, ref[ref.rindex('/')+1:])
                print('> updating montage: ' + ref)
                unreal.PythonCallableLibrary.update_montage_range(ref)

        return True

    def apps_executable_on(self):
        return [Application.UnrealEngine]

    def is_asset_eligible(self, asset):
        return True
