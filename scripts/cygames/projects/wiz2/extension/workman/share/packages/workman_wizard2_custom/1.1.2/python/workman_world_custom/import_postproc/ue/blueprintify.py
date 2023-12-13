# -*- coding: utf-8 -*-
from __future__ import print_function

from cylibassetdbutils import assetdbutils
from workfile_manager.plugin_utils import ImportPostprocBase, PluginType, Application
from workfile_manager import p4utils
from workfile_manager.ui import uiutils, ui_table_engine

from Qt import QtWidgets

try:
    from workfile_manager_ue import assetutils_ue, cmds
except:
    pass

try:
    import unreal
    alib = unreal.EditorAssetLibrary()
except:
    pass

import os


db = assetdbutils.DB.get_instance()
p4u = p4utils.P4Utils.get_instance()

def check_existence(dst):
    if alib.does_asset_exist(dst):
        print ('BP already exists: ', dst)
        bp_filename = cmds.filename_from_objectpath(dst)
        if os.path.exists(bp_filename):
            print ('checking out bp...')
            p4u.p4_run_xxx('edit', bp_filename)
        return True

    else:
        return False


def iterate_meshes_on(key, node):
    if 'node_type' in node and node['node_type'] == 'mesh':
        yield key, node
    
    for k in node.keys():
        if type(node[k]) is dict:
            for _k, _node in iterate_meshes_on(k, node[k]):
                yield _k, _node
        

def _find_first_visible_mesh(obj_paths, jsonfile):
    import json
    try:
        with open(jsonfile, 'r') as fhd:
            dct = json.load(fhd)
    except:
        return None

    maya_nodename_to_objpath = {}
    for obj in obj_paths:
        adata = alib.find_asset_data(obj)
        uasset = adata.get_asset()
        all_metadata = alib.get_metadata_tag_values(uasset)
        mkey = 'FBX.workman_maya_nodename'
        for tag_name, value in all_metadata.iteritems():
            tag_name = str(tag_name)
            if tag_name == mkey:
                value = str(value)
                maya_nodename_to_objpath[value] = obj
                break

    for mname, mdict in iterate_meshes_on(None, dct):
        if 'visibility' in mdict and mdict['visibility'] and 'parent' in mdict and mdict['parent']:
            if mname in maya_nodename_to_objpath:
                return maya_nodename_to_objpath[mname]

    return None

def find_first_visible_mesh(obj_paths, jsonfile):
    import json
    try:
        with open(jsonfile, 'r') as fhd:
            dct = json.load(fhd)
    except:
        return None

    import re
    for obj in obj_paths:
        leaf = obj[obj.rindex('/')+1:]
        m = re.search('^([^_]+_){5}(.*)', leaf)
        if m:
            nodename = m.group(2)
        else:
            nodename = 'all'
        for mname, mdict in iterate_meshes_on(None, dct):
            if 'visibility' in mdict and mdict['visibility'] and 'parent' in mdict and mdict['parent']:
                if mname == nodename:
                    return obj
    return None

    


def get_destination(obj_path, args, tags, asset):
    if obj_path in args['imported_names']:
        asset._asset_name = str(args['imported_names'][obj_path])

    outconfig = asset.check_output_config(tags=tags, additional_fields={'node':'Blueprint'})
    
    if outconfig is None:
        return None

    dst = asset.evaluate_output(outconfig, proc_token=True, proc_tag=True, tags=tags)
    return dst


class BlueprintSettings(QtWidgets.QWidget):
    def __init__(self):
        super(BlueprintSettings, self).__init__()
        vbox = QtWidgets.QVBoxLayout(self)
        self.cb_dither = QtWidgets.QCheckBox(u'ディザーを有効にする')
        vbox.addWidget(self.cb_dither)

    def get_params(self):
        res = {'dither':self.cb_dither.isChecked()}
        return res

class Plugin(ImportPostprocBase):
    def application(self):
        return Application.UnrealEngine

    def getlabel(self):
        return 'Blueprintify imported static meshes.'

    def _is_asset_to_blueprintify(self, adata):
        if adata.asset_class != 'StaticMesh':
            return False
        return True
        

    def execute(self, args):
        if not hasattr(unreal, 'PythonCallableLibrary') or not hasattr(unreal.PythonCallableLibrary, 'create_blueprint'):
            return False

        if 'imported_object' in args:
            imported_object = args['imported_object']
            print ('>> imported_object: ', imported_object)
        else:
            return False

        _asset = args['asset']
        if hasattr(_asset, '_is_skeletal_mesh') and getattr(_asset, '_is_skeletal_mesh'):
            return False

        tags = db.get_assigned_tags(_asset)
        tags = [(x['tag_type'], x['name']) for x in tags]

        if 'environment-type' in [x[0] for x in tags]:
            idx = [x[0] for x in tags].index('environment-type')
            if tags[idx][1] == 'col':
                return False

        from workfile_manager_ue import asset_engine
        asset = asset_engine.EngineMetaAssetUE()
        for k in _asset.get_dict():
            setattr(asset, k, getattr(_asset, k))
        
        #       
        buf = db.get_engine_assets(asset=asset)
        if len(buf) == 0:
            print('Engine asset not found.')
            return False

        from workman_world_custom.export_postproc.maya.model import export_collision_settings
        jsonfile = export_collision_settings.get_json_path_from_masterfile(args['filename'])
        print('>>>>>>>>>>>>>>>>> jsonfile: ', jsonfile)
        if not os.path.exists(jsonfile):
            # Support for compatibility with old specifications.
            src_share = buf[0]['source']
            refs = db.get_share_asset_refs(filename=src_share)
            try:
                jsonfile = [x['local_path'] for x in refs if x['local_path'].endswith('.json')][0]
                print('jsonfile: ', jsonfile)
            except:
                print('Json file not found.')
                jsonfile = None

        #
        bp_params = None
        if ui_table_engine._dont_show_blueprintify is None:
            w = BlueprintSettings()
            d = uiutils.PromptDialog('Blueprint settings', u'', wd=w, btns=[u'ブループリント化',u'しない'], show_repeat=True)
            res = d.exec_()
            
            bp_params = w.get_params()

            if d.cb_repeat.isChecked():
                if res != 1:
                    ui_table_engine._dont_show_blueprintify = False
                else:
                    ui_table_engine._dont_show_blueprintify = bp_params
                    
            if res != 1:
                return False
        else:
            if ui_table_engine._dont_show_blueprintify is False:
                return False
            bp_params = ui_table_engine._dont_show_blueprintify

        
        try:
            self.blueprintify(args, asset, tags, bp_params, imported_object, jsonfile)
        except:
            import traceback
            print (traceback.format_exc())
            return False
            
        return True


    def blueprintify(self, args, asset, tags, bp_params, imported_object, jsonfile):
        dither_enabled = bp_params['dither'] if 'dither' in bp_params else False

        blueprintable_objs = []
        first_dst = None
        for obj_path in imported_object:
            adata = alib.find_asset_data(obj_path)
            if not self._is_asset_to_blueprintify(adata):
                continue

            dst = get_destination(obj_path, args, tags, asset)
            if dst is None:
                continue
            if first_dst is None:
                first_dst = dst
            blueprintable_objs.append(obj_path)

            if jsonfile is None:
                ex = check_existence(dst)
                try:
                    unreal.PythonCallableLibrary.create_blueprint([obj_path], dst, '', dither_enabled)
                except Exception as e:
                    print(e)
                else:
                    if not ex:
                        alib.save_asset(dst) # 新規に作成された場合のみローカル保存。
                                             # 未保存ではDependecyが確立されていないので保存時にBPがひっぱってこれないため。

        if jsonfile is not None:
            if len(blueprintable_objs) > 0:
                vis_mesh = find_first_visible_mesh(blueprintable_objs, jsonfile)
                print('First visible mesh: ', vis_mesh)
                if vis_mesh is None:
                    if first_dst is not None:
                        dst = first_dst
                    else:
                        pass # 最後にインポートされたstaticMeshをbpパス生成に使用
                
                else:
                    assert vis_mesh in args['imported_names']
                    dst = get_destination(vis_mesh, args, tags, asset)
                    print('destination: ', dst)
                    if dst is None:
                        raise Exception('Output config not found for: ' + vis_mesh)

                import P4
                ex = False
                try:
                    ex = check_existence(dst)
                except P4.P4Exception as e:
                    print(e)
                except Exception as e:
                    raise (e)

                try:
                    unreal.PythonCallableLibrary.create_blueprint(blueprintable_objs, dst, jsonfile, dither_enabled)
                except Exception as e:
                    print(e)
                else:
                    if not ex and alib.does_asset_exist(dst):
                        alib.save_asset(dst)


    def apps_executable_on(self):
        return [Application.UnrealEngine]

    def is_asset_eligible(self, asset):
        if asset.assetgroup == 'environment' and asset.task == 'model':
            return True
        else:
            return False
