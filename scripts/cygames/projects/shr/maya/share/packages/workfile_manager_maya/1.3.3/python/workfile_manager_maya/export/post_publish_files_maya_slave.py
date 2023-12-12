# -*- coding: utf-8 -*-
from __future__ import print_function
import copy
import os
import subprocess
import re

from workfile_manager import p4utils, postproc_utils
from workfile_manager_maya.export import post_fbx_export as pfe_maya
from cylibassetdbutils import assetdbutils
import publish_files.ui

db = assetdbutils.DB.get_instance()
p4u = p4utils.P4Utils.get_instance()

def postfunc(presetname=None, inputfile=None, argfile=None):
    from workfile_manager import cmds as wcmds
    with open(argfile) as _argfile:
        args = wcmds.yaml_load(_argfile)

    maya_jobs = args['maya_jobs']

    logfile = args['logfile'] if 'logfile' in args else None

    for maya_job in maya_jobs:
        _args = copy.deepcopy(args)
        _args['dont_launch_new_app'] = True
        _args['export_module_name'] = 'workfile_manager_maya.export.post_fbx_export'
        _args['is_custom_task'] = True if maya_job['include_publish_operator'] else False
        _args['from_publish_files'] = True
        #child_pp = postproc_utils.find_proc_by_name('postproc_edit_set', plugin_type=postproc_utils.PluginType.PublishPostProcess)
        #_args['postproc'] = [child_pp]
        
        pid = maya_job['pid']
        for k in maya_job:
            _args[k] = maya_job[k] # may override 'dont_launch_new_app'

        _argfile = publish_files.ui.export_argfile(_args, pid)

        try:
            pfe_maya.postfunc(presetname='animation.fbxexportpreset', argfile=_argfile)
        except:
            publish_files.ui.output_log(logfile, 'ERROR: Maya: '+_args['inputfile'].replace('/', '\\'))
        else:
            publish_files.ui.output_log(logfile, 'SUCCESS: Maya: '+_args['inputfile'].replace('/', '\\'))


    for maya_job in maya_jobs:
        files = [maya_job['inputfile'], maya_job['outfile'], re.sub('[.][^.]+$', '.ma', maya_job['outfile'])]
        for f in files:
            if os.path.exists(f):
                try:
                    subprocess.call('attrib -R "%s"' % f)
                    os.remove(f)
                except:
                    import traceback
                    print(traceback.format_exc(), flush=True)
                    print('Failed in deleting: ', f, flush=True)
        
    


    
