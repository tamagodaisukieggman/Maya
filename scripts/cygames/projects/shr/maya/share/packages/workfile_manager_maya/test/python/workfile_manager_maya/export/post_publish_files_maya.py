# -*- coding: utf-8 -*-
from __future__ import print_function, annotations
import copy
import subprocess
import yaml
import os
import shutil
import re

from workfile_manager import dccutils, p4utils
from cylibassetdbutils import assetdbutils, assetutils

try:
    import maya.cmds as cmds
    from workfile_manager_maya.export import post_publish_files_maya_slave as pfe_maya
    from postproc_set_editor_maya import ui_maya
    from workfile_manager_maya import assetutils_maya
except:
    pass

import publish_files.ui

db = assetdbutils.DB.get_instance()
p4u = p4utils.P4Utils.get_instance()
dcccmds = ui_maya.DccCmds()


def find_part_set(part) -> str|None:
    """
    開いているシーン内の指定した名前のPostPorcessEditSet（ObectSet）のノード名を返す
    """
    for setname in dcccmds.list_node_names(type='objectSet'):
        try:
            setlabel = dcccmds.get_attr(setname+'.postproc_edit_set__name')
            if setlabel == part:
                return setname
        except Exception as e:
            print (e)
            continue

    return None


def postfunc(presetname=None, inputfile=None, argfile=None):
    from publish_files import publish_window
    from postproc_set_editor import post_process_operator
    from workfile_manager import cmds as wcmds
    import publish_files

    with open(argfile) as _argfile:
        args = wcmds.yaml_load(_argfile)

    pid = args['process_id']
    maxproc = args['num_groups']

    maya_jobs = []
    
    for work_file_order, original_work_file in enumerate(args['target_files'][pid::maxproc]):
        work_file_index = pid + work_file_order
        outfile = assetutils.get_publish_tempfilename_local(original_work_file)
        _dir = os.path.dirname(outfile)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        
        try:
            assetutils_maya.cached_share_safe_open(original_work_file)
        except Exception as e:
            print(e, flush=True)

        dcc_cmds = ui_maya.DccCmds()
        dcc_utils = assetutils_maya.MayaUtils.get_instance()
        publish_files.import_default_presets(dcc_cmds, dcc_utils, args, original_work_file, outfile)

        workasset_dict = publish_window.get_workasset(original_work_file)

        override_commit_output = None
        if workasset_dict is None:
            from wmutils import config
            config_ = config.Config.get_instance()
            workasset_dict = copy.deepcopy(config_.get('publish_files_tmp_asset').value())
            workasset_dict['local_master_path'] = original_work_file
            override_commit_output = os.path.join(os.path.dirname(original_work_file), 'export', os.path.basename(original_work_file))
            override_commit_output = override_commit_output[:override_commit_output.rindex('.')] + '.fbx'
            override_commit_output = assetdbutils.normalize_path(override_commit_output)

        work_asset = assetutils_maya.WorkAssetMaya()
        work_asset.copy_parameters_from_dict(workasset_dict)
        print('work_asset: ', work_asset.get_dict(), flush=True)

        share_asset = assetutils_maya.AnimationAssetMaya()
        share_asset.copy_parameters_from_dict(workasset_dict)
        print('share_asset: ', share_asset.get_dict(), flush=True)

        _tags = db.get_assigned_tags(work_asset)
        tags = [(x['tag_type'], x['name']) for x in _tags]
        print('tags: ', tags, flush=True)

        print('publish_parts_parts:', args['publish_parts_parts'], flush=True)

        for part in args['publish_parts_parts']:
            setname = find_part_set(part)
            if setname is None:
                print('Not found. Skipping.')
                continue

            job = {}
            job['publish_parts_parts'] = [part]
            job['specified'] = [part]
            job['inputfile'] = outfile
            job['original_work_file'] = original_work_file
            job['workfile_fully_synced'] = args['workfile_fully_synced_list'][work_file_index]
            
            try:
                target_set = [x for x in cmds.ls(cmds.sets(setname, q=True), type='objectSet') if x.endswith('_target')][0]
                buf = cmds.sets(target_set, q=True)
                if buf is not None:
                    job['selection'] = buf
            except:
                pass # ignore if target set not specified.
            

            tmpoutfile = assetutils.get_publish_tempfilename_local(os.path.basename(outfile))
            job['outfile'] = tmpoutfile

            job['share_asset'] = share_asset.get_dict()

            source_file_info = {'local_master_path':workasset_dict['local_master_path'], 'version':workasset_dict['version']}
            job['source_file_info'] = source_file_info
            job['tags'] = tags
            job['pid'] = pid

            job['include_publish_operator'] = post_process_operator.does_set_include_publish_op(part, dcccmds)

            if job['include_publish_operator']:
                from workman_shenron_custom.asset_actions.maya import publish_parts_base_maya
                if original_work_file.endswith('.ma'):
                    tmpfile = publish_parts_base_maya.convert_ma_to_cgkit_readable(original_work_file)
                    job['frame_range'] = publish_files.ui.get_maximum_framerange(tmpfile, publish_parts_base_maya.MAReader)
                else:
                    job['frame_range'] = publish_files.ui.get_maximum_framerange(original_work_file, publish_parts_base_maya.MBReader)
            else:
                job['frame_range'] = assetutils_maya.MayaUtils.get_instance().get_framerange()

            if override_commit_output is not None:
                job['override_commit_output'] = override_commit_output

            maya_jobs.append(job)

    args['maya_jobs'] = maya_jobs

    _argfile = publish_files.ui.export_argfile(args, pid)

    
    try:
        pfe_maya.postfunc(argfile=_argfile)
    except Exception as e:
        import traceback
        print(traceback.format_exc(), flush=True)
    
    for maya_job in maya_jobs:
        tmpfile = maya_job['outfile']
        if os.path.exists(tmpfile):
            os.remove(tmpfile)
        tmpfbx = re.sub('[.][^.]*$', '.fbx', tmpfile)
        if os.path.exists(tmpfbx):
            os.remove(tmpfbx)


    
