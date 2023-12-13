# -*- coding: utf-8 -*-
from __future__ import print_function, annotations
import os
import shutil
import re
import copy
import subprocess
import yaml
import traceback

try:
    import maya.cmds as cmds
    import maya.mel as mel
except:
    pass

from workfile_manager.plugin_utils import OnCommitProcBase, Application, CommitProcessResult
from cylibassetdbutils import assetutils, assetdbutils
from cylibassetdbutils.structures import FileToRegister
import workfile_manager.p4utils as p4utils
from wmutils import wmlog

logger = wmlog.get_logger(__name__)

def export_extra_params(ex_filename):
    print('ex_filename: ', ex_filename)
    nodes = {}
    for fn in cmds.ls(type='file'):
        if fn not in nodes:
            nodes[fn] = []
        pname = 'colorSpace'
        value = cmds.getAttr(fn+'.'+pname)
        ptype = cmds.getAttr(fn+'.'+pname, type=True)
        nodes[fn].append({'attribute':pname, 'value':value, 'attr_type':ptype})

        pname = 'uvTilingMode'
        value = cmds.getAttr(fn+'.'+pname)
        ptype = cmds.getAttr(fn+'.'+pname, type=True)
        nodes[fn].append({'attribute':pname, 'value':value, 'attr_type':ptype})
    
    params = {'application':{'maya':{'nodes':nodes}}}
    
    subprocess.call('attrib -R "%s"' % ex_filename)

    with open(ex_filename, 'w') as fhd:
        yaml.dump(params, fhd)

def rename_non_unique_materials():
    mats = cmds.ls(mat=True)
    mats_no_ns = [re.sub('.*:', '', x) for x in mats]
    for order, m in enumerate(mats):
        m_ = re.sub('.*:', '', m)
        print('m_: ', m_)
        tbuf = copy.deepcopy(mats_no_ns)
        tbuf.pop(order)
        if m_ in tbuf:
            i = 1
            base = re.sub('_\d+$', '', m_)
            while True:
                newname = base + '_%02d' % i
                if cmds.objExists(newname) and newname not in mats_no_ns:
                    i += 1
                    continue
                break
            if m == newname:
                continue
            try:
                newname = cmds.rename(m, newname)
                mats_no_ns[order] = newname
                print(' renamed -> ', newname)
            except:
                pass


class Plugin(OnCommitProcBase, object):
    """
    コミット処理の過程で一番最後に実行されるコミットプロセス
    現在開いているシーンに対して実行する。

    処理内容:
    - リファレンスのインポート
    - shareのテクスチャーから元のp4上にあるテクスチャーへの差し替え
    - ネームスペースで区別されている同名マテリアルのユニークネーム化（現在実行停止中）
    - マスターFBXファイルの書き出し
    - エクストラパラメータ―ファイル(exprm)の書き出し
    - サムネイルファイルの取得
    - 新エンジンアセットのバージョン生成
    ※実際のP4へのサブミットやDBへの登録はここでは行わない

    Return:
        - DBに登録するファイルとリビジョンのペア―のリストを返す

    """
    def __init__(self):
        self.init()
    
    def apps_executable_on(self):
        return [
            Application.Maya,
            Application.MotionBuilder,
            Application.UnrealEngine,
            Application.Standalone,
        ]

    def is_asset_eligible(self, asset):
        return True

    def gen_unique_mat_name(self, org_name, simple_mat_name):
        if simple_mat_name not in self.same_name_mats:
            self.same_name_mats[simple_mat_name] = (0, [])
        else:
            buf = [x[0] for x in self.same_name_mats[simple_mat_name][1]]
            if org_name in buf:
                return self.same_name_mats[simple_mat_name][1][buf.index(org_name)][1]

        idx = self.same_name_mats[simple_mat_name][0] + 1

        while True:
            cand = '%s_%d' % (simple_mat_name, idx)
            buf = cmds.ls(cand, r=True)
            if len(buf) > 0:
                idx += 1
                continue
            uname = cand

            buf = self.same_name_mats[simple_mat_name][1]
            buf.append((org_name, uname))
            self.same_name_mats[simple_mat_name] = (idx, buf)
            return uname


    

    def set_textures(self, p4u, files:list[FileToRegister], args:dict) -> None:
        """
        シーン内のShare領域にあるテクスチャー（キャッシュされたパスはのぞく）に対して、
        P4上の元ファイルをたどり、ファイル名とリビジョンをfilesに格納する。
        該当しないテクスチャーはスキップされる。
        """
        print('>> set_textures')
        from workfile_manager import cmds as wcmds
        from workfile_manager_maya import assetutils_maya
        db = assetdbutils.DB.get_instance()

        print('set_textures args:', args)

        submit_server = True if 'submit_server' in args and args['submit_server'] else False

        for _type in assetutils_maya.texture_types:
            try:
                nodes = cmds.ls(type=_type['type'])
            except:
                continue

            for f in nodes:
                print('>> node: ', f)
                if 'get_command' in _type:
                    buf = _type['get_command'](f)
                else:
                    buf = [assetdbutils.normalize_path(cmds.getAttr(f+'.'+_type['attr']))]

                for path in buf:
                    print('path: ', path)
                    path = wcmds.get_share_path_from_cache(path)

                    if assetutils.is_non_cached_share_file(path):
                        #print('WARNING: Texture outside share area found: ' + path)
                        #continue

                        print('path: ', path)
                        buf = db.get_share_asset_refs(ref_filename=path)
                        if len(buf) == 0:
                            print('WARNING: db record not found: ', path)
                            continue
                        print('buf:', buf)
                        org_texture = buf[0]['source']
                        print('org_texture: ', org_texture)
                        rev = buf[0]['source_revision']
                        if org_texture is None or rev is None:
                            print('WARNING: source info not found.')

                            if rev is None:
                                from workfile_manager import notification
                                message = 'コミット時にソーステクスチャーのリビジョンが特定出来ませんでした: ' + path
                                notification.send_to_slack(message, 'takeuchi_kengo')

                            continue
                        rev = int(rev)
                        
                        if submit_server:
                            try:
                                p4u.p4_run_xxx('edit', org_texture)
                            except:
                                pass
                            try:
                                p4u.p4_run_xxx('sync', '--parallel=threads=8', '%s#%d' % (org_texture, rev))
                            except:
                                print(traceback.format_exc())
                                if not os.path.exists(org_texture):
                                    try:
                                        p4u.p4_run_xxx('revert', org_texture)
                                    except:
                                        pass
                            
                            try:
                                p4u.p4_run_xxx('revert', org_texture)
                            except:
                                pass
                        else:
                            try:
                                p4u.p4_run_xxx('revert', '-a', org_texture)
                            except:
                                pass

                        
                        if not os.path.exists(org_texture):
                            print('WARNING: Texture not exists: ' + org_texture)
                            continue

                        assetutils_maya.set_texture(f, org_texture)

                        files.append(FileToRegister(org_texture, rev))

                    elif assetutils.is_in_p4_workspace(path):
                        files.append(FileToRegister(path))
                    else:
                        logger.warning('Texture in neither work nor share area found: %s', path)
                        continue



    def execute(self, args) -> CommitProcessResult:
        from workfile_manager import cmds as wcmds
        from workfile_manager_maya import assetutils_maya

        keep_intermediate = True if 'keep_intermediate' in args and args['keep_intermediate'] else False

        db = assetdbutils.DB.get_instance()
        p4u = p4utils.P4Utils.get_instance()
        if 'submit_server' in args and args['submit_server']:
            user = wcmds.get_p4user_on_postproc()
            if user is not None:
                p4u.user = user
        p4u.p4.cwd = os.environ['WM_P4_ROOT_DIR']
        p4u.setclient()
        
        current_filename = cmds.file(sn=True, q=True)
        asset = args['asset']
        srcfile = args['filename']

        asset.set_path_template(tags=args['tags'])

        self.same_name_mats = {} # key: (current_idx, [('org_mat_name', 'new_mat_name'), ...])

        if keep_intermediate:
            assetutils_maya.write_tempfile('restruct_01', current_filename)

        #self.add_material_meta()

        # import references.
        nr = len(assetutils_maya.get_valid_reference_nodes())
        for _ in range(nr):
            for r in assetutils_maya.get_valid_reference_nodes():
                p =cmds.referenceQuery(r, rfn=True, p=True)
                if p is None:
                    if cmds.referenceQuery(r, isLoaded=True):
                        cmds.file(ir=True, rfn=r)
            
        # rename non-unique-named materials.
        for k in self.same_name_mats:
            for m in self.same_name_mats[k][1]:
                print('Rename %s -> %s' % (m[0], m[1]))
                cmds.rename(m[0], m[1])


        commit_process_result: CommitProcessResult = CommitProcessResult()

        #if 'submit_server' in args and args['submit_server']:
        self.set_textures(p4u, commit_process_result.files_to_register, args)

        if 'override_commit_output' in args['global_args']:
            output_fbx_path = args['global_args']['override_commit_output']
        else:
            output_fbx_path = args['engine_output_path']

        print('output_fbx_path: ', output_fbx_path)
        output_fbx_dir = os.path.dirname(output_fbx_path)
        if not os.path.exists(output_fbx_dir):
            os.makedirs(output_fbx_dir)
        
        commit_process_result.files_to_register.insert(0, FileToRegister(output_fbx_path))
        
        subprocess.call('attrib -R "%s" /S /D' % output_fbx_path)

        
        dccutils = assetutils_maya.MayaUtils.get_instance()

        if 'frame_rate' in args:
            dccutils.set_framerate(args['frame_rate'])

        if 'frame_range' in args:
            try:
                print('frame_start: ', args['frame_range'][0])
                print('frame_end: ', args['frame_range'][1])
                dccutils.set_framerange(args['frame_range'][0], args['frame_range'][1])
            except:
                import traceback
                print(traceback.format_exc())
                print('Faild in setting framerange.')


        if keep_intermediate:
            assetutils_maya.write_tempfile('restruct_03', current_filename)

        mel.eval('FBXLoadExportPresetFile -f "%s"' % args['preset'])
        mel.eval('FBXExport -f "%s"' % output_fbx_path)
        print('Exported: ', output_fbx_path)

        # Export extra parameters
        #
        ex_filename = re.sub('[.][^.]+$', '.exprm', output_fbx_path)
        try:
            export_extra_params(ex_filename)
        except Exception as e:
            print(e)
            import traceback
            print(traceback.format_exc())
        else:
            commit_process_result.files_to_register.append(FileToRegister(ex_filename))

        #
        if 'submit_server' in args and args['submit_server']:
            engine_asset_version = db.next_available_engineasset_version(asset, output_fbx_path).version

            src_thumb = assetutils.Asset.thumbnail_filepath(srcfile, asset.version, replace_share_root=False)
            if not os.path.exists(src_thumb):
                src_thumb = assetutils.Asset.thumbnail_filepath(srcfile, asset.version)    

            print('src_thumb: ' + src_thumb)
            if os.path.exists(src_thumb):
                dst_thumb = assetutils.Asset.thumbnail_filepath(output_fbx_path, engine_asset_version)
                dst_dir = os.path.dirname(dst_thumb)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                print('dst_thumb: ' + dst_thumb)
                if not os.path.exists(dst_thumb):
                    shutil.copyfile(src_thumb, dst_thumb)
                commit_process_result.files_to_register.append(FileToRegister(dst_thumb))
        else:
            engine_asset_version = None

        
        commit_process_result.engine_asset_version = engine_asset_version
        return commit_process_result

    def get_label(self):
        return 'Restruct'

    def order(self):
        return 99999999

    def get_args(self):
        return None

    def default_checked(self):
        return True

    def is_editable(self):
        return False

    def module_path(self):
        return None

    def func_in_error(self):
        pass

