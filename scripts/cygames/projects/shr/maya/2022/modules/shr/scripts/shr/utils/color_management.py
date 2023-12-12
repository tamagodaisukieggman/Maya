import os
from maya import cmds

OCIO_CONFIG_PATH = 'C:/cygames/shrdev/shr/tools/in/lib/ocio/shenron/config.ocio'
XML_FILE_PATH = 'C:/cygames/shrdev/shr/tools/in/lib/ocio/Maya2022-default/20221021.xml'
PROJECT_COLOR_SPACE = 'sRGB'

_color_management_coms = {
    "cmEnabled":                          True,
    "configFilePath":                     OCIO_CONFIG_PATH,
    "cmConfigFileEnabled":                True,
    "colorManagePots":                    True,
    "ocioRulesEnabled":                   False,
    "outputTransformEnabled":             False,
    "outputTransformName":                'Un-tone-mapped (sRGB)',
    "outputTransformUseColorConversion":  False,
    "outputUseViewTransform":             True,
    "renderingSpaceName":                 'scene-linear Rec.709-sRGB',
    "viewName":                           'Un-tone-mapped',
    "viewTransformName":                  'Un-tone-mapped (sRGB)',
    "policyFileName":                     '',
    }

_color_management_coms = {
    "cmEnabled":                          False,
    "policyFileName":                     '',
    }

# XML 設定用、inputcolormanegement の設定ができずにエラーとなる場合があるのでオミット
# _color_management_coms = {
#     "cmEnabled":                          True,
#     "policyFileName":                     XML_FILE_PATH,
# }

def set_file_rule():
    rules = cmds.colorManagementFileRules(listRules=True)
    if PROJECT_COLOR_SPACE not in rules:
        cmds.colorManagementFileRules(
                                add=PROJECT_COLOR_SPACE,
                                pattern='*',
                                extension='tga',
                                colorSpace=PROJECT_COLOR_SPACE)


class ColorManagement:
    @classmethod
    def _enable_color_management(self):
        cmds.colorManagementPrefs(refresh=True)
        for _com, _value in _color_management_coms.items():
            _q_command = f'print(cmds.colorManagementPrefs(q=True, {_com}=True))'
            # print(f'-- {"befor color management":}')
            # exec(_q_command)
            if isinstance(_value, str):
                _command = f'cmds.colorManagementPrefs(e=True, {_com}="{_value}")'
            else:
                _command = f'cmds.colorManagementPrefs(e=True, {_com}={_value})'
            exec(_command)
        set_file_rule()

    @classmethod
    def __enable_color_management_old(self):
        _config_file_path = cmds.colorManagementPrefs(q=True, configFilePath=True).replace(os.sep, '/')
        _xml_file_path = cmds.colorManagementPrefs(q=True, policyFileName=True).replace(os.sep, '/')
        cmds.colorManagementPrefs(edit=True, cmEnabled=True)
        cmds.colorManagementPrefs(edit=True, cmConfigFileEnabled=True)
        cmds.colorManagementPrefs(colorManageAllNodes=True)

        cmds.colorManagementPrefs(edit=True, configFilePath=OCIO_CONFIG_PATH)
        cmds.colorManagementPrefs(edit=True, policyFileName="")
