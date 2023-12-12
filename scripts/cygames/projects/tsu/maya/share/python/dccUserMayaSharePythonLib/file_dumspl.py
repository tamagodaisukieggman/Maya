# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : dccUserMayaSharePythonLib.file_dumspl
# Author  : toi
# Version : 0.0.3
# Update  : 2020/12/7
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import sys
import time
import json
import stat
import glob
from functools import partial
from collections import OrderedDict

try:
    import maya.cmds as cmds
except ImportError:
    pass


def settingDir(dir_name):
    return os.path.join(
        os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"),
        'Documents', 'maya', 'Scripting_Files', dir_name)


def getAllFiles(target_dir, search_files_in_folder=False):
    path_ = target_dir
    if search_files_in_folder:
        file_list = []
        for root, dirs, files in os.walk(path_):
            for f in files:
                file_list.append(os.path.join(root, f))
    else:
        file_list = [x for x in glob.glob(target_dir + '/*') if os.path.isfile(x)]
    return file_list


# --------------------------------------------------------------------------------
# json
# --------------------------------------------------------------------------------
def exportJson(path_=r'', dict={}):
    if not os.path.isdir(os.path.dirname(path_)):
        os.makedirs(os.path.dirname(path_))
    f = open(path_, 'w')
    json.dump(dict, f, indent=4)
    f.close()


def importJson(path=r''):
    f = open(path, 'r')
    tmp = f.read()
    res = json.loads(tmp, object_pairs_hook=OrderedDict)
    f.close()
    return res


class JsonDict(object):
    def __init__(self, json_path):
        self.json_path = json_path
        if not os.path.isfile(json_path):
            exportJson(json_path)
        self._dict = importJson(json_path)

    def get(self, key, default_val=''):
        self._dict.setdefault(key, default_val)
        return self._dict[key]

    def set(self, key, val):
        self._dict[key] = val
        exportJson(self.json_path, self._dict)


def getSettingFilePath(file_name):
    return os.path.join(
        os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"),
        'Documents', 'maya', 'Scripting_Files', file_name)


def createSettingFile(file_name):
    setting_json = os.path.join(getSettingFilePath(file_name), file_name + '.json')
    if not os.path.isfile(setting_json):
        exportJson(setting_json)
    return JsonDict(setting_json)


# --------------------------------------------------------------------------------
def importFbx(fbx_path, ns=''):
    cmds.file(fbx_path, f=True, i=True, namespace=ns)


def exportFbx(path=r''):
    cmds.file(path, f=True, op='v=0;', typ='FBX export', pr=True, ea=True)