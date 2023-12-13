# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import shutil
import re
import copy
import subprocess
import json

try:
    import maya.cmds as cmds
    import maya.mel as mel
except:
    pass

from workfile_manager.plugin_utils import OnCommitProcBase, Application

class Plugin(OnCommitProcBase, object):
    def __init__(self):
        self.init()
    
    def init(self):
        pass
    
    def apps_executable_on(self):
        return [
            Application.Maya,
            Application.Standalone,
        ]

    def is_asset_eligible(self, asset):
        if asset.assetgroup == 'environment' and asset.task == 'model':
            return True
        return False
    
    def execute(self, args):
        # from cylibassetdbutils import assetdbutils
        # db = assetdbutils.DB.get_instance()
        # share_filename = args['filename']
        # buf = db.get_sharedasset_from_file(share_filename)
        # if len(buf) == 0:
        #     raise Exception('No share asset found.')
        # sh_assetdict = buf[0]
        # sh_version = sh_assetdict['version']
        # buf = db.get_share_asset_refs(filename=share_filename, include_omit=False)
        # json_filenames = [x['local_path'] for x in buf if x['local_path'].endswith('.json') and x['version']==sh_version]
        # print('json_filenames: ', json_filenames)



        # sel_org = cmds.ls(sl=True)
        
        # json_path = ""
        # for json_filename in json_filenames:
        #     if "_physics_data_" in json_filename:
        #         json_path = json_filename
        #         break

        from workman_world_custom.export_postproc.maya.model import export_collision_settings
        sel_org = cmds.ls(sl=True)
        json_path = export_collision_settings.get_json_path_from_masterfile(args['engine_output_path'])
        print("json_path>>"+json_path)
        
        #古いファイルに対応
        if json_path == "":
            return

        #//一時的に決め打ち
        json_open = open(json_path)
        json_load = json.load(json_open)
       
        for mesh in cmds.ls(type='mesh'):
            meshtr = cmds.listRelatives(mesh, p=True, pa=True)[0]
            try:
                print ([meshtr,json_load["mesh_datas"]["datas"][meshtr]])
                if json_load["mesh_datas"]["datas"][meshtr]["simple_phys_material"] != None:
                    
                    attrname = 'outputrule__mesh_physics_type'
                    try:
                        print (meshtr+">>"+attrname)
                        cmds.addAttr(meshtr, ln=attrname, dt='string')
                    except:
                        pass
                    
                    #今のところダミーの場合のみなので決め打ち
                    node_type = "dmy"
                    cmds.setAttr('%s.%s' % (meshtr, attrname), node_type, type='string')    
            except:
                continue

        cmds.select(sel_org, ne=True)

    def getlabel(self):
        return 'Add physics Metadata'

    def order(self):
        return 99999

    def get_args(self):
        return None

    def default_checked(self):
        return True

    def is_editable(self):
        return False


