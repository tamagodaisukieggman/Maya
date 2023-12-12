# -*- coding: utf-8 -*-
from __future__ import annotations
import yaml, os, shutil, re, subprocess
from workfile_manager import p4utils
from workfile_manager.ui import ui_table_common
from cylibassetdbutils import assetdbutils
from workman_shenron_custom.asset_extension import workman_asset_extension
from workfile_manager_maya import assetutils_maya

p4u = p4utils.P4Utils.get_instance()

from maya import cmds

class Task:
    ShareRoot = 'c:/cygames/shrshare/share/asset'
    P4MirrorRoot = 'c:/cygames/shrdev/shr_art/resources/ta/workman/share_mirrored/asset'
    tracebacks = []

    def repath(self, org_path) -> str:
        new_path = org_path.replace(self.ShareRoot, self.P4MirrorRoot)
        new_path = re.sub('_v\d{3}', '', new_path)
        return new_path

    def copy_textures(self) -> list[str]:
        copied_textures = []

        for file_node in cmds.ls(type='file'):
            path = assetdbutils.normalize_path(cmds.getAttr(file_node+'.fileTextureName'))
            
            assert path.startswith(self.ShareRoot)
            
            dst = self.repath(path)
            dst_dir = os.path.dirname(dst)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            if os.path.exists(dst):
                subprocess.call(f'attrib -R {dst}')

            shutil.copyfile(path, dst)
            print('Texture in share copied: %s -> %s' % (path, dst), flush=True)
            cmds.setAttr(file_node+'.fileTextureName', dst, type='string')
            copied_textures.append(dst)

        return copied_textures


    def execute(self, argfile):
        with open(argfile, encoding='utf8') as fhd:
            args = yaml.load(fhd, Loader=yaml.UnsafeLoader)
        asset_content_items:list[ui_table_common.AssetContentItem] = args['asset_content_items']

        files_to_submit = []
        submit_sources = []

        for asset_content_item in asset_content_items:
            for version in asset_content_item.versions:
                path = version['path']
                if path.startswith(self.ShareRoot):
                    self.target_scenefiles.append(path)

                    assetutils_maya.cached_share_safe_open(path)

                    print('File opened:', path, flush=True)
                    copied_textures = self.copy_textures()
                    dst_maya_scene_path = self.repath(path)
                    dst_maya_scene_dir = os.path.dirname(dst_maya_scene_path)
                    if not os.path.exists(dst_maya_scene_dir):
                        os.makedirs(dst_maya_scene_dir)

                    if os.path.exists(dst_maya_scene_path):
                        subprocess.call(f'attrib -R {dst_maya_scene_path}')

                    cmds.file(rn=dst_maya_scene_path)
                    cmds.file(s=True, f=True, type='mayaBinary')
                    print('File saved:', dst_maya_scene_path, flush=True)
                    files_to_submit += [dst_maya_scene_path]
                    files_to_submit += copied_textures
                    submit_sources.append(path)

        if len(files_to_submit) > 0:
            comment = 'Shareアセットをミラーリング\n' + '\n'.join(submit_sources)
            p4u.p4_run_xxx('reconcile', ['-ea'] + files_to_submit)
            p4u.submitfiles(files_to_submit, reopen=False, desc=comment)
            self.submitted_files = files_to_submit


    
def postfunc(argfile=None, presetname=None):
    task = Task()
    workman_asset_extension.share_asset_mirroring_cmd(task, argfile)

    