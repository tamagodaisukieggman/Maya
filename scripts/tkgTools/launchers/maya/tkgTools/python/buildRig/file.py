# -*- coding: utf-8 -*-
import codecs
from collections import OrderedDict
from imp import reload
import json
import os
import re

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2

import buildRig.common as brCommon
reload(brCommon)

try:
    DIR_PATH = '/'.join(__file__.replace('\\', '/').split('/')[0:-1])
except:
    DIR_PATH = ''

class Settings:
    """
from imp import reload
import re
import traceback

import maya.cmds as cmds
import maya.mel as mel

import buildRig.file as brFile
reload(brFile)

settings = brFile.Settings()
settings.default_settings()
settings.export_settings()
    """
    def __init__(self):
        self.setting_dict = OrderedDict()
        self.setting_dict['FK'] = OrderedDict()
        self.setting_dict['IK'] = OrderedDict()

        DATA_PATH = DIR_PATH + '/data'
        self.setting_json = DATA_PATH + '/setting.json'

        self.default_settings()

        if not os.path.isdir(DATA_PATH):
            os.makedirs(DATA_PATH)

        if not os.path.isfile(self.setting_json):
            self.export_settings()

        elif os.path.isfile(self.setting_json):
            self.import_settings()

    def export_settings(self):
        brCommon.json_transfer(self.setting_json, 'export', self.setting_dict)

    def import_settings(self):
        self.setting_dict = brCommon.json_transfer(self.setting_json, 'import')

    def default_settings(self):
        names = {
            'offsets':['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV'],
            'ctrl':['', '', ['_CURVE', '_CTRL']],
            'colors':{
                'center':{
                    'value':[1.0, 1.0, 0],
                    'filter':['center', 'C_*', '*_C']
                },
                'left':{
                    'value':[1.0, 0, 0],
                    'filter':['left', 'L_*', '*_L']
                },
                'right':{
                    'value':[0, 0, 1.0],
                    'filter':['right', 'R_*', '*_R']
                },
                'other':{
                    'value':[0.5, 0.5, 0.8],
                    'filter':['']
                }
            }
        }

        for type, name_settings in self.setting_dict.items():
            for n, nv in names.items():
                name_settings[n] = nv
