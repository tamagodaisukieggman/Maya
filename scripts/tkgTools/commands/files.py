# -*- coding: utf-8 -*-
import maya.cmds as cmds

import codecs
import fnmatch
import json
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

def remove_namespace():
    while True:
        all_namespace = cmds.namespaceInfo(listOnlyNamespaces=True)
        li_uniq = list(set(all_namespace))
        nums = len(li_uniq)
        if nums == 2:
            break
        else:
            for i in range(nums):
                if li_uniq[i] != "UI" and li_uniq[i] != "shared":
                    cmds.namespace(mergeNamespaceWithParent=True, removeNamespace=li_uniq[i])

def json_transfer(file_name=None, operation=None, export_values=None):
    u"""
    param:
        file_name = 'file_path'
        operation = 'import' or 'export'
        export_values = dict

    dict = json_transfer(file_name, 'import')
    json_transfer(file_name, 'export', dict)
    """
    encodings = ["utf-8", "shift_jis", "iso-2022-jp", "euc-jp"]
    if operation == 'export':
        try:
            with codecs.open(file_name, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)
        except:
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)

    elif operation == 'import':
        for encoding in encodings:
            try:
                with codecs.open(file_name, 'r', encoding=encoding) as f:
                    return json.load(f, encoding, object_pairs_hook=OrderedDict)
            except:
                with open(file_name, 'r', encoding=encoding) as f:
                    return json.load(f, object_pairs_hook=OrderedDict)

def import_fbx(fbx_path=None, nss=None, new_scene=None):
    if new_scene: cmds.file(new=True, f=True)

    if not cmds.namespace(ex=nss): cmds.namespace(add=nss)
    cmds.namespace(set=nss)

    basename_without_ext = os.path.splitext(os.path.basename(fbx_path))[0]
    cmds.file(
        fbx_path,
        i=True,
        type='FBX',
        ignoreVersion=True,
        mergeNamespacesOnClash=False,
        pr=True,
        importTimeRange='override',
        importFrameRate=True,
        ra=True,
        namespace=basename_without_ext
    )

    cmds.namespace(set=':')

    nss = nss + ':'
    return cmds.ls('{}*'.format(nss), type='transform')

def find_files(directory=None, pattern=None, exact=None):
    for root, dirs, files in os.walk(directory):
        if root.endswith(exact):
            continue
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename
