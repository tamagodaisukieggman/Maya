# -*- coding: utf-8 -*-
from __future__ import print_function

from workfile_manager import postproc_utils, p4utils, cmds as wcmds
from workfile_manager.plugin_utils import PostProcBase, PluginType, Application, AssetAction
from cylibassetdbutils import assetdbutils, assetutils
import re, copy, os

p4u = p4utils.P4Utils.get_instance()

class Plugin(AssetAction):
    def apps_executable_on(self):
        return [Application.Maya]

    def is_asset_eligible(self, asset):
        if asset.area() != 'work':
            return False
        return True

    def getlabel(self):
        return 'Update assets'

    def allow_multi_items(self):
        return True

    def execute(self, args):
        from workfile_manager.ui import uiutils
        d = uiutils.PromptDialog('Confirmation', u'アップデートジョブを投げますか？', btns=['OK', 'Cancel'])
        d.resize(400, 160)
        res = d.exec_()
        if res != 1:
            return

        table = args['table']
        assets = args['assets']

        from workfile_manager_maya import assetutils_maya
        deadline_batchname = re.sub('[.][^.]*', '', assetdbutils.labelpostfix())
        p4user = p4u.p4.user

        deps = []
        asset_filenames = []
        for wasset in assets:
            wasset.version = wasset._version
            asset = assetutils_maya.ShareAssetMaya()
            asset.__dict__ = copy.deepcopy(wasset.__dict__)
            filename = wasset._filename

            comment = 'Updated with AssetAction\n' + 'Source:' + filename
            thumb_src = assetutils.Asset.thumbnail_filepath(filename, asset.version, replace_share_root=False)
            
            tmp_output = assetutils.get_publish_tempfilename(filename)

            args = {
                'export_all': True, 
                'export_only': False,
                'submit_server': True,
                'postproc': [postproc_utils.find_proc_by_name('postproc_update_assets', plugin_type=PluginType.PublishPostProcess)], 
                'preproc': [],
                'procs': [], 
                'user': p4user,
                'commit_to_engine': False,
                'keep_intermediate': False,
                'thumbnail_source': thumb_src, 
                'is_custom_task': True,
                'tmp_output': tmp_output,
                'deadline_batchname': deadline_batchname,
                'comment':comment,
                'work_asset': wasset,
            }
            
            wfile = {'share_filepath':filename, 'version':asset.version}
            
            task = wcmds.PublishTask(asset, asset._tags, wfile, comment, args)
            res = task.execute(silent=True)
            if task.last_deadline_jobid is not None:
                deps.append(task.last_deadline_jobid)
            asset_filenames.append((filename, wasset))

        register_notif_job(deps, deadline_batchname, comment, asset_filenames)

        #
        from workfile_manager.ui import uiutils
        uiutils.PromptDialog('Confirmation', u'ワークファイルアップデートジョブを投げました。', btns=['OK']).exec_()

    

def register_notif_job(deps, deadline_batchname, comment, asset_filenames):
    from workfile_manager_maya import assetutils_maya
    from cypyapiutils import envutils
    envutilspath = os.path.dirname(envutils.__file__).replace('\\', '/')

    share_asset = assetutils_maya.ModelAssetMaya()

    args = {}
    env = envutils.save(os.path.dirname(assetutils.get_publish_tempfilename('update_assets.yaml')))
    print('envfile: ', env)
    args['envfile'] = env
    args['deadline_batchname'] = deadline_batchname

    args['export_module_name'] = 'workman_world_custom.asset_actions.all.update_assets'
    args['postproc'] = []
    args['is_custom_task'] = True
    args['comment'] = comment
    args['user'] = p4u.user
    args['asset_filenames'] = asset_filenames

    rargs = {}
    cmd = share_asset.get_postproc_cmd(None, args)
    print ('pycmd: ', cmd.replace('/', '\\'))

    rargs['command'] = cmd
    rargs['cyclops_app_name'] = os.environ['WM_MAYA_APP']
    rargs['app_version'] = os.environ['WM_MAYA_APP_VERSION']
    rargs['deps'] = deps
    if 'deadline_batchname' in args:
        rargs['deadline_batchname'] = args['deadline_batchname']

    #
    from workfile_manager import deadline_submit as dls
    tool_dir = 'W:/production/tools'
    batchfile = '%s/projects/world/inhouse/win/extension/maya/share/packages/workfile_manager_maya/%s/python/workfile_manager_maya/export/post_fbx_export.bat' % (tool_dir, os.environ['WORKFILE_MANAGER_MAYA_VERSION'])
    package_version = '""'
    info = {'name':'Notification', 'username':p4u.p4.user, 'task':share_asset.task, 'comment':'Notificate when updating done.'}
    dls.submit(info, envutilspath, env, batchfile, rargs, package_version, share_asset, app=Application.Maya)   



def postfunc(presetname=None, argfile=None):
    try:
        execute_notification(presetname, argfile)
    except:
        import traceback
        print(traceback.format_exc())
        import sys
        sys.exit(1)

def execute_notification(presetname=None, argfile=None):
    from workfile_manager_maya import assetutils_maya
    from workfile_manager import dbutils
    from cylibassetdbutils import tag_tree
    from workfile_manager import cmds as wcmds

    args = wcmds.yaml_load(argfile)

    asseturls = []
    for master, asset in args['asset_filenames']:
        asset.version = None
        try:
            print('>>> asset_dict:', asset.get_dict())
            print('>>> master: ', master)
            print('>>> asset: ', asset)
            asseturl = asset.get_url(master)
            print('>>> asseturl: ', asseturl)
        except:
            import traceback
            print(traceback.format_exc())
            asseturls.append(master.replace('/', '\\'))
        else:
            asseturls.append(asseturl)

    message = u'アップデートが完了しました。\n' + \
        u'*コメント*\n```' + args['comment'] + '```\n' + \
        u'*出力アセット*\n```' +'\n'.join(asseturls) + '```\n'
    
    from workfile_manager import notification
    notification.send_to_slack(message, args['user'])
