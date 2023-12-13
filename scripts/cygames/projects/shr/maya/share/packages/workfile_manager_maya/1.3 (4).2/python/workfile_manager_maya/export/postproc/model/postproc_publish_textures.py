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
from workfile_manager.plugin_utils import Application
from workfile_manager_maya.export.postproc.postproc_maya_base import MayaPostprocBase


class Plugin(MayaPostprocBase):
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

    #def execute_on_local_publish(self):
    #    return False

    def execute(self, args):
        """
        テクスチャーをshare領域にコピーして、シーン内のパス参照を置き換える。
        コミット時にP4の元テクスチャーの場所を取得するために、元ファイルと使用リビジョンの情報をdictに格納して返す。

        Result:
            {<share_texture_path>:(<texture_path_on_p4>, <revision>), ...}
        """
        from workfile_manager import p4utils, cmds as wcmds
    
        p4u = p4utils.P4Utils.get_instance()
        user = wcmds.get_p4user_on_postproc()
        if user is not None:
            p4u.user = user
        p4u.p4.cwd = os.environ['WM_P4_ROOT_DIR']
        p4u.setclient()

        from cylibassetdbutils.assetvar import ShareAsset
        texdir = ShareAsset.get_texture_dir_from_master_file(args['outfile'])
        
        if not os.path.exists(texdir):
            os.makedirs(texdir)

        submit_server = True if 'submit_server' in args and args['submit_server'] else False

        from workfile_manager_maya import assetutils_maya
        if not submit_server:
            buf = assetutils_maya._get_textures(target_nodes=None)
            args['textures'] = assetutils.get_file_revisions(buf)

        texture_names = [x[0] for x in args['textures']]

        print('texture_names: ', texture_names, flush=True)
        files_done = {}
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
                    filepaths_on_node = _type['get_command'](fn)
                else:
                    f = cmds.getAttr(fn+'.'+_type['attr'])
                    filepaths_on_node = [assetdbutils.normalize_path(f)]
                
                for filepath_on_node in filepaths_on_node:
                    print('filepath_on_node: ', filepath_on_node)
                    if filepath_on_node not in files_done:
                        basename = os.path.basename(filepath_on_node)
                        filebase = re.sub('[.][^.]*$', '', basename)
                        fileext = re.sub('^.*[.]', '', basename)

                        cnt = 1
                        while True:
                            if basename not in used_basenames:
                                break
                            basename = filebase + '_%d' % cnt + '.' + fileext
                            cnt += 1

                        share_texpath = assetdbutils.normalize_path(os.path.join(texdir, basename))

                        if assetutils.is_share_file(filepath_on_node):
                            print('Already published texture: ', filepath_on_node)
                            continue
                            
                        assert(filepath_on_node.startswith(assetdbutils.normalize_path(os.environ['WM_P4_ROOT_DIR'])))
                        
                        if filepath_on_node not in texture_names:
                            """
                            パブリッシュ操作の過程で生成されたテクスチャー
                            もしくは何らかの理由で、パブリッシュ操作時にtexture_namesに登録されなかったテクスチャー（ケースについては現在サポートしていない。）
                            """
                            rev = None

                        else:
                            """
                            パブリッシュ操作をしたときにすでに存在したテクスチャー
                            """
                            idx = texture_names.index(filepath_on_node)
                            rev = args['textures'][idx][1]
                            assert(rev is not None)
                            try:
                                if os.path.exists(filepath_on_node):
                                    p4u.p4_run_xxx('edit', filepath_on_node)
                            except:
                                pass

                            try:
                                p4u.p4_run_xxx('sync', '--parallel=threads=8', '%s#%d' % (filepath_on_node, rev))
                                p4u.p4_run_xxx('revert', filepath_on_node)
                            except Exception as e:
                                print('WARNING: P4 Exception:')
                                print(e)
                                if not os.path.exists(filepath_on_node):
                                    try:
                                        p4u.p4_run_xxx('revert', filepath_on_node)
                                    except:
                                        pass
                            
                        if submit_server:
                            print('copying...', filepath_on_node, share_texpath)
                            if os.path.exists(share_texpath):
                                subprocess.call('attrib -R "%s" /S /D' % share_texpath.replace('/', '\\'))

                            shutil.copyfile(filepath_on_node, share_texpath)
                        
                        files_done[filepath_on_node] = share_texpath

                        used_basenames.append(os.path.basename(share_texpath))

                        maps[share_texpath] = (filepath_on_node, rev)
                    
                    else:
                        share_texpath = files_done[filepath_on_node]

                    if submit_server:
                        assetutils_maya.set_texture(fn, share_texpath)
        
        return maps

    def get_label(self):
        return 'Publish Textures'

    def default_checked(self):
        return True

    def is_editable(self):
        return False