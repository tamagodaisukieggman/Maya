# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import pymel.core as pm

import codecs
from collections import OrderedDict
import datetime
import json
import os
import sys
import traceback

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance

class TkgUtils(object):
    def __init__(self):
        pass

    @classmethod
    def get_currentSceneInfo(cls):
        u"""現在のファイルのパスを取得

        :return filepath, filename, raw_name, extension
        """
        cls.filepath = cmds.file(q=True, sn=True) or None
        if cls.filepath:
            cls.filename = os.path.basename(cls.filepath) or None
            if cls.filename:
                cls.raw_name, cls.extension = os.path.splitext(cls.filename)
        else:
            return None, None, None, None

        return cls.filepath, cls.filename, cls.raw_name, cls.extension

    def allreferences_uncheck_remove(self, sts=None, removeAt=None):
        u"""
        'RNode'
        'namespace'
        'filename'
        'w_filenam'
        'isLoaded'
        'nodes'
        'node'
        """

        ref_info = get_reference_info()
        for ref in ref_info:
            ref_node = ref['RNode']
            ref_filename = ref['filename']
            if sts == 'uncheck':
                cmds.file(ur=ref_node)
                cmds.file (cr=ref_node)

            elif sts == 'check':
                cmds.file(lr=ref_node)
                cmds.file (cr=ref_node)

            elif sts == 'remove':
                cmds.file(ref_filename, rr=1)

            elif sts == 'removeEdits':
                refEdits = cmds.referenceQuery(ref_node, ea=1, en=1)
                for editAt in refEdits:
                    cmds.referenceEdit(editAt, failedEdits=True, successfulEdits=True, editCommand=removeAt, removeEdits=1)

    def importAllReferences(self):
        u"""Referenceをすべてインポートします"""
        print("Importing all references...")
        done = False
        while (done == False and (len(pm.listReferences()) != 0)):
            refs = pm.listReferences()
            print("Importing " + str(len(refs)) + " references.")
            for ref in refs:
                if ref.isLoaded():
                    done = False
                    ref.importContents()
                else:
                    done = True
        print("Done importing references...")
        return True

    def remove_all_namespace(self):
        u"""Namespaceをすべて削除します"""
        cmds.namespace(setNamespace=':')
        for ns in reversed(cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)):
            if ns != 'UI' and ns != 'shared':
                cmds.namespace(moveNamespace=(ns, ':'), force=True)
                cmds.namespace(removeNamespace=ns)

    def remove_CgAbBlastPanelOptChangeCallback(self):
        for item in pm.lsUI(editors=True):
           if isinstance(item, pm.ui.ModelEditor):
               pm.modelEditor(item, edit=True, editorChanged="")

    def re_file_open(self):
        if cmds.file(q=1, sn=1):
            cmds.file(cmds.file(q=1, sn=1), o=1, f=1)

def get_reference_info():
    ret = []

    refNodes = cmds.ls(references=True)
    for RNnode in refNodes:
        ref = {}
        ref.update({
            'RNode'    : RNnode,
            'namespace' : cmds.referenceQuery(RNnode, namespace=True),
            'filename'   : cmds.referenceQuery(RNnode, filename=True),
            'w_filenam' : cmds.referenceQuery(RNnode, filename=True, withoutCopyNumber=True),
            'isLoaded'  : cmds.referenceQuery(RNnode, isLoaded=True),
            'nodes'     : cmds.referenceQuery(RNnode, nodes=True),
            'node'      : cmds.referenceQuery(RNnode, nodes=True)[0],
            })
        ret.append(ref)

    return ret

def grabViewport(filePath):
    viewport = omui.M3dView.active3dView()
    viewport.refresh()
    img = om.MImage()
    img.create(1920, 1080)
    viewport.readColorBuffer(img, True)
    ext = filePath.split('.')[1]
    img.writeToFile(filePath, ext)

def capture():
    # savepath = cmds.fileDialog2(ds=2, cap='ScreenShot', ff='All Files (*.*);;*.bmp;;*.jpg;;*.png;;*.tif;;*.gif;;*.iff;;*.psd', fm=0)
    # if not savepath:
    #     return
    # else:
    #     savepath = savepath[0]

    # print('Saved "{}"'.format(savepath))

    if os.name == 'nt':
        home = os.getenv('USERPROFILE')
    else:
        home = os.getenv('HOME')
    desktop_dir = os.path.join(home, 'Desktop')

    today_time = datetime.datetime.today()
    today_time_str = today_time.strftime("%Y%m%d_%H%M%S")
    filename = today_time_str + '.png'
    savepath = desktop_dir + '/' + filename

    grabViewport(savepath)

def default_snap():
    mel.eval('GoToDefaultView;')

    camera_shs = cmds.ls(type='camera')
    cameras = []
    for camera_sh in camera_shs:
        camera_pa = cmds.listRelatives(camera_sh, p=True) or list()
        if camera_pa:
            cameras.append(camera_pa[0])

    top_nodes = [node for node in cmds.ls(assemblies=True) if not node in cameras]
    cmds.select(top_nodes)

    cmds.setAttr('perspShape.focalLength', 150)

    mel.eval('FrameSelectedWithoutChildren;')

    cmds.select(cl=True)

    panel = cmds.getPanel(withFocus=True)

    cmds.modelEditor(panel, e=True, hud=False)

    capture()

    cmds.modelEditor(panel, e=True, hud=True)

def replace_clipboard_path():
    clipboard = QClipboard()
    text = clipboard.text().replace('\\', '/')
    clipboard.setText(text)
    return text

class JsonFile(object):
    @classmethod
    def read(cls, file_path):
        if not file_path:
            return {}

        if not os.path.isfile(file_path):
            return {}

        with codecs.open(file_path, 'r', 'utf-8') as f:
            try:
                data = json.load(f, object_pairs_hook=OrderedDict)
            except ValueError:
                data = {}

        return data

    @classmethod
    def write(cls, file_path, data):
        if not file_path:
            return

        dirname, basename = os.path.split(file_path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        with codecs.open(file_path, 'w', 'utf-8') as f:
            json.dump(data, f, indent=4)
            f.flush()
            os.fsync(f.fileno())
