# -*- coding: utf-8 -*-
from __future__ import print_function, annotations
import os
import importlib
import re
import yaml
import copy
import subprocess
import traceback

try:
    import maya.cmds as cmds
except:
    pass

from cylibassetdbutils import assetdbutils, assetvar
from cylibassetdbutils.structures import CommitArgument, FileToRegister
import workfile_manager.p4utils as p4utils
from workfile_manager.plugin_utils import OnCommitProcBase, CommitProcessResult
from workfile_manager.export import CommitTarget
from wmutils import wmlog, notification
from workfile_manager import cmds as wcmds
import shutil

db = assetdbutils.DB.get_instance()
logger = wmlog.get_logger(__name__)

def find_desc_files(dir_):
    for root, _, files in os.walk(dir_):
        for file in files:
            if os.path.basename(file).startswith('_'):
                continue
            if re.search('.*[.]desc$', file):
                tp = os.path.join(root, file).replace('\\', '/')
                yield tp

def get_output_path(tags, asset):
    asset.set_path_template(tags=tags)

    export_name = asset.get_exportname(use_path_template=True)[0]
    fbxpath = re.sub('[.][^.]+$', '.fbx', export_name)
    return fbxpath

def execute(argfile:str|None, open_scene:bool=True, args:dict|None=None):
    """
    args['targets']に複数コミットのターゲット情報が格納されている。
    
    複数ターゲットそれぞれに対して、コミットプロセスとFBX書き出しを実行し(P4サブミット&DB登録はまだ)、
    P4サブミット&DB登録すべきファイルリストをtarget['files_to_register']に格納する。

    lazy_submitの場合、
        P4サブミット&DB登録に進めるかどうかをsessionファイルを見て確認する。
        進める場合は、必要なファイル群を収集し、P4サブミット&DB登録。
    
    lazy_submitではない場合、
        全てのファイルは現マシンのローカルに存在するので、そのままP4サブミット&DB登録。

    ※lazy_submitかどうかによらず、targetは複数存在しうることに注意。
    """

    # TODO: Remove dcc dependencies.
    try:
        from postproc_set_editor_mbuilder import ui_mbuilder
        dcc_cmds = ui_mbuilder.DccCmds()
    except:
        from postproc_set_editor_maya import ui_maya
        dcc_cmds = ui_maya.DccCmds()

    p4u = p4utils.P4Utils.get_instance()

    if argfile is None:
        assert args is not None
    else:
        print('argfile: ', argfile.replace('/', '\\'))
        with open(argfile) as _argfile:
            args = wcmds.yaml_load(_argfile)
    
    
    if 'submit_server' in args and args['submit_server']:
        user = wcmds.get_p4user_on_postproc()
        print('user:', user)
        if user is not None:
            p4u.user = user

    print('p4user:', p4u.user)
    p4u.p4.cwd = os.environ['WM_P4_ROOT_DIR']
    p4u.setclient()

    # Mayaで実行されている場合のみ必要
    # TODO: DCC非依存に
    try:
        if not cmds.pluginInfo('fbxmaya', q=True, l=True):
            cmds.loadPlugin('fbxmaya')
    except:
        pass

    # 全ターゲットにおける全てのサブミット対象となるファイルのリスト
    files_to_register: list[FileToRegister] = []

    commit_targets: list[CommitTarget] = args['targets']
    print('commit_targets:', commit_targets)

    for target_idx, target in enumerate(commit_targets):
        
        filename = target.share_asset_info.share_master_filename
        print('share_master_filename: ', filename, flush=True)
        keep_intermediate = True if 'keep_intermediate' in args and args['keep_intermediate'] else False

        print('open_scene: ', open_scene, flush=True)
        print('target_idx: ', target_idx, flush=True)
        if open_scene or target_idx > 0:
            dcc_cmds.dccutils().open(filename)
        
            if keep_intermediate:
                dotpos = filename.index('.')
                im = filename[:dotpos] + '_maya_commit_im01' + filename[dotpos:]
                shutil.copyfile(filename, im)
                print('Intermediate written: ', im.replace('/', '\\'), flush=True)

        if target.share_asset_info.share_asset_dict is not None:
            share_asset_dict = target.share_asset_info.share_asset_dict
        else:    
            res = db.get_sharedasset_from_file(filename)
            if res is None:
                print('ERROR: No shareasset found.', filename.replace('/', '\\'))
                return
            if len(res) > 1:
                print('ERROR: Multiple shareasset matches.', filename.replace('/', '\\'))
                return
            
            share_asset_dict = res[0]

        asset = dcc_cmds.dccutils().create_engine_asset({})
        asset.copy_parameters_from_dict(share_asset_dict)

        asset.truncate_path_template()
        engine_output_path = get_output_path(target.share_asset_info.tags, asset)
        
        if share_asset_dict['frame_rate'] is not None:
            args['frame_rate'] = share_asset_dict['frame_rate']
        if share_asset_dict['frame_start'] is not None and share_asset_dict['frame_end'] is not None:
            args['frame_range'] = (share_asset_dict['frame_start'], share_asset_dict['frame_end'])

        if args['procs'] == []:
            if 'child_commitprocs' in args:
                args['procs'] = args['child_commitprocs']

        for _mod in args['procs']:
            try:
                mod = importlib.import_module(_mod['module_name'])
            except:
                continue
            ppargs = {}

            preset = os.path.join(os.path.dirname(__file__), '..', 'fbx_presets', args['preset'])
            preset = re.sub('\\\\', '/', preset)
            ppargs['preset'] = preset
            ppargs['filename'] = filename
            ppargs['asset'] = asset
            ppargs['user'] = args['user']
            ppargs['comment'] = args['comment']
            ppargs['tags'] = target.share_asset_info.tags
            ppargs['keep_intermediate'] = args['keep_intermediate'] if 'keep_intermediate' in args else False
            ppargs['submit_server'] = args['submit_server'] if 'submit_server' in args else False
            ppargs['engine_output_path'] = engine_output_path
            ppargs['global_args'] = args

            try:
                ppargs['frame_rate'] = args['frame_rate']
                ppargs['frame_range'] = args['frame_range']
            except:
                pass

            pp: OnCommitProcBase = mod.Plugin()
            print('[ON_COMMIT_PROC] ', pp.get_label(), flush=True)
            
            commit_proc_result: CommitProcessResult|None = pp.execute(ppargs)
            
            if commit_proc_result is None:
                continue

            if commit_proc_result.engine_asset_version is not None:
                # 原則on_commit_proc_restructのときのみ
                print('>>>>>>>>>>>>>>>>> commit_proc_result.engine_asset_version:', commit_proc_result.engine_asset_version)
                target.engine_asset_info.engine_asset.version = commit_proc_result.engine_asset_version
            
            if len(commit_proc_result.files_to_register) > 0:
                add0 = [x for x in commit_proc_result.files_to_register if x not in target.engine_asset_info.files_to_register]
                add1 = [x for x in commit_proc_result.files_to_register if x not in files_to_register]
                if _mod['module_name'].endswith('on_commit_proc_restruct'):
                    """
                    マスターfbx書き出しプロセス(on_commit_proc_restruct)の時は先頭に挿入
                    """
                    target.engine_asset_info.files_to_register = add0 + target.engine_asset_info.files_to_register
                    files_to_register = add1 + files_to_register
                else:
                    """
                    それ以外の通常プロセスの場合は後ろに追加
                    """
                    target.engine_asset_info.files_to_register += add0
                    files_to_register += add1
                    
            print('[DONE] ', pp.get_label(), flush=True)

    if 'lazy_submit' in args and args['lazy_submit']:
        print ('lazy_submit...', flush=True)

        assert 'lazy_submit_session' in args
        assert 'lazy_publish_cnts' in args

        session_name = args['lazy_submit_session']
        print('session_name: ', session_name, flush=True)
        print('lazy_publish_cnts: ', args['lazy_publish_cnts'], flush=True)

        tmpdir = None
        try:
            if os.path.exists(os.environ['WM_TMP_DIR']):
                tmpdir = os.environ['WM_TMP_DIR']
        except:
            pass
        assert tmpdir is not None
        assert 'COMPUTERNAME' in os.environ
        datestr = assetdbutils.datetime_to_str(msec=True, for_filename=True)
        session_dir = os.path.join(tmpdir, 'commit', session_name)
        jobname = '%s_%s' % (datestr, os.environ['COMPUTERNAME'])
        tmpdir = os.path.join(session_dir, jobname)
        print('tmpdir: ', tmpdir, flush=True)
        
        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)
            
        for filename in [x.filename for x in files_to_register]:
            print('filename: ', filename, flush=True)
            desc_file_base = os.path.basename(filename) + '.desc'
            desc_file = os.path.join(tmpdir, desc_file_base)
            print('desc_file: ', desc_file, flush=True)
            with open(desc_file, 'w') as fhd:
                params = {'original_filename': filename}
                yaml.dump(params, fhd)

            dst = os.path.join(tmpdir, os.path.basename(filename))
            if os.path.exists(dst):
                subprocess.call('attrib -R "%s"' % dst)
            shutil.copyfile(filename, dst)

        print ('files copied successfully.', flush=True)

        # check session.
        session_file = os.path.join(session_dir, 'session.sdesc')

        assert os.path.exists(session_file)

        import filelock
        lock = filelock.FileLock(session_file + '.lock')
    
        try:
            with lock.acquire(timeout=30):
                with open(session_file, 'r') as fhd:
                    dic = wcmds.yaml_load(fhd)
                    if len(dic['commit_ready']) == (args['lazy_publish_cnts']-1):
                        # commit.
                        print ('launch commit.', flush=True)

                        # gather files.
                        for desc in find_desc_files(session_dir):
                            with open(desc, 'r') as fhd:
                                dic = wcmds.yaml_load(fhd)
                                org_file = dic['original_filename']
                            src = desc[:desc.rindex('.')]
                            try:
                                shutil.copyfile(src, org_file)
                            except:
                                pass
                        
                        #
                        import glob
                        commits = glob.glob(os.path.join(session_dir, '*.commit'))
                        targets: list[CommitTarget] = args['targets']
                        for cm in commits:
                            with open(cm, 'r') as fhd:
                                dic = wcmds.yaml_load(fhd)
                                targets += dic['targets']

                        from workfile_manager_maya import assetutils_maya
                        args['dccutils'] = assetutils_maya.MayaUtils.get_instance()

                        args.pop('lazy_submit')
                        
                        from workfile_manager import postproc_utils
                        postproc_utils.exec_all_commit_proc(args)

                    else:
                        dic['commit_ready'].append(jobname)
                        with open(session_file, 'w') as whd:
                            yaml.dump(dic, whd)

                        commit_file = os.path.join(session_dir, jobname+'.commit')
                        with open(commit_file, 'w') as fhd:
                            yaml.dump({'targets':args['targets']}, fhd)

        except filelock.Timeout:
            notification.send_to_slack(u'コミット時にセッションファイルをロックできませんでした。')
            
        finally:
            lock.release()

    elif 'fbx_export_session_filename' in args:
        from workfile_manager.ui import ui_table_engine
        
        fbx_export_session = ui_table_engine.FBXExportSession(args['fbx_export_session_filename'])
        key = files_to_register[0].filename
        fbx_export_session.add_target(key, None, None, None, None)
        result = ui_table_engine.FBXExportSessionJobResult(args, asset, files_to_register, files_to_register[0].filename)
        fbx_export_session.store_result(key, result)

    else:
        submit_and_register(args, asset, files_to_register)
        
            


def submit_and_register(args, asset, files_to_register:list[FileToRegister]) -> None:
    
    submit_server = 'submit_server' in args and args['submit_server']

    if submit_server:
        # P4サブミットコマンドに渡すファイルリスト
        # 既存のリビジョンを使用するものはサブミットコマンドに渡さない。
        # 既存リビジョンを使用するものは、このタイミングではdepotFileフィールドがセットされていないが、それらについては後にセットされる。
        p4u = p4utils.P4Utils.get_instance()
        files_to_submit: list[str] = [x.filename for x in files_to_register if x.revision is None]
        try:
            p4u.p4_run_xxx('reconcile', '-ea', files_to_submit)
        except Exception as e:
            print('on_commit_proc.execute: ', e)
        #for file_to_submit in files_to_submit:
        #    print('>> file_to_submit:', file_to_submit)
        res_org: list[str, dict] = p4u.submitfiles(files_to_submit, desc=u'%s (by %s)' % (args['comment'], args['user']), submit_outside=True)
        #print('>> res_org: ', res_org)
    else:
        res_org = None

    asseturls = []
    commmit_targets: list[CommitTarget] = args['targets']
    for target in commmit_targets:
        
        if res_org is not None:
            files_to_register_per_target: list[FileToRegister] = target.engine_asset_info.files_to_register
            
            #print('files_to_register_per_target:', files_to_register_per_target)

            for idx, file_to_register in enumerate(files_to_register_per_target):
                print('file_to_register.filename:', file_to_register.filename)
                if not submit_server:
                    backup_dir:str = wcmds.get_local_tempdir_for_now(makedirs_if_not_exist=True, subdir='local_publish_data', msec=True)
                    file_to_register.backup_file = assetdbutils.normalize_path(os.path.join(backup_dir, os.path.basename(file_to_register.filename)))
                    shutil.copyfile(file_to_register.filename, file_to_register.backup_file)
                    print(f'Copied {file_to_register.filename} -> {file_to_register.backup_file}')

                if file_to_register.revision is None:
                    try:
                        revision_dict:dict = [x for x in res_org if x[0]==file_to_register.filename][0][1]
                    except:
                        import traceback
                        print(traceback.format_exc())
                        message = 'File not found in submitted: ' + file_to_register
                        notification.send_to_slack(message, 'takeuchi_kengo')
                        if idx == 0:
                            raise Exception('master file not found in submitted:')
                    
                    print('revision_dict:', revision_dict)
                    file_to_register.set_revision_from_dict(revision_dict)
                    file_to_register.depot_path = revision_dict['depotFile']
                
                
        else:
            files_to_register_per_target = None

        #print('>> files_to_register_per_target: ', files_to_register_per_target)

        args['asset'] = target.engine_asset_info.engine_asset
        args['filename'] = target.share_asset_info.share_master_filename
        commit_args = CommitArgument(args['asset'], args['user'], args['filename'], args['comment'])

        result_version = None

        if files_to_register_per_target:
            """
            target.engine_asset.versionはNoneの場合とそうでない場合がある。
            ローカルパブリッシュデータを後からpublicにする操作のとき、target.engine_asset.version=Noneである。
            """
            result_version = db.commit_to_engine(files_to_register_per_target, commit_args)
        else:
            """
            サブミットコマンド実行に際して、どのファイルもリビジョン更新されなかった時、
            もしくはローカルパブリッシュの時にここ来る
            """
            if submit_server:
                logger.info('No revisions updated.')
            else:
                engine_master_filename = target.engine_asset_info.files_to_register[0].filename
                commit_info_dir = os.path.dirname(engine_master_filename)
                commit_info_filename = os.path.join(commit_info_dir, re.sub('[.][^.]*$', '.commit_info', engine_master_filename))
                with open(commit_info_filename, 'w') as fhd:
                    fhd.write(yaml.dump(target))
                logger.info('commit info file exported: %s', commit_info_filename)

                engine_asset_dicts: list[dict] = db.get_engine_assets(commit_args.engine_asset, engine_master_filename, ignore_version=True)
                if len(engine_asset_dicts) == 0:
                    # エンジン領域にエントリーが存在しないときはプレイスホルダーのみDBに登録する

                    commit_args.engine_asset.version = 0
                    # プレイスホルダーのときはversion=0とする
                    commit_args.comment = ''
                    commit_args.username = ''
                    db.commit_to_engine([FileToRegister(engine_master_filename)], commit_args)

        try:
            asset = target.engine_asset_info.engine_asset
            asset.version = result_version
            master = target.engine_asset_info.files_to_register[0].filename
            asseturl = asset.get_url(master)

        except:
            asseturls.append(master.replace('/', '\\'))
        else:
            asseturls.append(asseturl)


    if submit_server:
        message = u'コミットが完了しました。\n' + \
            u'*コメント*\n```' + args['comment'] + '```\n' + \
            u'*出力アセット*\n```' +'\n'.join(asseturls) + '```\n'
    else:
        message = u'ローカル書き出しが完了しました。\n' + \
            u'*コメント*\n```' + args['comment'] + '```\n' + \
            u'*出力FBXファイル*\n```' + engine_master_filename.replace('/', '\\') + '```\n' + \
            u'*対応するEngineアセット枠*\n```' +'\n'.join(asseturls) + '```\n'
    
    
    try:
        notification.send_to_slack(message, args['user'])
        print('Commit finish message sent to', args['user'], flush=True)
    except UnicodeDecodeError:
        print(traceback.format_exc())
        message = u'コミットが完了しましたが、通知メッセージの送信に失敗しました。\nご面倒ですが、該当データを直接ご確認ください。'
        notification.send_to_slack(message, args['user'])

    if 'commit_log' in args:
        commit_logfile = args['commit_log']
        print('commit_logfile: ', commit_logfile)
        if not os.path.exists(commit_logfile):
            dirname = os.path.dirname(commit_logfile)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(commit_logfile, 'w') as fhd:
                fhd.write('')

        try:
            """
            本来であればacquireは一番外側にしたいところ。
            ただしacquire中にread/writeが許可されないためやむを得ず。正しいやり方を検討すること。
            ただし、acquire中であっても、yaml.load, yamp.dumpは出来る模様。

            """
            with open(commit_logfile, 'r') as rh:
                buf = rh.read()
            with open(commit_logfile, 'w') as fh:
                import filelock
                lock = filelock.FileLock(commit_logfile)
                with lock.acquire(timeout=300):
                    fh.write(buf + '\n'.join(asseturls) + '\n')
        except Exception as e:
            import traceback
            print(traceback.format_exc())




def submit_and_register_multi_items(submit_server:bool, items:list[tuple]) -> None:
    
    # items = [(args, asset, files_to_register:list[FileToRegister]), ...]
    
    files_to_register_all = []

    for item in items:
        files_to_register_all += item[2]

    if submit_server:
        # P4サブミットコマンドに渡すファイルリスト
        # 既存のリビジョンを使用するものはサブミットコマンドに渡さない。
        # 既存リビジョンを使用するものは、このタイミングではdepotFileフィールドがセットされていないが、それらについては後にセットされる。

        # 一つ目のアイテムのコメントとユーザー名を使用
        comment = items[0][0]['comment']
        user = items[0][0]['user']

        p4u = p4utils.P4Utils.get_instance()
        files_to_submit: list[str] = [x.filename for x in files_to_register_all if x.revision is None]
        try:
            p4u.p4_run_xxx('reconcile', '-ea', files_to_submit)
        except Exception as e:
            print('on_commit_proc.execute: ', e)
        res_org: list[str, dict] = p4u.submitfiles(files_to_submit, desc=u'%s (by %s)' % (comment, user), submit_outside=True)
    else:
        res_org = None

    #
    asseturls = []
    engine_master_filenames:list[str] = []

    for item in items:
        args = item[0]
        
        commmit_targets: list[CommitTarget] = args['targets']
        for target in commmit_targets:
            
            files_to_register_per_target: list[FileToRegister] = target.engine_asset_info.files_to_register

            for idx, file_to_register in enumerate(files_to_register_per_target):
                if not submit_server:
                    backup_dir:str = wcmds.get_local_tempdir_for_now(makedirs_if_not_exist=True, subdir='local_publish_data', msec=True)
                    file_to_register.backup_file = assetdbutils.normalize_path(os.path.join(backup_dir, os.path.basename(file_to_register.filename)))
                    shutil.copyfile(file_to_register.filename, file_to_register.backup_file)
                    print(f'Fbx file Copied {file_to_register.filename} -> {file_to_register.backup_file}')

            if res_org is not None:
                #print('files_to_register_per_target:', files_to_register_per_target)

                for idx, file_to_register in enumerate(files_to_register_per_target):
                    print('file_to_register.filename:', file_to_register.filename)
                        
                    if file_to_register.revision is None:
                        try:
                            revision_dict:dict = [x for x in res_org if x[0]==file_to_register.filename][0][1]
                        except:
                            import traceback
                            print(traceback.format_exc())
                            message = 'File not found in submitted: ' + file_to_register
                            notification.send_to_slack(message, 'takeuchi_kengo')
                            if idx == 0:
                                raise Exception('master file not found in submitted:')
                        
                        print('revision_dict:', revision_dict)
                        file_to_register.set_revision_from_dict(revision_dict)
                        file_to_register.depot_path = revision_dict['depotFile']
                    
                    
            else:
                files_to_register_per_target = None

            #print('>> files_to_register_per_target: ', files_to_register_per_target)

            args['asset'] = target.engine_asset_info.engine_asset
            args['filename'] = target.share_asset_info.share_master_filename
            commit_args = CommitArgument(args['asset'], args['user'], args['filename'], args['comment'])

            result_version = None
            if files_to_register_per_target:
                """
                target.engine_asset.versionはNoneの場合とそうでない場合がある。
                ローカルパブリッシュデータを後からpublicにする操作のとき、target.engine_asset.version=Noneである。
                """
                result_version = db.commit_to_engine(files_to_register_per_target, commit_args)
            else:
                """
                サブミットコマンド実行に際して、どのファイルもリビジョン更新されなかった時、
                もしくはローカルパブリッシュの時にここ来る
                """
                if submit_server:
                    logger.info('No revisions updated.')
                else:
                    engine_master_filename = target.engine_asset_info.files_to_register[0].filename
                    commit_info_dir = os.path.dirname(engine_master_filename)
                    commit_info_filename = os.path.join(commit_info_dir, re.sub('[.][^.]*$', '.commit_info', engine_master_filename))
                    with open(commit_info_filename, 'w') as fhd:
                        fhd.write(yaml.dump(target))
                    logger.info('commit info file exported: %s', commit_info_filename)

                    engine_asset_dicts: list[dict] = db.get_engine_assets(commit_args.engine_asset, engine_master_filename, ignore_version=True)
                    if len(engine_asset_dicts) == 0:
                        # エンジン領域にエントリーが存在しないときはプレイスホルダーのみDBに登録する

                        commit_args.engine_asset.version = 0
                        # プレイスホルダーのときはversion=0とする
                        commit_args.comment = ''
                        commit_args.username = ''
                        db.commit_to_engine([FileToRegister(engine_master_filename)], commit_args)

            try:
                asset = target.engine_asset_info.engine_asset
                asset.version = result_version
                master = target.engine_asset_info.files_to_register[0].filename
                engine_master_filenames.append(master.replace('/', '\\'))
                asseturl = asset.get_url(master)

            except:
                asseturls.append('<Not Found>')
            else:
                asseturls.append(asseturl)


    if submit_server:
        message = u'コミットが完了しました。\n' + \
            u'*コメント*\n```' + args['comment'] + '```\n' + \
            u'*出力アセット*\n```' +'\n'.join(asseturls) + '```\n'
    else:
        message = u'ローカル書き出しが完了しました。\n' + \
            u'*コメント*\n```' + args['comment'] + '```\n' + \
            u'*出力FBXファイル*\n```' + '\n'.join(engine_master_filenames) + '```\n' + \
            u'*対応するEngineアセット枠*\n```' +'\n'.join(asseturls) + '```\n'
    
    
    try:
        notification.send_to_slack(message, args['user'])
        print('Commit finish message sent to', args['user'], flush=True)
    except UnicodeDecodeError:
        message = u'コミットが完了しましたが、通知メッセージの送信に失敗しました。\nご面倒ですが、該当データを直接ご確認ください。'
        notification.send_to_slack(message, args['user'])

    if 'commit_log' in args:
        commit_logfile = args['commit_log']
        print('commit_logfile: ', commit_logfile)
        if not os.path.exists(commit_logfile):
            dirname = os.path.dirname(commit_logfile)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(commit_logfile, 'w') as fhd:
                fhd.write('')

        try:
            """
            本来であればacquireは一番外側にしたいところ。
            ただしacquire中にread/writeが許可されないためやむを得ず。正しいやり方を検討すること。
            ただし、acquire中であっても、yaml.load, yamp.dumpは出来る模様。

            """
            with open(commit_logfile, 'r') as rh:
                buf = rh.read()
            with open(commit_logfile, 'w') as fh:
                import filelock
                lock = filelock.FileLock(commit_logfile)
                with lock.acquire(timeout=300):
                    fh.write(buf + '\n'.join(asseturls) + '\n')
        except Exception as e:
            import traceback
            print(traceback.format_exc())            