from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path
import yaml
import os
import maya.cmds as cmds

from .. import gui_util

HERE = Path(os.path.dirname(os.path.abspath(__file__)))
YAML_FILE_NAME = "houdini_engine_settings.yaml"

HOUDINI_ENGINE_PLUGIN_NAME = "houdiniEngine"
HOUDINI_ENGINE_PLUGIN_EXT = ".mll"

_SafeModeAllowedlistPaths = "SafeModeAllowedlistPaths"
_TrustCenterPathAction = "TrustCenterPathAction"


class HoudiniEngineMaya:
    def __init__(self, prg:gui_util.ProgressDialog) -> None:
        maya_version = cmds.about(version=True)
        self.maya_version = maya_version.split(" ")[0]
        self.prg = prg
        self.prg_num = 1
        self.houdini_engine_config = self._load_yaml_data()
        self.houdini_engine_timeout = self.houdini_engine_config["HOUDINI_ENGINE_TIMEOUT"]
        self.houdini_version = self.houdini_engine_config["HOUDINI_VERSION"]
        self.houdini_sub_version = self.houdini_engine_config["HOUDINI_SUB_VERSION"]
        self.project_houdini_version = f'{self.houdini_version}.{self.houdini_sub_version}'
        self.houdini_engine_plugin_name = f'{HOUDINI_ENGINE_PLUGIN_NAME}{HOUDINI_ENGINE_PLUGIN_EXT}'
        self._set_option_var()

    def _num(self):
        self.prg.step(self.prg_num)
        self.prg_num += 1

    def _load_yaml_data(self) -> dict:
        with open(HERE / YAML_FILE_NAME, encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config

    def _set_option_var(self) -> None:
        if cmds.optionVar(q="houdiniEngineSessionType") != 2:
            cmds.optionVar(intValue=["houdiniEngineSessionType", 2])
        if cmds.optionVar(q="houdiniEngineSessionPipeCustom") != 0:
            cmds.optionVar(intValue=["houdiniEngineSessionPipeCustom", 0])
        if cmds.optionVar(q="houdiniEngineThriftPipe") != "hapi":
            cmds.optionVar(stringValue=["houdiniEngineThriftPipe", "hapi"])
        if cmds.optionVar(q="houdiniEngineAsynchronousMode") != 0:
            cmds.optionVar(intValue=["houdiniEngineAsynchronousMode", 0])
        cmds.optionVar(intValue=["houdiniEngineTimeout", self.houdini_engine_timeout])

    def check_houdini_exe_path(self) -> str:
        self._num()
        _result = ''
        houdini_exe_path = Path(self.houdini_engine_config["HOUDINI_PATH"])
        self.houdini_exe_path = houdini_exe_path / f'Houdini {self.houdini_version}.{self.houdini_sub_version}/bin'
        if not self.houdini_exe_path.exists():
            _result = self.houdini_exe_path
        return _result

    def check_houdini_engine_script_path(self) -> str:
        self._num()
        _result = ''
        houdini_engine_path = Path(self.houdini_engine_config["HOUDINI_ENGINE_PATH"])
        houdini_engine_path_script = houdini_engine_path / f'maya{self.maya_version}' / 'scripts'
        self.houdini_engine_script_path = houdini_engine_path_script
        if not houdini_engine_path_script.exists():
            _result = self.houdini_engine_script_path
        return _result

    def check_houdini_engine_path(self) -> str:
        self._num()
        _result = ''
        houdini_engine_path = Path(self.houdini_engine_config["HOUDINI_ENGINE_PATH"])
        houdini_engine_path = houdini_engine_path / f'maya{self.maya_version}' / 'plug-ins'
        self.houdini_engine_path = houdini_engine_path
        self.houdini_engine_plugin = houdini_engine_path / f'{HOUDINI_ENGINE_PLUGIN_NAME}{HOUDINI_ENGINE_PLUGIN_EXT}'

        if not self.houdini_engine_plugin.exists():
            _result = self.houdini_engine_plugin
        return _result

    def check_hda_path(self) -> str:
        self._num()
        _result = ''
        self.hda_path = Path(self.houdini_engine_config["HDA_PATH"])
        if not self.hda_path.exists():
            _result = self.hda_path
        return _result

    def add_path(self) -> None:
        self._num()
        env_paths = {
                'PATH': self.houdini_exe_path,
                'MAYA_PLUG_IN_PATH': self.houdini_engine_path,
                'MAYA_SCRIPT_PATH': self.houdini_engine_script_path,
                }

        for env, env_path in env_paths.items():
            path_string = os.environ.get(env, None)
            env_path = str(env_path)

            # if not path_string:
            #     continue

            _path_exists = env_path in path_string.split(";")
            print(f'[ BeforSetting] [ EXISTS: {_path_exists} ] [ ENV: {env:<20} ] [ ENV PATH: {env_path} ]')

            if not _path_exists:
                os.environ[env] = f'{path_string};{env_path}'

                path_string = os.environ.get(env, None)
                _path_exists = env_path in path_string.split(";")
                print(f'[ AfterSetting] [ EXISTS: {_path_exists} ] [ ENV: {env:<20} ] [ ENV PATH: {env_path} ]')
        self._set_default_trust()
        self._set_trust_path()

    def _set_default_trust(self) -> None:
        """untrust location のデフォルト動作を変更
        ただしこれを行ってもダイアログは表示される
        """
        self._num()
        _option_value = {"Ask for Permission":  1,
                        "Deny":                 2}

        _value = cmds.optionVar(q=_TrustCenterPathAction)
        _str_value = [k for k,v in _option_value.items()if v==_value]

        print(f'[ Untrust location setting: {_str_value} ]')
        if cmds.optionVar(q=_TrustCenterPathAction) != _option_value["Deny"]:
            cmds.optionVar(intValue=[_TrustCenterPathAction, _option_value["Deny"]])
            _value = cmds.optionVar(q=_TrustCenterPathAction)
            print(f'[ Change untrust location setting --- {_value} ]')

    def _set_trust_path(self) -> None:
        """Z ドライブのHoudiniEngine をプラグインとして登録できるように
        trust directory に登録
        """
        self._num()
        houdini_engine_path = str(self.houdini_engine_path).replace(os.sep, '/')
        paths = cmds.optionVar(q=_SafeModeAllowedlistPaths)
        print(f'\n{"Trust directorys ":-<100}')
        for path in paths:
            print(path)
        print(f'{"":-<100}')
        if houdini_engine_path not in paths:
            print('[ Not set Trust path setting ]')
            cmds.optionVar(stringValueAppend=[_SafeModeAllowedlistPaths, houdini_engine_path])
            print(f'[ Set trust directory: {houdini_engine_path} ]')

    def check_loaded_plugin(self) -> list:
        self._num()
        _loaded_plugin = HOUDINI_ENGINE_PLUGIN_NAME in cmds.pluginInfo(query=True, listPlugins=True)
        self.loaded_plugin = _loaded_plugin
        return _loaded_plugin

    def check_loaded_plugin_version(self) -> str:
        self._num()
        _result = ""
        _current_version = cmds.houdiniEngine(buildHoudiniVersion=True)
        if _current_version != self.project_houdini_version:
            _result = f'Current Houdini Version: [ {_current_version} ], '
            _result += f'Project Houdini Version: [ {self.project_houdini_version} ]'
        return _result

    def check_loaded_plugin_path(self) -> str:
        self._num()
        _result = ''
        _path = Path(cmds.pluginInfo(HOUDINI_ENGINE_PLUGIN_NAME, q=True, path=True))
        if _path != self.houdini_engine_plugin:
            _result = str(_path)
        return _result

    def unload_houdini_engine_plugin(self) -> None:
        cmds.unloadPlugin(self.houdini_engine_plugin_name, force=True)

    def load_plugin(self) -> bool:
        self._num()
        _flag = True
        if not HOUDINI_ENGINE_PLUGIN_NAME in cmds.pluginInfo(query=True, listPlugins=True):
            try:
                cmds.loadPlugin(self.houdini_engine_plugin, quiet=True)
                cmds.pluginInfo(self.houdini_engine_plugin, edit=True, autoload=False)
            except Exception as e:
                print(e)
                _flag = False
        return _flag

    def get_houdini_engine_plugin_path(self) -> str:
        return str(self.houdini_engine_plugin).replace(os.sep, '/')


def main() -> bool:
    prg = gui_util.ProgressDialog(title='Activation Houdini Engine', maxValue=11)
    _hou_maya = HoudiniEngineMaya(prg=prg)
    prg.__enter__()
    _exe = _hou_maya.check_houdini_exe_path()
    if _exe:
        _m = f'{_exe}\n Not Fond Houdini EXE Directory'
        _d = gui_util.ConformDialog(titli=HOUDINI_ENGINE_PLUGIN_NAME, message=_m)
        _d.exec_()
        return

    _houdini_engine = _hou_maya.check_houdini_engine_path()
    if _houdini_engine:
        _m = f'{_houdini_engine}\n Not Found Houdini Engine for Maya'
        _d = gui_util.ConformDialog(titli=HOUDINI_ENGINE_PLUGIN_NAME, message=_m)
        _d.exec_()
        return

    _houdini_engine_script = _hou_maya.check_houdini_engine_script_path()
    if _houdini_engine_script:
        _m = f'{_houdini_engine_script}\n Not Found Houdini Engine Script for Maya'
        _d = gui_util.ConformDialog(titli=HOUDINI_ENGINE_PLUGIN_NAME, message=_m)
        _d.exec_()
        return

    _hda_directory = _hou_maya.check_hda_path()
    if _hda_directory:
        _m = f'{_hda_directory}\n Not Found HDA Directory'
        _d = gui_util.ConformDialog(titli=HOUDINI_ENGINE_PLUGIN_NAME, message=_m)
        _d.exec_()
        return

    _hou_maya.add_path()

    _loaded_plugin = _hou_maya.check_loaded_plugin()
    if _loaded_plugin:
        _loaded_houdini_engine_version = _hou_maya.check_loaded_plugin_version()
        _loaded_houdini_engine_path = _hou_maya.check_houdini_engine_path()
        if _loaded_houdini_engine_version or _loaded_houdini_engine_path:
            _hou_maya.unload_houdini_engine_plugin()

    _load_plugin = _hou_maya.load_plugin()
    if not _load_plugin:
        _path = _hou_maya.get_houdini_engine_plugin_path()
        _m = f'{_path}\n Could Not Activate'
        _d = gui_util.ConformDialog(titli=HOUDINI_ENGINE_PLUGIN_NAME, message=_m)
        _d.exec_()
        return
    prg.__exit__()

    if not _loaded_plugin and _load_plugin:
        _m = '<hl>Launch</hl> Houdini Engine for Maya'
        cmds.inViewMessage(assistMessage=f'{_m}', position='midCenter', fade=True)

    return True