from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from pathlib import Path
import importlib
import webbrowser

import maya.cmds as cmds
import maya.mel

from ...utils import gui_util
from . import houdini_util
from . import NAME
from . import HDA_PATH

# import shr.utils.gui_util as gui_util
# importlib.reload(gui_util)
# import shr.utils.hda_loader.houdini_util as houdini_util
# importlib.reload(houdini_util)


class HDAData:
    def __init__(self, name="", path=Path(), parent_folder=''):
        self.name = name
        self.short_name = name.split("/")[-1]
        self.path = str(path).replace(os.sep, '/')
        self.btn_name = "{}_{}_btn".format(NAME, name)
        self.parent_folder = parent_folder
        self.develop = False
        self.set_develop_mode()

    def set_develop_mode(self):
        if self.parent_folder == "develop":
            self.develop = True

    def __repr__(self) -> str:
        return self.short_name


def _trackSelectionOrder_Flag(_flag=False):
    """ジオメトリの選択順を有効化
    元の設定をとっておきツール終了時に元に戻す
    Returns:
        [bool]: 元の設定のフラグ
    """
    _tso_flag = cmds.selectPref(q=True, trackSelectionOrder=True)
    if not _tso_flag:
        cmds.selectPref(trackSelectionOrder=True)
    return _tso_flag

def _reset_track_selection_order_flag(_flag=True):
    """Maya の選択順を保持するスイッチ

    Args:
        _flag (bool, optional): _description_. Defaults to True.
    """
    cmds.selectPref(trackSelectionOrder=_flag)

def check_path_exists(path="", make_dir=False):
    """パスが存在するかの確認

    Args:
        path (str): [description]
        make_dir (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """
    if not os.path.exists(path) and make_dir:
        os.makedirs(path)

    if not os.path.exists(path):
        print("Not Found [ {} ]".format(path.replace(os.sep, '/')))
        return
    else:
        return True

def check_houdini_engine():
    """プロジェクト管理のHoudiniEngine
    確認、読み込み

    Returns:
        _type_: _description_
    """
    return houdini_util.main()

def open_help_site():
    """ヘルプサイト表示
    """
    _web_site = "https://wisdom.cygames.jp/display/shenron/Maya:+HDA+Loader"
    webbrowser.open(_web_site)

def _iter_path(path=Path()) -> list:
    """HDA を集める

    Args:
        path (_type_, optional): _description_. Defaults to Path().

    Returns:
        list: [Pathlib.Path]
    """
    _paths = []
    for _path in path.iterdir():
        if _path.suffix.lower() == ".hda":
            _paths.append(_path)
    return _paths

def reload_hda():
    """Maya 状のHoudiniAsset の再読み込み
    """
    nodes = cmds.ls(type="transform")
    houdini_assets = []
    _error = []

    for node in nodes:
        try:
            if cmds.nodeType(node) == "houdiniAsset":
                houdini_assets.append(node)
        except Exception as e:
            _error.append(node)

    if houdini_assets:
        for houdini_asset in houdini_assets:
            cmds.houdiniAsset(reloadAsset=houdini_asset)

    if _error:
        print('\n\n{:-^100}'.format("  Reload Error  "))
        for _e in _error:
            print(f'[ {_e} ]')
        print('{:-^100}\n\n'.format("  Reload Error  "))

def get_hdas(hda_path='') -> list:
    """hda_path のHDA を集めて
    Maya 上のHoudiniAsset として読み込む

    Args:
        hda_path (str, optional): _description_. Defaults to ''.

    Returns:
        dict: HDAData.short_name(Sop/が入らない名前): HDAData
    """
    _hda_files = []
    _hda_datas = {}
    _error = []
    if not hda_path:
        hda_path = HDA_PATH

    hda_path = Path(hda_path)
    _hda_files = _iter_path(hda_path)

    hda_develop_path = hda_path / "develop"
    _hda_files.extend(_iter_path(hda_develop_path))

    for _hda in _hda_files:
        _asset_names = None
        parent_folder = _hda.parent.stem
        try:
            _asset_names = cmds.houdiniAsset(listAssets=_hda)
        except Exception as e:
            _error.append(_hda)
        if _asset_names:
            for _asset_name in _asset_names:
                _hda_data = HDAData(name=_asset_name, path=_hda, parent_folder=parent_folder)
                _hda_datas[_hda_data.short_name] = _hda_data
    if _error:
        print('\n\n{:-^100}'.format("  Import Error  "))
        for _e in _error:
            print(f'[ {_e} ]')
        print('{:-^100}\n\n'.format("  Import Error  "))

    return _hda_datas

def load_hda(hda=None):
    """HDA の読み込みとアサイン
    読み込み後にアトリビュートに値を設定
    HoudiniAsset を選択
    Args:
        hda (_type_, optional): _description_. Defaults to None.
    """
    if not hda:
        return
    selections = cmds.ls(orderedSelection=True, type='transform')
    if not selections:
        gui_util.conform_dialog(message='Select Transform Node')
        return

    hda_node = cmds.houdiniAsset(loadAsset=[hda.path, hda.name])
    mel_string_array = '{{ {} }}'.format(', '.join(['"{}"'.format(s) for s in selections]))
    maya.mel.eval("houdiniEngine_setAssetInput {} {}".format(
                            hda_node + ".input[0].inputNodeId", mel_string_array))

    cmds.select(hda_node, replace=True)

def sync_asset(hda_node=None, sync_attribute=False, sync_output=False):
    """HoudiniAsset をsync する

    Args:
        hda_node (_type_, optional): _description_. Defaults to None.
        sync_attribute (bool, optional): _description_. Defaults to False.
        sync_output (bool, optional): _description_. Defaults to False.
    """
    if not cmds.objExists(hda_node):
        return

    if not cmds.attributeQuery("outputHiddenObjects", name=hda_node, exists=True):
        hidden_flag = cmds.getAttr(hda_node + ".outputHiddenObjects")
    else:
        hidden_flag = False

    if not cmds.attributeQuery("outputTemplatedGeometries", name=hda_node, exists=True):
        template_flag = cmds.getAttr(hda_node + ".outputTemplatedGeometries")
    else:
        template_flag = False

    houdini_assets = cmds.houdiniAsset(loadAsset=[hda_node.path, hda_node.name])
    if not houdini_assets:
        return

    cmds.houdiniAsset(
                sync=houdini_assets,
                syncAttributes=sync_attribute,
                syncOutputs=sync_output,
                syncHidden=hidden_flag,
                syncTemplatedGeos=template_flag
                )

def bake_asset() -> None:
    selections = cmds.ls(selection=True, type="houdiniAsset")

    if not selections:
        gui_util.conform_dialog(message='Select HoudiniAsset Node')
        return

    for selection in selections:
        maya.mel.eval(f'houdiniEngine_bakeAsset {selection};')

def wire_display_toggle():
    """ワイヤー表示の表示トグル
    """
    if cmds.displayPref(q=True, wireframeOnShadedActive=True) == 'full':
        cmds.displayPref(wireframeOnShadedActive='none')
    else:
        cmds.displayPref(wireframeOnShadedActive='full')

def wire_display_full():
    """ワイヤー表示の強制表示
    終了時に表示させるようにする
    """
    cmds.displayPref(wireframeOnShadedActive='full')