# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import shutil
import subprocess

try:
    import maya.cmds as cmds
    from workfile_manager_maya import assetutils_maya
except:
    pass

from cylibassetdbutils import assetutils, assetdbutils
from workfile_manager.plugin_utils import PostProcBase, Application


class Plugin(PostProcBase):
    def apps_executable_on(self):
        return (
            Application.Maya,
            Application.MotionBuilder,
        )

    def is_asset_eligible(self, asset):
        if asset.task == 'material' or asset.task == 'model':
            return True
        else:
            return False

    def order(self):
        return 1000

    def execute_on_local_publish(self):
        return False

    def execute(self, args):
        from workfile_manager import p4utils, cmds as wcmds
    
        p4u = p4utils.P4Utils.get_instance()
        user = wcmds.get_p4user_on_postproc()
        if user is not None:
            p4u.p4.user = user
        p4u.p4.cwd = os.environ['WM_P4_ROOT_DIR']
        p4u.setclient()

        base = os.path.basename(args['outfile'])
        base = re.sub('[.][^.]+$', '', base)
        texdir = os.path.join(os.path.dirname(os.path.dirname(args['outfile'])), 'textures', base)
        texdir = texdir.replace('\\', '/')
        
        if not os.path.exists(texdir):
            os.makedirs(texdir)

        texture_names = [x[0] for x in args['textures']]
        print('texture_names: ', texture_names)
        copied_files = {}
        used_basenames = []

        maps = {}

        for _type in assetutils_maya.texture_types:
            try:
                nodes = cmds.ls(type=_type['type'])
            except:
                continue

            for fn in nodes:
                print('fn: ', fn)
                if 'get_command' in _type:
                    files = _type['get_command'](fn)
                else:
                    f = cmds.getAttr(fn+'.'+_type['attr'])
                    files = [assetdbutils.normalize_path(f)]
                
                for p in files:
                    print('p: ', p)
                    if p not in copied_files:
                        basename = os.path.basename(p)
                        filebase = re.sub('[.][^.]*$', '', basename)
                        fileext = re.sub('^.*[.]', '', basename)

                        cnt = 1
                        while True:
                            if basename not in used_basenames:
                                break
                            basename = filebase + '_%d' % cnt + '.' + fileext
                            cnt += 1

                        newpath = assetdbutils.normalize_path(os.path.join(texdir, basename))

                        if assetutils.is_share_file(p) or assetutils.is_cached_share(p):
                            print('Already published texture: ', p)
                            continue
                            
                        assert(p.startswith(assetdbutils.normalize_path(os.environ['WM_P4_ROOT_DIR'])))
                        
                        if p not in texture_names:
                            cmds.delete(fn)
                            continue

                        idx = texture_names.index(p)
                        rev = args['textures'][idx][1]
                        assert(rev is not None)
                        try:
                            if os.path.exists(p):
                                p4u.p4_run_xxx('edit', p)
                        except:
                            pass

                        try:
                            p4u.p4_run_xxx('sync', '--parallel=threads=8', '%s#%d' % (p, rev))
                            p4u.p4_run_xxx('revert', p)
                        except Exception as e:
                            print('WARNING: P4 Exception:')
                            print(e)
                            if not os.path.exists(p):
                                try:
                                    p4u.p4_run_xxx('revert', p)
                                except:
                                    pass
                            
                        print('copying...', p, newpath)
                        if os.path.exists(newpath):
                            subprocess.call('attrib -R "%s" /S /D' % newpath.replace('/', '\\'))
                        shutil.copyfile(p, newpath)
                        copied_files[p] = newpath
                        used_basenames.append(os.path.basename(newpath))
                        maps[newpath] = (p, rev)
                    
                    else:
                        newpath = copied_files[p]

                    assetutils_maya.set_texture(fn, newpath)
        
        return maps

    def getlabel(self):
        return 'Publish Textures'

    def default_checked(self):
        return True

    def is_editable(self):
        return False