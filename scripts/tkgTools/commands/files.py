# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os

def reference_fbx(path=None, namespace=None):
    if path and namespace:
        if os.path.isfile(path):
            cmds.file(
                path,
                namespace=namespace,
                r=True,
                type='FBX',
                ignoreVersion=True,
                gl=True,
                mergeNamespacesOnClash=False,
            )

def get_reference_info():
    ret = []
    ret_no_files = OrderedDict()

    refNodes = cmds.ls(references=True)
    for RNnode in refNodes:
        ref = {}
        file_name = cmds.referenceQuery(RNnode, filename=True, failedEdits=True)
        if os.path.isfile(file_name):
            ref.update({
                'namespace' : cmds.referenceQuery(RNnode, namespace=True, failedEdits=True),
                'filename'   : cmds.referenceQuery(RNnode, filename=True, failedEdits=True),
                'w_filenam' : cmds.referenceQuery(RNnode, filename=True, withoutCopyNumber=True, failedEdits=True),
                'isLoaded'  : cmds.referenceQuery(RNnode, isLoaded=True, failedEdits=True),
                'nodes'     : cmds.referenceQuery(RNnode, nodes=True, failedEdits=True),
                'node'      : cmds.referenceQuery(RNnode, nodes=True, failedEdits=True),
                })
            ret.append(ref)

        else:
            ret_no_files[RNnode.replace('RN', '')] = file_name

    return ret, ret_no_files
