# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import shutil
import re
import copy
import subprocess

try:
    import maya.cmds as cmds
    import maya.mel as mel
except:
    pass

from workfile_manager.plugin_utils import OnCommitProcBase, Application

def list_collision_materials(share_file):
    import yaml
    from cylibassetdbutils import assetdbutils
    db = assetdbutils.DB.get_instance()
    res = []
    refs = db.get_share_asset_refs(filename=share_file, include_omit=False)
    print('share_file:', share_file)
    for ref in refs:
        if not ref['local_path'].endswith('.json'):
            continue
        print('json:', ref['local_path'])
        try:
            with open(ref['local_path'], 'r') as fhd:
                ph_misc = yaml.load(fhd)
                for mat_name in list(ph_misc['materials']['datas'].keys()):
                    print('mat_name:', mat_name)
                    if ph_misc['materials']['datas'][mat_name]['materialName'] is not None:
                        res.append(mat_name)
        except:
            import traceback
            print(traceback.format_exc())
            continue

    print('materials for collision: ', res)
    return res

class Plugin(OnCommitProcBase, object):
    def apps_executable_on(self):
        return [
            Application.Maya,
            Application.Standalone,
        ]

    def is_asset_eligible(self, asset):
        return True

    
    def execute(self, args):
        print('>>> args: ', args)
        from workfile_manager_maya import assetutils_maya
        refnodes = assetutils_maya.get_valid_reference_nodes()
        refdict = {}
        for rn in refnodes:
            filename = cmds.referenceQuery(rn, filename=True, wcn=True)
            nodes = cmds.referenceQuery(rn, nodes=True)
            refdict[filename] = nodes

        m_to_filename = {}
        for m in cmds.ls(mat=True):
            for filename in list(refdict.keys()):
                if m in refdict[filename]:
                    m_to_filename[m] = filename
                    break
        
        col_mats = list_collision_materials(args['filename'])

        meshtr_done = []
        for mesh in cmds.ls(type='mesh'):
            meshtr = cmds.listRelatives(mesh, p=True, f=True)[0]
            if meshtr in meshtr_done:
                continue
            
            for mat in cmds.ls(mat=True):
                simple_name = re.sub('.*:', '', mat)
                if mat in list(m_to_filename.keys()):
                    if len(cmds.ls(simple_name, r=True)) > 1:
                        uname = self.gen_unique_mat_name(mat, simple_name)
                        attrname = 'workman_import_name_override__' + uname
                        try:
                            cmds.addAttr(meshtr, ln=attrname, dt='string')
                        except:
                            pass
                        cmds.setAttr('%s.%s' % (meshtr, attrname), simple_name, type='string')    

                        simple_name = uname

                    attrname = 'workman_share_asset__' + simple_name 
                    try:
                        cmds.addAttr(meshtr, ln=attrname, dt='string')
                    except:
                        pass
                    cmds.setAttr('%s.%s' % (meshtr, attrname), m_to_filename[mat], type='string')
                
                attrname = 'workman_materialtype__' + simple_name 
                try:
                    cmds.addAttr(meshtr, ln=attrname, dt='string')
                except:
                    pass

                if mat in col_mats:
                    cmds.setAttr('%s.%s' % (meshtr, attrname), 'collision', type='string')
                else:
                    mattype = cmds.objectType(mat)
                    print('mattype:'+mattype)
                    try:
                        if mattype == 'GLSLShader':
                            tech = cmds.getAttr(mat+'.technique')
                            mattype = 'GLSLShader:'+tech
                            print('mattype:'+mattype)
                        cmds.setAttr('%s.%s' % (meshtr, attrname), mattype, type='string')
                    except Exception as e:
                        print(e)

            meshtr_done.append(meshtr)


    def getlabel(self):
        return 'Add Material Metadata'

    def order(self):
        return 99999

    def get_args(self):
        return None

    def default_checked(self):
        return True

    def is_editable(self):
        return False


