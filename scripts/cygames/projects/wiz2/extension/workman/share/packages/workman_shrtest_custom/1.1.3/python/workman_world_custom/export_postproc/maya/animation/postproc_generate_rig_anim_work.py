# -*- coding: utf-8 -*-
from __future__ import print_function

from workfile_manager.plugin_utils import PostProcBase, PluginType, Application
from cylibassetdbutils import assetdbutils, assetutils

try:
    import maya.cmds as cmds
    import pymel.core as pm
    from workfile_manager_maya import assetutils_maya
except:
    pass

import os, shutil

db = assetdbutils.DB.get_instance()

class Plugin(PostProcBase):
    def apps_executable_on(self):
        return (
            Application.Maya, Application.MotionBuilder, Application.Standalone
        )

    def is_asset_eligible(self, asset):
        if asset.task == 'animation':
            return True
        else:
            return False
            
    def order(self):
        return 0
    
    def getlabel(self):
        return 'Generate workfile(s)'

    def default_checked(self):
        return False

    def is_editable(self):
        return False


    def execute(self, args):
        dccutils = assetutils_maya.MayaUtils.get_instance()
        cmds.file(f=True, new=True)

        animfile = args['animation_file']
        print('animfile: ', animfile)

        rigfile = args['rig_file']

        # Get rig asset.
        buf = db.get_sharedasset_from_file(rigfile)
        if len(buf) == 0:
            raise Exception('Rig not found in DB.')
        
        model_asset = assetutils_maya.ModelAssetMaya()
        for k in model_asset.get_dict():
            setattr(model_asset, k, buf[0][k])

        anim_asset = assetutils_maya.AnimationAssetMaya()
        for k in anim_asset.get_dict():
            setattr(anim_asset, k, buf[0][k])

        # Reference rig.
        ns = model_asset.get_namespace()
        model_asset.import_(rigfile, namespace_option=2, namespace=ns, **{'r': True})
        assetutils_maya.load_unloaded_references()

        # Select a node which an animation will be imported to.
        try:
            cmds.select(cmds.ls(ns+':*')[0], ne=True)
        except:
            print("Error: Nothing selected which an aimation will be imported to.")

        # Import animation file here.
        print('Importing animation...', animfile)
        print('Import namespace: ', ns)
        anim_asset.import_(animfile, namespace_option=3, namespace=ns)

        try:
            buf = db.get_sharedasset_from_file(animfile)
            if len(buf) == 0:
                raise Exception('Animation not found in DB.')
            frame_start = buf[0]['frame_start']
            frame_end = buf[0]['frame_end']
            frame_rate = buf[0]['frame_rate']
            print('frame_start:', frame_start)
            print('frame_end:', frame_end)
            print('frame_rate:', frame_rate)
            dccutils.set_framerate(frame_rate)
            dccutils.set_framerange(frame_start, frame_end, set_edit_range=True)
        except Exception as e:
            print(e)
            print('Warning: cannot set frame range.')


        thumb_filename = assetutils.Asset.thumbnail_filepath(args['tmp_output'], 0)
        if os.path.exists(args['thumbnail_source']):
            dstdir = os.path.dirname(thumb_filename)
            if not os.path.exists(dstdir):
                os.makedirs(dstdir)
            shutil.copyfile(args['thumbnail_source'], thumb_filename)
        print('thumb_filename:', thumb_filename)

        # save as new workfile.
        cmds.file(rn=args['tmp_output'])
        cmds.file(f=True, save=True, type='mayaAscii', pr=True)
                
        return True

    
