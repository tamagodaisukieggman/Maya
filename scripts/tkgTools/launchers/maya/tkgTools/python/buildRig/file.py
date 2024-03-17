# -*- coding: utf-8 -*-
import codecs
from collections import OrderedDict
from imp import reload
import json
import os
import re
import sys

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
    def __init__(self, setup_env_path=None):
        self.setting_dict = OrderedDict()

        self.setup_env_path = setup_env_path

        DATA_PATH = DIR_PATH + '/data'
        if self.setup_env_path:
            self.setting_json = self.setup_env_path + '/setting.json'
        else:
            self.setting_json = DATA_PATH + '/setting.json'

        # self.default_settings()

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
        self.setting_dict['RIGGRPS'] = OrderedDict()
        self.setting_dict['FK'] = OrderedDict()
        self.setting_dict['IK'] = OrderedDict()
        self.setting_dict['ROOT'] = OrderedDict()

        rig_grps_names = {
            'grps':['CHAR', 'MODEL', 'RIG', 'SKEL'],
        }

        ik_fk_names = {
            'offsets':['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV'],
            'ctrl':['', '', ['_CURVE', '_CTRL']],
            'colors':{
                'center':{
                    'value':[1.0, 1.0, 0],
                    'filter':['center*', 'C_*', '*_C']
                },
                'left':{
                    'value':[1.0, 0.214, 0.214],
                    'filter':['left*', 'L_*', '*_L']
                },
                'right':{
                    'value':[0.421, 0.421, 0.796],
                    'filter':['right*', 'R_*', '*_R']
                },
                'other':{
                    'value':[0.7, 0.7, 0.1],
                    'filter':['']
                }
            }
        }

        root_names = {
            'offsets':['GRP', 'OFFSET', 'SPACE', 'MOCAP', 'DRV'],
            'ctrl':['', '', ['_CURVE', '_CTRL']],
            'colors':{
                'global':{
                    'value':[0.199, 0.108, 0.315],
                    'filter':['*Global*']
                },
                'local':{
                    'value':[0.069, 0.377, 0.694],
                    'filter':['*Local*']
                },
                'root':{
                    'value':[1.0, 1.0, 0.24],
                    'filter':['*Root*']
                }
            }
        }

        for type, name_settings in self.setting_dict.items():
            if type in ['RIGGRPS']:
                for n, nv in rig_grps_names.items():
                    name_settings[n] = nv
            elif type in ['FK', 'IK']:
                for n, nv in ik_fk_names.items():
                    name_settings[n] = nv
            elif type in ['ROOT']:
                for n, nv in root_names.items():
                    name_settings[n] = nv


class Files:
    """
    files = Files(ref_path, 'chr', 'reference')
    file_objects = files.file_execute()
    top_nodes = files.get_top_nodes()
    """
    def __init__(self, path=None, namespace=None, mode='reference'):
        self.namespace = namespace
        self.path = path
        self.mode = mode

        self.reference_sts = None
        self.import_sts = None

        self.options = {}

        self.file_objects = None
        self.top_nodes = []

        self.set_options()

    def set_options(self):
        if self.mode == 'reference':
            self.reference_sts = True
            self.import_sts = False
        elif self.mode == 'import':
            self.reference_sts = False
            self.import_sts = True

        self.options = {
            'ignoreVersion':True,
            'namespace':self.namespace,
            'reference':self.reference_sts,
            'import':self.import_sts,
            'gl':True,
            'mergeNamespacesOnClash':True,
            'returnNewNodes':True,
            'options':'v=0;'
        }

    def file_execute(self):
        self.file_objects = cmds.file(self.path, **self.options)
        return self.file_objects

    def get_top_nodes(self):
        self.top_nodes = []
        for f_obj in self.file_objects:
            if '|' in f_obj:
                self.top_nodes.append(f_obj.split('|')[1])
        self.top_nodes = list(set(self.top_nodes))
        return self.top_nodes

class Plugins:
    def __init__(self, plugins=None):
        self.plugins = plugins
        self.plugin_results = {}

    def load(self):
        for plugin in self.plugins:
            plugin_result = cmds.loadPlugin(plugin) if not cmds.pluginInfo(plugin, q=True, l=True) else False
            self.plugin_results[plugin] = plugin_result

        function_name = sys._getframe().f_code.co_name
        sys.stdout.write('{}: {}: {}\n'.format(self.__class__.__name__, function_name, self.plugin_results))
        sys.stdout.flush()

# plugins = Plugins(plugins=[
#     'Type',
#     'fbxmaya',
#     'lookdevKit'
#     ])
# plugins.load()
