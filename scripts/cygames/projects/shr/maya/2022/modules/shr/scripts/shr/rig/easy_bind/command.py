from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial
from pathlib import Path
import subprocess
import json
import os
import re
import yaml
import webbrowser
import xml.etree.ElementTree as ET

from PySide2 import QtCore

import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as om2anim
import maya.cmds as cmds
import maya.mel

from ...utils import gui_util

from . import TOOL_NAME
from . import NAME
from . import WEIGHT_FILE_FORMAT
from . import PROJECT_WEIGHT_FILE_FORMAT

from . import JOINT_SUFFIX
from . import END_JOINT
from . import MOTION_POINT
from . import ROOT

from . import JOINT_SUFFIXES
from . import JOINT_COLOR_INDEX
from . import JOINT_OUTLINER_COLOR

HERE = Path(os.path.dirname(os.path.abspath(__file__)))
YAML_FILE_NAME = "settings.yaml"


def open_web_site():
    """ヘルプサイトを開く
    """
    _web_site = 'https://wisdom.cygames.jp/display/shenron/Maya:+Easy+Bind'
    webbrowser.open(_web_site)

def conform_dialog(title='', message=''):
    """ダイアログ表示

    Args:
        title (str, optional): ウィンドウタイトル. Defaults to ''.
        message (str, optional): 表示メッセージ. Defaults to ''.
    """
    if not title:
        title=TOOL_NAME
    _d = gui_util.ConformDialog(title=title, message=message)
    _d.exec_()
    print(message)

def _count_success(_length=1, _error_flag=0, _prefix='Import'):
    """成功数を数えて表示する

    Args:
        _length (int, optional): 全体の数. Defaults to 1.
        _error_flag (int, optional): エラーとなった数. Defaults to 0.
        _prefix (str, optional): 行った処理. Defaults to 'Import'.
    """
    _success_flag = _length - _error_flag

    _m = ''
    if _success_flag:
        _m += f'{_prefix} [ {_success_flag} ] count(s)'
    if _error_flag:
        if _success_flag:
            _m += "\n"
        _m += f"Could not {_prefix} [ {_error_flag} ] count(s)"

    _d = gui_util.ConformDialog(title=TOOL_NAME, message=_m)
    _d.exec_()
    print(_m)

def attach_job(object_name="", job=None):
    """GUI にスクリプトジョブを付ける

    Args:
        object_name (str): GUI Object name
        job (function):
    """
    if not object_name or not job:
        return
    # cmds.scriptJob(parent=object_name, event=("SceneOpened", partial(job)))
    cmds.scriptJob(parent=object_name, event=("PostSceneRead", partial(job)))
    cmds.scriptJob(parent=object_name, event=("NewSceneOpened", partial(job)))
    cmds.scriptJob(parent=object_name, event=("NameChanged", partial(job)))

def query_joint_view()->tuple:
    joint_view = cmds.modelEditor(
                    'modelPanel4',
                    q=True,
                    joints=True,
                    )
    joint_xray = cmds.modelEditor(
                    'modelPanel4',
                    q=True,
                    jointXray=True,
                    )
    return joint_view, joint_xray

def change_joint_view(joint_view:bool=True):
    cmds.modelEditor(
                    'modelPanel4',
                    edit=True,
                    joints=joint_view,
                    )

def change_joint_xray(joint_xray:bool=False):
    cmds.modelEditor(
                    'modelPanel4',
                    edit=True,
                    jointXray=joint_xray,
                    )

def toggle_joint_axis_view(view_state:bool=False):
    joints:list = cmds.ls(type='joint', long=True)
    if not joints:
        return
    for joint in joints:
        if not cmds.getAttr(f'{joint}.displayLocalAxis', lock=True):
            cmds.setAttr(f'{joint}.displayLocalAxis', view_state)

def select_neck_vtx():
    file_path = r'C:\cygames\shrdev\shr\tools\in\ext\maya\2022\modules\shr\scripts\shr\rig\easy_bind\joint_weight.json'
    skin_cluster = 'mob0010:skinCluster4'
    node = 'mob0010:head_lod0'

    with open(file_path, "r") as json_data:
        weight_data = json.load(json_data)

    _vtx = []
    for vtx, inf_weight in weight_data.items():
        _vtx_name = f'{node}.vtx[{vtx}]'
        _vtx.append(_vtx_name)

    if _vtx:
        cmds.select(_vtx, replace=True)
        maya.mel.eval('setSelectMode components Components; selectType -smp 1 -sme 0 -smf 0 -smu 0 -pv 1 -pe 0 -pf 0 -puv 0; HideManipulators;')

def load_joint_weight(file_path:str='', node:str='', skin_cluster:str=''):
    if not file_path or not skin_cluster or not node:
        return

    file_path = r'C:\cygames\shrdev\shr\tools\in\ext\maya\2022\modules\shr\scripts\shr\rig\easy_bind\joint_weight.json'

    skin_cluster = 'head_lod0_mesh_skinCluster'
    node = 'head_lod0_mesh_lod0'

    with open(file_path, "r") as json_data:
        weight_data = json.load(json_data)
    _infs = []

    for i,(vtx, inf_weight) in enumerate(weight_data.items()):
        _vtx_name = f'{node}.vtx[{vtx}]'
        _infs.extend(inf_weight.keys())

    _infs = list(set(_infs))

    for inf in _infs:
        try:
            cmds.skinCluster('head_lod0_mesh_skinCluster', edit=True, useGeometry=True, polySmoothness=0.0, lockWeights=True, weight=0.0, addInfluence=inf)
            cmds.skinCluster(skin_cluster, influence=inf, e=True, lockWeights=False)
        except Exception as e:
            print(e)
            pass

    for i,(vtx, inf_weight) in enumerate(weight_data.items()):
        _vtx_name = f'{node}.vtx[{vtx}]'
        cmds.skinPercent(skin_cluster, _vtx_name, transformValue=list(inf_weight.items()))
    cmds.skinCluster(skin_cluster, edit=True, forceNormalizeWeights=True)

def get_weightdata_from_json(file_path:Path=None)->dict:
    weight_data = {}
    if not file_path:
        return weight_data
    file_path = Path(file_path)
    if not file_path.exists():
        return weight_data

    with open(file_path, "r") as json_data:
        weight_data = json.load(json_data)

    return weight_data

def get_joints_from_json(file_path:Path=None)->list:
    if not file_path:
        return

    joints:list = []

    with open(file_path, "r") as json_data:
        weight_data = json.load(json_data)

    if not weight_data:
        return joints
    for k,v in weight_data.items():
        for inf, weight in v.items():
            joints.append(inf)

    return joints


def load_weight_json(save_directory:str=''):
    if not save_directory:
        return

    file_path = f'{save_directory}/memory.json'
    weight_data = get_weightdata_from_json(file_path=file_path)

    if weight_data:
        # cmds.warning('Load Weight Data')
        # cmds.warning(f'Load File: [ {file_path} ]')
        print(f'Load Json File: [ {file_path} ]')

    return weight_data


def weight_dict_updater(old_dict:dict, new_dict:dict)->dict:
    old_dict = old_dict.copy()

    for shape in new_dict.keys():
        if shape in old_dict:
            _old_dict = old_dict[shape].copy()
            for vtx in new_dict[shape].keys():
                _old_dict[vtx] = new_dict[shape][vtx]
            old_dict[shape] = _old_dict
        else:
            old_dict[shape] = new_dict[shape]

    return old_dict

def save_weight_json(weight_data:dict={}, save_directory:str='', clear:bool=False)->None:
    if  not save_directory:
        return

    if not clear and not weight_data:
        cmds.warning('No Weight Data')
        return

    if not check_path_exists(path=save_directory, make_dir=True):
        return

    _old_data = load_weight_json(save_directory=save_directory)

    if clear:
        weight_data = dict()
    else:
        weight_data = weight_dict_updater(old_dict=_old_data, new_dict=weight_data)

    file_path = Path(save_directory) / 'memory.json'
    _save:bool = False

    with open(str(file_path), "w") as _json_file:
       _json_data = json.dumps(
           weight_data,
        #    indent=4,
        #    separators=(',', ': ')
           )
       try:
           _json_file.write(_json_data)
           _save = True
       except Exception as e:
        print(f'Save Json Error: [ {e} ]')

    if _save:
        if clear:
            print(f'Clear Save Json File: [ {file_path} ]')
        else:
            print(f'Save Json File: [ {file_path} ]')

def chose_node_selections(nodes:list=[], node_type='mesh', project_name='Shenron', metahuman_name_flag=False)->list:

    # {'Metahuman': {'joint': ['DHI:root', 'root_div'], 'mesh': ['rig']}, 'Shenron': {'joint': ['root_jnt', 'mesh']}}
    _root_node_name:dict = load_config('Root_Node')

    if not nodes:
        return
    result_nodes = []
    for node in nodes:
        if not cmds.objExists(node):
            continue
        node_long_name = cmds.ls(node, long=True)[0]
        node_name_split = node_long_name.split("|")
        if node_type == 'mesh':
            if project_name == 'Shenron' and node_name_split[1] in _root_node_name['Shenron']['mesh']:
                result_nodes.append(node)
            if metahuman_name_flag and node_name_split[1] in _root_node_name['Metahuman']['mesh']:
                result_nodes.append(node)
        if node_type == 'joint':
            if project_name == 'Shenron' and node_name_split[1] in _root_node_name['Shenron']['joint']:
                result_nodes.append(node)
            if metahuman_name_flag and node_name_split[1] in _root_node_name['Metahuman']['joint']:
                result_nodes.append(node)
    return result_nodes


def paste_weights(weight_data:dict={})->None:
    _add_influence_flag = False
    selections:list = cmds.ls(selection=True, flatten=True)
    selection_nodes:list = cmds.ls(selection=True, objectsOnly=True)
    # print(selection_nodes)
    # print(len(selection_nodes))
    if not selection_nodes or len(selection_nodes) != 1:
        return

    selection:str = selection_nodes[0]
    # print(selection)
    shape_node:str = ''

    # print(cmds.listRelatives(selection_nodes, children=True, type='mesh'), " ---")

    if cmds.nodeType(selection) == 'transform':
        shape_node = [x for x in cmds.listRelatives(selection_nodes, children=True, type='mesh')if x and not x.endswith('Orig')]
        # print(shape_node, " ======")
        if not shape_node:
            return
        shape_node = shape_node[0]
    else:
        shape_node = selection
    # print(shape_node)

    vtxs:list = cmds.filterExpand(cmds.polyListComponentConversion(selections, toVertex=True), selectionMask=31)
    shape_weightdata:dict = {}

    if not vtxs:
        return

    joints:list = []
    selection:str = selection_nodes[0]
    skin_cluster:str = get_skin_cluster(selection)
    # print(weight_data)
    # print(selection)
    # print(skin_cluster)
    shape_weightdata = weight_data.get(shape_node.rsplit('|')[-1])
    # print(shape_weightdata)

    if not shape_weightdata:
        cmds.warning('No Wwight Data')
        return

    joints = []
    _new_weight_data = {}
    for vtx, inf_weight in shape_weightdata.items():
        _new_inf_weight = {}
        for inf, weight in inf_weight.items():
            if ':' in inf:
                _name_split = inf.split(':')
                inf = _name_split[-1]
            if cmds.objExists(inf):
                _add_influence_flag = True
                _new_inf_weight[inf] = weight
                joints.append(inf)
        if _new_inf_weight:
            _new_weight_data[vtx] = _new_inf_weight

    if _add_influence_flag:
        joints = list(set(joints))
        add_influence(skin_cluster=skin_cluster, joints=joints)

    _length = len(vtxs)
    _count = 0
    _do_it = 0

    with gui_util.ProgressDialog(title='Paste Weight', message="Paste Weight ...", maxValue=_length) as prg:
        QtCore.QCoreApplication.processEvents()
        for vtx in vtxs:
            _count += 1
            _id = vtx.rsplit('[')[-1][:-1]
            inf_weight = _new_weight_data.get(_id)

            if inf_weight:
                _do_it += 1
                # cmds.skinPercent(skin_cluster, vtx, resetToDefault=True)
                cmds.skinPercent(skin_cluster, vtx, transformValue=list(inf_weight.items()), zeroRemainingInfluences=True)

            prg.setValue(_count)
            prg.step(_count)
            if prg.wasCanceled():
                break
    cmds.skinCluster(skin_cluster, edit=True, forceNormalizeWeights=True)


    if _do_it:
        cmds.warning(f"Paste Weights [ {_do_it} ] vertex ID")
        # conform_dialog(message=f"Paste Weights [ {_count} ] vertex ID")
    else:
        cmds.warning("Not Found Weight Data")


def memory_weights()->dict:
    _w_dict:dict = {}
    selections:list = cmds.ls(selection=True, flatten=True)
    selection_nodes:list = cmds.ls(selection=True, objectsOnly=True)
    # print(selections)
    # print(selection_nodes)
    if not selection_nodes or len(selection_nodes) != 1:
        return _w_dict

    selection:str = selection_nodes[0]
    shape_node:str = ''
    if cmds.nodeType(selection) == 'transform':
        shape_node = [x for x in cmds.listRelatives(selection, children=True, type='mesh')if x and not cmds.getAttr(f"{x}.intermediateObject")]
        if not shape_node:
            return _w_dict
        shape_node = shape_node[0]
    else:
        shape_node = selection

    vtxs:list = cmds.filterExpand(cmds.polyListComponentConversion(selections, toVertex=True), selectionMask=31)
    shape_weightdata:dict = {}

    if not vtxs:
        return _w_dict

    skin_cluster:str = get_skin_cluster(shape_node)
    if not skin_cluster:
        return _w_dict

    _length = len(vtxs)
    _count = 0

    with gui_util.ProgressDialog(title='Memory Weight', message="Memory Weight ...", maxValue=_length) as progress:
        for vtx in vtxs:
            QtCore.QCoreApplication.processEvents()
            _count += 1
            if progress.wasCanceled():
                break
            _infs:list = [x.split(':')[-1] if len(x.split(':')) != 1 else x for x in cmds.skinPercent(skin_cluster, vtx, q=True, transform=None)]
            _weight:list = cmds.skinPercent(skin_cluster, vtx, q=True, value=True)
            _vtx_dict:dict = dict([[i,w] for i,w in zip(_infs, _weight) if w])

            _w_dict[vtx.rsplit('[')[-1][:-1]] = _vtx_dict
            progress.setValue(_count)
            progress.step(_count)
    shape_weightdata[shape_node] = _w_dict
    if _count:
        print(f"Copy Weights [ {_count} ] vertex ID")
    else:
        cmds.warning("Not Found Weight Data")
    return shape_weightdata


def load_config(config_name:str = ''):

    with open(HERE / YAML_FILE_NAME, encoding='utf-8') as f:
        config = yaml.safe_load(f)
    _confing_data = config.get(config_name, None)
    return _confing_data

def create_work_directory(work_dir='', create=True):
    """ディレクトリ作成
    下のものと被るが、こちらは作るだけ

    Args:
        work_dir (str, optional): _description_. Defaults to ''.
        create (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    work_dir = Path(work_dir)
    work_dir = work_dir / NAME
    if create:
        work_dir.mkdir(parents=True, exist_ok=True)
    return work_dir

def check_path_exists(path="", make_dir=False):
    """パスが存在するかの確認
    あるなしの確認を返す、フラグで作成

    Args:
        path (str): [description]
        make_dir (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """
    if not path:
        conform_dialog(message="Scene files need to be saved")
        return

    if not os.path.exists(path) and make_dir:
        os.makedirs(path, exist_ok=True)

    if not os.path.exists(path):
        conform_dialog(message="Not Found [ {} ]".format(path.replace(os.sep, '/')))
        return
    else:
        return True

def _trackSelectionOrder_Flag(_flag=False):
    """ウェイトコピーの際に選択順に適用するための関数
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

def selection_target(select_target=[]):
    select_target = [x for x in select_target if cmds.objExists(x)]
    if select_target:
        cmds.select(select_target, replace=True)
    else:
        cmds.select(clear=True)

def get_file_info_data(data_name="") -> str:
    """Maya のシーンに設定されたfileInfo のデータ取得
    shenron Easy Bind_{data_name}
    の形になる
    Args:
        data_name (str, optional): fileInfo のデータ名. Defaults to "".

    Returns:
        str: _description_
    """
    _info_data = cmds.fileInfo("{}_{}".format(TOOL_NAME, data_name), q=True)

    return _info_data or None

def set_file_info_data(data_name="", value=""):
    """Maya シーンにfileInfo のデータを設定する

    Args:
        data_name (str, optional): fileInfo のデータ名. Defaults to "".
        value (str, optional): 設定するのデータの値. Defaults to "".
    """
    cmds.fileInfo("{}_{}".format(TOOL_NAME, data_name), value)

def open_exploer(path=''):
    """パスを受け取りWindowsエクスプローラーで表示させる

    Args:
        path (str): ディレクトリパス
    """
    _path = str(path)
    _path = _path.replace(os.sep, "/")
    _m = ''
    if not os.path.exists(_path):
        _m = f"[ {_path} ] not found"
        conform_dialog(message=_m)
        return
    try:
        subprocess.Popen(['explorer', os.path.normpath(_path)])
    except:
        _m = f'[ {_path} ] could not open'
        conform_dialog(message=_m)
        pass

def get_parents(node:str='') -> str:
    """ルートノード取得

    Args:
        node (str)): Maya ノードの文字列

    Yields:
        [type]: [description]
    """
    parent = cmds.listRelatives(node, parent=True, fullPath=True)
    if parent:
        yield parent[0]
        for p in get_parents(parent):
            yield p
    else:
        yield node[0] if isinstance(node, list) else node

def get_skin_cluster(node: str) -> str:
    """スキンクラスタの存在確認

    Args:
        node (str): メッシュノード

    Returns:
        str: スキンクラスタノード
    """

    flag = ""
    if cmds.objExists(node):
        _historys = cmds.listHistory(node)
        if _historys:
            for _history in _historys:
                if cmds.nodeType(_history) == "skinCluster":
                    flag = _history
                    break
    return flag

def select_nodes(nodes:list=[], add_select_flag:bool=False, ignore_lod:bool=False)->None:
    if not nodes:
        cmds.select(clear=True)
        return
    _exists_nodes = []
    with gui_util.ProgressDialog(
                        title='Progress',
                        message='progress ...',
                        maxValue=len(nodes)) as prg:
        for i, node in enumerate(nodes):

            if prg.wasCanceled():
                break
            if ignore_lod and 'lod' in node:
                m = re.findall(r'\d+', node)
                if '0' not in m:
                    continue
            if cmds.objExists(node):
                _exists_nodes.append(node)
            else:
                node_short_name = node.rsplit("|", 1)[-1]
                node = cmds.ls(node_short_name, long=True)
                if node:
                    _exists_nodes.append(node[0])
            prg.step(i)

    if add_select_flag:
        cmds.select(_exists_nodes, add=True)
    else:
        cmds.select(_exists_nodes, replace=True)

def set_joint_color(joint:str=""):
    """ジョイントカラーの設定

    Args:
        joint (str, optional): _description_. Defaults to "".
    """
    if not joint:
        return

    joints = cmds.listRelatives(joint, allDescendents=True, fullPath=True, type="joint")

    if not joints:
        return

    for joint in joints:
        joint_short_name = joint.rsplit("|", 1)[-1]
        suffix = joint_short_name.rsplit("_", 1)[-1]
        _flag = True
        if suffix in JOINT_SUFFIXES:
            cmds.setAttr(f'{joint}.template', False)
            connections = cmds.listConnections(f"{joint}.drawOverride", connections=True, plugs=True)
            if connections:
                soueces = connections[1::2]
                targets = connections[0::2]
                for source, target in zip(soueces, targets):
                    cmds.disconnectAttr(source, target)

            if suffix == JOINT_SUFFIX:
                _flag = False

            if cmds.getAttr(f"{joint}.template"):
                cmds.setAttr(f"{joint}.template", False)

            cmds.setAttr(f"{joint}.overrideEnabled", _flag)
            cmds.setAttr(f"{joint}.useOutlinerColor", _flag)

            cmds.setAttr(f"{joint}.overrideRGBColors", False)
            cmds.setAttr(f"{joint}.overrideColor", JOINT_COLOR_INDEX[suffix])
            cmds.setAttr(f"{joint}.overrideColorR", 0.0)
            cmds.setAttr(f"{joint}.overrideColorG", 0.0)
            cmds.setAttr(f"{joint}.overrideColorB", 0.0)

            cmds.setAttr(f"{joint}.outlinerColor",
                                            JOINT_OUTLINER_COLOR[suffix][0],
                                            JOINT_OUTLINER_COLOR[suffix][1],
                                            JOINT_OUTLINER_COLOR[suffix][2])
            cmds.setAttr(f"{joint}.objectColor", False)
            cmds.setAttr(f"{joint}.objectColorR", 0.0)
            cmds.setAttr(f"{joint}.objectColorG", 0.0)
            cmds.setAttr(f"{joint}.objectColorB", 0.0)

def skin_cluster_check(influenceAssociation:str='closestJoint',src:str='', dst:str=''):
    if influenceAssociation in ['label', 'name', 'oneToOne']:
        src_lnfluences = cmds.skinCluster(src, q=True, influence=True)
        dst_lnfluences = cmds.skinCluster(dst, q=True, influence=True)
        if len(src_lnfluences) != len(dst_lnfluences):
            return True
    return

def weight_copy(
            src:str="",
            dst:str="",
            surfaceAssociation:str='closestPoint',
            influenceAssociation:str='closestJoint',
            normalize:bool=False
            ):
    """ウェイトのコピー

    Args:
        src (str, skinCluster): [skinCluster name]. スキンクラスタの名前（skinCluster30）
        dst (str, skinCluster): [skinCluster name]. スキンクラスタの名前（skinCluster30）
    """
    if not src or not dst:
        return True
    if skin_cluster_check(influenceAssociation=influenceAssociation, src=src, dst=dst):
        return True
    cmds.copySkinWeights(sourceSkin=src,
                        destinationSkin=dst,
                        noMirror=True,
                        surfaceAssociation=surfaceAssociation,
                        influenceAssociation=influenceAssociation,
                        noBlendWeight=True,
                        normalize=normalize)
    return

def weight_copy_uv(
            src:str="",
            dst:str="",
            src_uv:str='',
            dst_uv:str='',
            surfaceAssociation:str='closestPoint',
            influenceAssociation:str='closestJoint',
            normalize:bool=False
            ):
    """ウェイトのコピー

    Args:
        src (str, skinCluster): [skinCluster name]. スキンクラスタの名前（skinCluster30）
        dst (str, skinCluster): [skinCluster name]. スキンクラスタの名前（skinCluster30）
    """
    if not src or not dst:
        return True
    if skin_cluster_check(influenceAssociation=influenceAssociation, src=src, dst=dst):
        return True
    cmds.copySkinWeights(sourceSkin=src,
                        destinationSkin=dst,
                        noMirror=True,
                        surfaceAssociation=surfaceAssociation,
                        influenceAssociation=influenceAssociation,
                        uvSpace=(src_uv, dst_uv),
                        noBlendWeight=True,
                        normalize=normalize)
    return

class NodeSelections:
    def __init__(self, project=""):
        self.project = project

        # シーン中の全ジョイント
        self.all_joints = []

        # バインドに必要なジョイント
        self.need_joints = []

        # 選択からメッシュシェイプ抽出
        # トランスフォームノードとシェイプの辞書
        self.need_transform_meshes = {}

        # shenron 仕様
        # シーンルートにあるノード、下4文字が整数
        self.shenron_root_node = ""

        # lod0 の全トランスフォームノード
        self.lod0_group_nodes = {}

        # lodGroup 直下のトランスフォームノード
        # 最初のLOD(LOD0)を抜かしている
        self.lod_root_group = []
        # lodGroup 直下のトランスフォームノードの数
        self.lod_length = 0

        if project == "shenron":
            self.get_shenron_root_node()

    def get_need_nodes_from_current_selection(self):
        """現在の選択から必要なノードを取得
        """
        selections = cmds.ls(selection=True, type="transform")
        if not selections:
            return
        for sel in selections:
            shape = cmds.listRelatives(sel, children=True, type="mesh", fullPath=True, noIntermediate=True)
            if shape:
                shape = [x for x in shape if not cmds.getAttr("{}.intermediateObject".format(x))][0]
                self.need_transform_meshes[sel] = shape
            else:
                self.need_joints.append(sel)

    def get_shenron_root_node(self):
        """shenron 仕様のルート取得
        下4桁が整数のルートノードをshenron 仕様のノードと判定
        シーン名との符合があってもいいかも
        """
        root_nodes = cmds.ls(assemblies=True)

        # シーンのルートノードで下四文字が整数のものをshenron ノードとする
        shenron_root_node = [x for x in root_nodes if x[-4:].isdecimal()]
        if shenron_root_node:
            self.shenron_root_node = shenron_root_node[0]

    def get_all_joints(self):
        """ルートノード以下の前ジョイント取得
        """
        # プロジェクト用の分岐shenron プロジェクトはルートノードは
        # 最後の４文字が整数
        joints = []
        if self.project == "shenron":
            if self.shenron_root_node:
                joints = cmds.listRelatives(
                                            self.shenron_root_node,
                                            type="joint",
                                            fullPath=True,
                                            allDescendents=True
                                            )
        else:
            joints = cmds.ls(
                            type="joint",
                            long=True,
                            )
        self.all_joints = joints

    def get_need_joints(self):
        """ルートノード以下からshenron 仕様のジョイント選択
        """
        self.get_all_joints()
        if not self.all_joints:
            return

        if self.project == "shenron":
            joints = [x for x in self.all_joints if not x.rsplit("|", 1)[-1].startswith(ROOT) and
                                                    not x.endswith(END_JOINT) and
                                                    not x.endswith(MOTION_POINT)]
        else:
            joints = self.all_joints

        self.need_joints = joints

    def select_all_joints(self, add_selection:bool=False):
        """ルートノード以下の前ジョイント選択
        """
        self.get_all_joints()
        self.select_node(select_node_type="all_joint", add_selection=add_selection)

    def select_need_joints(self, add_selection:bool=False):
        """ルートノード以下のスキニングに関連するジョイント選択
        """
        self.get_need_joints()
        self.select_node(select_node_type="need_joint", add_selection=add_selection)

    def select_need_transform_meshes(self, ignore_lod_flag:bool=False, add_selection:bool=False):
        """ルートノード以下のメッシュノードを持ったトランスフォームノードとメッシュノードの辞書
        を作成し、トランスフォームノードを選択

        Args:
            ignore_lod_flag (bool, optional): _description_. Defaults to False.
        """
        self.get_scene_transform_meshes(ignore_lod_flag=ignore_lod_flag)
        self.select_node(select_node_type="transform", add_selection=add_selection)

    def select_need_transform_and_joint(self, ignore_lod_flag:bool=False, add_selection:bool=False):
        """ルートノード以下のメッシュノードを持ったトランスフォームノードとメッシュノードの辞書
        を作成し、トランスフォームノードとジョイントノードを選択

        Args:
            ignore_lod_flag (bool, optional): _description_. Defaults to False.
        """
        self.get_need_joints()
        self.get_scene_transform_meshes(ignore_lod_flag=ignore_lod_flag)
        self.select_node(select_node_type="transform and joint", add_selection=add_selection)

    def get_metahuman_lodgroups(self)->dict:
        lod_group_mesh = {}
        selections = cmds.ls(selection=True, type='transform', long=True)
        if not selections and len(selections) != 1:
            return

        _lod_group = selections[0]

        lod_groups = cmds.listRelatives(_lod_group, children=True, type="transform", path=True)
        if not lod_groups:
            return

        for lod_group in lod_groups:
            meshes = cmds.listRelatives(lod_group, allDescendents=True, type="mesh", path=True)
            for mesh in meshes:
                if cmds.getAttr("{}.intermediateObject".format(mesh)):
                    continue
                lod_group_mesh[lod_group] = mesh
        return lod_group_mesh

    def get_lod_group_nodes_from_selection(self, full_path:bool=True):
        selections = cmds.ls(selection=True, type='transform', long=True)
        if not selections and len(selections) != 1:
            return

        _lod_group = selections[0]

        lod_nodes = cmds.listRelatives(_lod_group, children=True, type="transform", fullPath=True)
        if not lod_nodes:
            return

        self.lod_root_group = lod_nodes[1:]
        self.lod_length = len(self.lod_root_group)
        if full_path:
            meshes = cmds.listRelatives(lod_nodes[0], allDescendents=True, type="mesh", fullPath=True)
        else:
            meshes = cmds.listRelatives(lod_nodes[0], allDescendents=True, type="mesh", path=True)
        for mesh in meshes:
            if cmds.getAttr("{}.intermediateObject".format(mesh)):
                continue
            parent = cmds.listRelatives(mesh, parent=True, type="transform", path=True)[0]
            self.lod0_group_nodes[parent] = mesh

    def get_lodgroup_nodes(self):
        _lod_group = cmds.ls(type='lodGroup')
        if not _lod_group:
            return

        lod_nodes = cmds.listRelatives(_lod_group, children=True, type="transform", fullPath=True)
        if not lod_nodes:
            return

        self.lod_root_group = lod_nodes[1:]
        self.lod_length = len(self.lod_root_group)
        meshes = cmds.listRelatives(lod_nodes[0], allDescendents=True, type="mesh", fullPath=True)
        for mesh in meshes:
            if cmds.getAttr("{}.intermediateObject".format(mesh)):
                continue
            parent = cmds.listRelatives(mesh, parent=True, type="transform", path=True)[0]
            self.lod0_group_nodes[parent] = mesh

    def get_scene_transform_meshes(self, full_path_flag:bool=False, ignore_lod_flag:bool=False):
        """ルートノード以下のメッシュノードを持ったトランスフォームノードとメッシュノードの辞書を作成

        Args:
            full_path_flag (bool, optional): _description_. Defaults to True.
            ignore_lod_flag (bool, optional): _description_. Defaults to False.

        """
        self.lod0_group_nodes = {}
        self.need_transform_meshes = {}
        meshes = []

        if self.project == "shenron":
            if not self.shenron_root_node:
                return
            meshes = cmds.listRelatives(self.shenron_root_node, allDescendents=True, type="mesh", fullPath=True)
        else:
            meshes = cmds.ls(type="mesh", long=True)

        if not meshes:
            return

        for mesh in meshes:
            if cmds.getAttr("{}.intermediateObject".format(mesh)):
                continue
            if not full_path_flag:
                parent = cmds.listRelatives(mesh, parent=True, type="transform", path=True)
            else:
                parent = cmds.listRelatives(mesh, parent=True, type="transform", fullPath=True)

            parent = parent[0]
            if ignore_lod_flag:
                # split_name = parent.rsplit('|')[-1]
                if parent[-4:].startswith('lod') and parent[-1] != '0':
                    continue

            self.need_transform_meshes[parent] = mesh

    def get_lod_length(self) -> int:
        return self.lod_length

    def get_lod0_nodes_from_selection(self, full_path:bool=True)->dict:
        self.get_lod_group_nodes_from_selection(full_path=full_path)
        return self.lod0_group_nodes

    def get_lod0_nodes(self)->dict:
        self.get_lodgroup_nodes()
        return self.lod0_group_nodes

    def get_need_transform_by_weight_transfer_lod(self)->dict:
        self.get_scene_transform_meshes()
        return self.need_transform_meshes


    def get_bind_need_mesh_transforms_from_selection(self)->list:
        """選択から必要なトランスフォームノード、メッシュシェイプの辞書作成
        トランスフォームノードのリストを返す

        Returns:
            list: _description_
        """
        self.get_need_nodes_from_current_selection()
        return list(self.need_transform_meshes.keys())

    def get_bind_need_mesh_transforms(self, ignore_lod_flag:bool=False)->list:
        """ルートノード以下のトランスフォームノード、シェイプの辞書作成
        トランスフォームノードのリストを返す

        Args:
            ignore_lod_flag (bool, optional): _description_. Defaults to False.

        Returns:
            list: _description_
        """
        self.get_scene_transform_meshes(ignore_lod_flag=ignore_lod_flag)
        return list(self.need_transform_meshes.keys())

    def get_bind_need_joints(self)->list:
        """ルートノード以下のバインドに必要なジョイントを返す

        Returns:
            list: _description_
        """
        self.get_need_joints()
        return self.need_joints

    def get_selected_joints(self)->list:
        """選択からメッシュを抽出して返す

        Returns:
            list: _description_
        """
        return self.need_joints

    def get_mesh_joint_from_selection(self):
        """選択からメッシュシェイプを抽出して返す

        Returns:
            _type_: _description_
        """
        selections = cmds.ls(selection=True, type="transform", long=True)
        joints = []
        meshes = []

        if not selections:
            return joints, meshes

        for selection in selections:
            shapes = cmds.listRelatives(selections, children=True, type="mesh", fullPath=True, noIntermediate=True)
            if shapes:
                shape = [x for x in shapes if not cmds.getAttr("{}.intermediateObject".format(x))][0]
                meshes.append(shape)
            elif cmds.nodeType(shape) == "joint":
                joints.append(selection)

        return joints, meshes

    def select_node(self, select_node_type:str="need_joint", add_selection:bool=False):
        """ノードの選択

        Args:
            select_node_type (str, optional): _description_. Defaults to "need_joint".
        """
        _nodes = []

        if select_node_type == "all_joint" and self.all_joints:
            _nodes = self.all_joints
            # cmds.select(self.all_joints, replace=True)
        elif select_node_type == "need_joint" and self.need_joints:
            _nodes = self.need_joints
            # cmds.select(self.need_joints, replace=True)
        elif select_node_type == "transform" and self.need_transform_meshes:
            _nodes = list(self.need_transform_meshes.keys())
            # cmds.select(list(self.need_transform_meshes.keys()), replace=True)
        elif select_node_type == "mesh" and self.need_transform_meshes:
            _nodes = list(self.need_transform_meshes.values())
            # cmds.select(list(self.need_transform_meshes.values()), replace=True)
        elif select_node_type == "transform and joint" and self.need_joints and self.need_transform_meshes:
            _nodes = self.need_joints + list(self.need_transform_meshes.keys())
            # cmds.select(self.need_joints + list(self.need_transform_meshes.keys()), replace=True)

        if _nodes:
            if add_selection:
                cmds.select(_nodes, add=True)
            else:
                cmds.select(_nodes, replace=True)
        else:
            cmds.select(clear=True)

def transfer_weight_lods(
                        lod_flag:bool=True,
                        project:str = "",
                        surfaceAssociation:str='closestPoint',
                        influenceAssociation:str='closestJoint',
                        normalize:bool=True
                        )->None:
    """LODの命名規則に沿ったウェイト転送
    """
    _node_selection = NodeSelections(project=project)
    need_transform_meshes = _node_selection.get_need_transform_by_weight_transfer_lod()

    if lod_flag:
        lod0_grpup_nodes = _node_selection.get_lod0_nodes()
    else:
        lod0_grpup_nodes = _node_selection.get_lod0_nodes_from_selection()

    lod_length = _node_selection.get_lod_length()
    other_lod_group = _node_selection.lod_root_group

    if not need_transform_meshes:
        conform_dialog(message="No Meshes")
        return
    if not lod0_grpup_nodes:
        conform_dialog(message="There is no lod")
        return

    _length = len(lod0_grpup_nodes)
    _count = 0

    with gui_util.ProgressDialog(title='Transfer Weight', message="Transfer Weight ...", maxValue=_length) as prg:
        for transform, mesh in lod0_grpup_nodes.items():
            QtCore.QCoreApplication.processEvents()
            if prg.wasCanceled():
                break
            for _lodgroup in other_lod_group:
                _transforms = cmds.listRelatives(_lodgroup, allDescendents=True, type='transform', path=True)
                if not _transforms:
                    continue
                for lod_transform in _transforms:
                    if cmds.getAttr("{}.intermediateObject".format(lod_transform)):
                        continue

                    lodnum:str = _lodgroup[-1]
                    if not lodnum.isdecimal():
                        continue

                    replace_name = lod_transform.replace(f'lod{lodnum}', 'lod0')

                    if replace_name != transform:
                        continue
                    child = cmds.listRelatives(lod_transform, children=True, type='mesh', fullPath=True)[0]
                    src_skin_cluster = get_skin_cluster(mesh)
                    dst_skin_cluster = get_skin_cluster(child)
                    joints = cmds.skinCluster(src_skin_cluster, q=True, influence=True)

                    if not dst_skin_cluster:
                        dst_skin_cluster = create_skin_cluster(joints=joints, node=child)
                    else:
                        add_influence(skin_cluster=dst_skin_cluster, joints=joints)

                    if surfaceAssociation == "UVSpace":
                        src_uv = cmds.polyUVSet(mesh, allUVSets=True, q=True)
                        if src_uv:
                            src_uv = src_uv[0]
                        else:
                            src_uv = None

                        dst_uv = cmds.polyUVSet(mesh, allUVSets=True, q=True)
                        if dst_uv:
                            dst_uv = dst_uv[0]
                        else:
                            dst_uv = None
                        result = weight_copy_uv(
                            src=src_skin_cluster,
                            dst=dst_skin_cluster,
                            src_uv=src_uv,
                            dst_uv=dst_uv,
                            influenceAssociation=influenceAssociation,
                            normalize=normalize
                            )
                    else:
                        result = weight_copy(
                            src=src_skin_cluster,
                            dst=dst_skin_cluster,
                            surfaceAssociation=surfaceAssociation,
                            influenceAssociation=influenceAssociation,
                            normalize=normalize
                        )
            _count += 1
            prg.setValue(_count)
            prg.step(_count)

def select_all_joints(project:str="", add_selection:bool=False):
    """ルートノード以下の全ジョイント選択
    """
    _node_selection = NodeSelections(project=project)
    _node_selection.select_all_joints(add_selection=add_selection)

def select_need_joints(project:str = "", add_selection:bool=False):
    """ルートノード以下のスキニングに必要なジョイント選択
    """
    _node_selection = NodeSelections(project=project)
    _node_selection.select_need_joints(add_selection=add_selection)

def select_need_transforms(project:str = "", ignore_lod_flag:bool=False, add_selection:bool=False):
    """ルートノード以下のトランスフォームノード、メッシュシェイプの辞書から
    トランスフォームノードを選択

    Args:
        ignore_lod_flag (bool, optional): _description_. Defaults to False.
    """
    _node_selection = NodeSelections(project=project)
    _node_selection.select_need_transform_meshes(ignore_lod_flag=ignore_lod_flag, add_selection=add_selection)

def select_need_transform_and_joint(project:str = "", ignore_lod_flag:bool=False, add_selection:bool=False):
    """ルートノード以下のトランスフォームノード、メッシュシェイプの辞書から
    トランスフォームノードとジョイントを選択

    Args:
        ignore_lod_flag (bool, optional): _description_. Defaults to False.
    """
    _node_selection = NodeSelections(project=project)
    _node_selection.select_need_transform_and_joint(ignore_lod_flag=ignore_lod_flag, add_selection=add_selection)

def set_joint_preferred_angles(joint:str=""):
    """ジョイントのpreferred_anglesを復元

    Args:
        joint (str, optional): _description_. Defaults to "".
    """
    if not joint:
        return
    cmds.joint(joint, edit=True, setPreferredAngles=True, children=True)

def check_nema_space(nodes:list=[]):
    if not nodes:
        return
    # print("^^^^^^^^^^^^")
    # print(nodes)
    result_nodes = []
    remap = ''
    for node in nodes:
        exists = False
        # print(node)
        # print(cmds.objExists(node))
        if not cmds.objExists(node):
            if ':' in node:
                _name_split = node.split(':')
                not_ns_name = _name_split[-1]
                if cmds.objExists(not_ns_name):
                    exists = True
                    result_nodes.append(_name_split[-1])
                    if not remap:
                        remap = _name_split[0]
        else:
            exists = True
        if exists:
            result_nodes.append(node)
    return result_nodes if result_nodes else nodes, remap


def bind_metahuman(mesh_influence:dict=[]):
    # if not mesh_influence:
    #     return
    # _node_selection = NodeSelections(project='')
    # lod_group_mesh = _node_selection.get_metahuman_lodgroups()
    _length = len(mesh_influence)
    # print("_length --  ", _length)
    with gui_util.ProgressDialog(title='Bind Skin', maxValue=_length) as prg:
        QtCore.QCoreApplication.processEvents()
        for i,(mesh, _joints) in enumerate(mesh_influence.items()):
            _joints, remap_flag = check_nema_space(nodes=_joints)
            # _joints = load_config('MetahumanLOD_influence').get(f'lod{i}', None)
            # print(_joints)
            # if not _joints:
            #     continue
            mesh_short_name = mesh.rsplit('|', 1)[-1]
            # print(i, " ----------------------------i")
            # print(mesh)
            # print(mesh_short_name, cmds.objExists(mesh_short_name))
            # print(_joints)

            if prg.wasCanceled():
                break

            # if not cmds.objExists(mesh_short_name):
            #     continue
            # else:
            target_nodes = cmds.ls(mesh_short_name, type='mesh')
            # print(target_nodes, " ---------- target_nodes")
            if len(target_nodes) != 1:
                continue

            skin_cluster = get_skin_cluster(mesh)
            # print("skin_cluster  ------  ", skin_cluster)
            if skin_cluster:
                continue

            skin_cluster = cmds.skinCluster(
                                        _joints,
                                        mesh_short_name,
                                        toSelectedBones=True,
                                        bindMethod=0,
                                        normalizeWeights=True,
                                        weightDistribution=0,
                                        maximumInfluences=12,
                                        obeyMaxInfluences=False,
                                        dropoffRate=4,
                                        removeUnusedInfluence=False,
                                        name='{}_skinCluster'.format(mesh_short_name)
                                        )
            cmds.setAttr(f'{mesh_short_name}_skinCluster.maintainMaxInfluences', 1)
            prg.step(i)


def _bind_metahuman(joints:list=[], meshes:list=[]):
    # if not joints or not meshes:
    #     return
    _node_selection = NodeSelections(project='')
    lod_group_mesh = _node_selection.get_metahuman_lodgroups()
    _length = len(lod_group_mesh)
    with gui_util.ProgressDialog(title='Bind Skin', maxValue=_length) as prg:
        for i,(lod_group, meshes) in enumerate(lod_group_mesh.items()):
            print(lod_group)
            _joints = load_config('MetahumanLOD_influence').get(f'lod{i}', None)
            print(_joints)
            if not _joints:
                continue

            if prg.wasCanceled():
                break
            for mesh in meshes:
                print(mesh)
                skin_cluster = get_skin_cluster(mesh)
                if skin_cluster:
                    continue

                skin_cluster = cmds.skinCluster(
                                            _joints,
                                            mesh,
                                            toSelectedBones=True,
                                            bindMethod=0,
                                            normalizeWeights=True,
                                            weightDistribution=0,
                                            maximumInfluences=12,
                                            obeyMaxInfluences=False,
                                            dropoffRate=4,
                                            removeUnusedInfluence=False,
                                            name='{}_skinCluster'.format(mesh)
                                            )
                cmds.setAttr(f'{mesh}_skinCluster.maintainMaxInfluences', 1)
            prg.step(i)

def create_skin_cluster(joints:list=[], node:str='', max_influences=12):
    skin_cluster_base_name = node.rsplit("|", 1)[-1]
    skin_cluster = cmds.skinCluster(
                                joints,
                                node,
                                toSelectedBones=True,
                                bindMethod=0,
                                normalizeWeights=True,
                                weightDistribution=0,
                                maximumInfluences=max_influences,
                                obeyMaxInfluences=False,
                                dropoffRate=4,
                                removeUnusedInfluence=False,
                                name='{}_skinCluster'.format(skin_cluster_base_name)
                                )[0]
    cmds.setAttr(f'{skin_cluster}.maintainMaxInfluences', 1)
    set_joint_preferred_angles(joints[-1])
    set_joint_color(joints[-1])
    return skin_cluster

def bind_skin(project:str="", bind_type:str="auto", max_influences=12, ignore_lod_flag:bool=False):
    """スムースバインド実行

    Args:
        bind_type (str, optional): _description_. Defaults to "auto".
        max_influences (int, optional): _description_. Defaults to 4.
        ignore_lod_flag (bool, optional): _description_. Defaults to False.
    """
    _node_selection = NodeSelections(project=project)
    selections = cmds.ls(selection=True, type="transform", long=True)

    if bind_type == "auto":
        _mesh_transforms = _node_selection.get_bind_need_mesh_transforms(ignore_lod_flag=False)
        _joints = _node_selection.get_bind_need_joints()
    else:
        _mesh_transforms = _node_selection.get_bind_need_mesh_transforms_from_selection()
        _joints = _node_selection.get_selected_joints()

    if not _mesh_transforms:
        conform_dialog(message="No Meshes")
        return

    if not _joints:
        conform_dialog(message="No Jooints")
        return

    # 複数のバインドポーズ対応のためコメントアウト
    # if [x for x in cmds.listHistory(_mesh_transforms)if cmds.nodeType(x) == "skinCluster"]:
    #     conform_dialog(message="Already skinned")
    #     return

    _length = len(_mesh_transforms)

    with gui_util.ProgressDialog(title='Bind Skin', maxValue=_length) as prg:
        for i, node in enumerate(_mesh_transforms):
            shortName = node.rsplit("|", 1)[-1]

            if prg.wasCanceled():
                break

            bb_size = cmds.polyEvaluate(node, boundingBox=True, accurateEvaluation=True)

            if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
                continue

            if not cmds.getAttr("{}.v".format(node)):
                continue

            skin_cluster = get_skin_cluster(node)
            if skin_cluster:
                continue
            skin_cluster = create_skin_cluster(joints=_joints, node=node, max_influences=max_influences)
            # skin_cluster = cmds.skinCluster(
            #                             _joints,
            #                             node,
            #                             toSelectedBones=True,
            #                             bindMethod=0,
            #                             normalizeWeights=True,
            #                             weightDistribution=0,
            #                             maximumInfluences=max_influences,
            #                             obeyMaxInfluences=False,
            #                             dropoffRate=4,
            #                             removeUnusedInfluence=False,
            #                             name='{}_skinCluster'.format(shortName)
            #                             )
            # cmds.setAttr(f'{shortName}_skinCluster.maintainMaxInfluences', 1)

            prg.step(i)

    # set_joint_preferred_angles(_joints[-1])
    # set_joint_color(_joints[-1])

    if selections:
        cmds.select(selections, replace=True)
    else:
        cmds.select(clear=True)

def obj_exists(node:str='')->bool:
    return cmds.objExists(node)

def get_short_path_mesh_node_names(nodes:list=[])->list:
    if not nodes:
        return
    return cmds.ls(nodes, shortNames=True)

def get_full_path_mesh_node_names(nodes:list=[])->list:
    """フルパスを返す

    Args:
        nodes (list, optional): _description_. Defaults to [].

    Returns:
        _type_: _description_
    """
    if not nodes:
        return
    return cmds.ls(nodes, long=True)

def get_mesh_shape_node(nodes:list=[], long_name:bool=True):
    """mesh node から中間オブジェクトを抜かして返す

    Args:
        nodes (list): maya mesh nodes

    Returns:
        [list]: maya mesh nodes
    """
    meshes = []
    if not nodes:
        return

    if long_name:
        meshes = cmds.listRelatives(nodes, children=True, type="mesh", fullPath=True)
    else:
        meshes = cmds.listRelatives(nodes, children=True, type="mesh", path=True)

    if meshes:
        meshes = [x for x in meshes if x and not cmds.getAttr("{}.intermediateObject".format(x))]

    return meshes

def get_meshes(long_name:bool=True):
    """選択トランスフォームノードからメッシュを取り出す

    Returns:
        [list]: mesh node list
    """
    sel = cmds.ls(selection=True, type="transform")

    if not sel:
        return
    meshes = get_mesh_shape_node(sel, long_name=long_name)

    if not meshes:
        return
    return meshes

def delete_joint_history(joints):
    """骨に対してヒストリの削除、

    Args:
        joints ([type]): [description]
    """
    for j in joints:
        if cmds.lockNode(j, q=True, lock=True):
            continue
        cmds.delete(j, ch=True)
        # if cmds.getAttr("{}.useObjectColor".format(j)):
        #     cmds.setAttr("{}.useObjectColor".format(j), 0)

def check_joints():
    """cyllista の補助骨はGotoBindPose ができないので
    予め存在を確認

    Returns:
        _type_: _description_
    """
    _helper_flag = False
    joints = cmds.ls(type='joint', long=True)
    if not joints:
        return _helper_flag

    # ジョイントを階層が深い順にソート
    joints = sorted(joints, key=lambda x:len(x.split("|")), reverse=True)
    for _j in joints:
        if 'helper' in _j.rsplit('|')[-1]:
            _helper_flag = True
    return _helper_flag

def reset_joint_rotation():
    """joint に設定されたpreferredAngleを設定し
    バインドポーズに戻す
    """
    joints = cmds.ls(type="joint", long=True)
    _axis = ["X", "Y", "Z"]
    if not joints:
        return
    for joint in joints:
        _connection_flag = False
        _rot = cmds.getAttr(f'{joint}.preferredAngle')[0]
        for axis in _axis:
            if cmds.getAttr(f'{joint}.rotate{axis}', lock=True):
                _connection_flag = True
                break
            if cmds.listConnections(f'{joint}.rotate{axis}', destination=True):
                _connection_flag = True
                break
        if _connection_flag:
            continue
        try:
            cmds.setAttr(f'{joint}.rotate', _rot[0], _rot[1], _rot[2], type="double3")
        except Exception as e:
            print(e)

def go_to_bindpose(selection_only:bool=False):
    """mel の go to bind を模倣

    Args:
        nodes (list): transform nodes
    """
    if check_joints():
        _m = 'helper joint could not Goto Bindpose'
        conform_dialog(message=_m)
        return

    if selection_only:
        nodes = cmds.ls(selection=True, type="transform", long=True)
    else:
        nodes = cmds.ls(type="transform", long=True)

    if not nodes:
        return
    bind_store = []
    _error = False

    for node in nodes:
        if _error:
            break

        bindPose = cmds.dagPose(node, q=True, bindPose=True)

        if bindPose and len(bindPose) == 1:
            try:
                cmds.dagPose(node, restore=True, g=True, bindPose=True)
            except Exception as e:
                _error = True
                break
            continue
        else:

            historys = cmds.listHistory(node)
            skin_cluster = [x for x in historys if cmds.nodeType(x) == "skinCluster"]

            if not skin_cluster:
                continue
            skin_cluster = skin_cluster[0]
            skinBindPosePlug = skin_cluster + ".bindPose"

            bindPose = cmds.listConnections(skinBindPosePlug,
                                            destination=False,
                                            source=True,
                                            type='dagPose')

            if bindPose:
                bindPose = bindPose[0]
                if bindPose in bind_store:
                    continue
                bind_store.append(bindPose)
                try:
                    cmds.dagPose(bindPose, restore=True, g=True)
                except Exception as e:
                    print(e)
            else:
                influences = cmds.skinCluster(skin_cluster, q=True, influence=True)
                for inf in influences:
                    bindPose = cmds.dagPose(inf, q=True, bindPose=True)
                    if not bindPose:
                        continue

                    bindPose = bindPose[0]
                    if bindPose in bind_store:
                        continue
                    bind_store.append(bindPose)
                    try:
                        cmds.dagPose(bindPose, restore=True, g=True)
                    except Exception as e:
                        print(e)

def unbind_skin(nodes=[], joints=[]):
    """バインドの解除、ノードに対して解除、ジョイントに対してヒストリの削除

    Args:
        nodes ([type]): [description]
        joints ([type]): [description]
    """

    delete_joint_history(joints)
    _length = len(nodes)

    with gui_util.ProgressDialog(title='Un Bind Skin', maxValue=_length) as prg:
        for i, node in enumerate(nodes):
            if prg.wasCanceled():
                break

            historys = cmds.listHistory(node)

            if [x for x in historys if cmds.nodeType(x) == "skinCluster"]:
                cmds.skinCluster(node, e=True, unbind=True)
                # cmds.bindSkin(node, unbind=True)
            prg.step(i)

    bindPose = cmds.ls(type="dagPose")
    if bindPose:
        for bp in bindPose:
            if cmds.lockNode(bp, q=True, lock=True):
                continue
            try:
                cmds.delete(bindPose)
            except Exception as e:
                print(e)

def unbind_skin_selections():
    selections = cmds.ls(selection=True, long=True)
    if not selections:
        return

    with gui_util.ProgressDialog(title='Unbind', message="UnBindSKin ...", maxValue=len(selections)) as prg:
        for i, sel in enumerate(selections):
            mesh = cmds.listRelatives(sel, children=True, type="mesh", fullPath=True)
            prg.step(i)
            if prg.wasCanceled():
                break
            if not mesh:
                continue
            historys = cmds.listHistory(mesh)
            skin_cluster = [x for x in historys if cmds.nodeType(x) == "skinCluster"]
            if not skin_cluster:
                continue
            cmds.skinCluster(skin_cluster, edit=True, unbind=True)


def unbind_skin_preprocess(only_selection:bool=False):
    """バインド解除
    """
    _flag = False
    joints = cmds.ls(type="joint", long=True)
    _m = ''
    if not joints:
        _m += 'No required joint'

    nodes = cmds.ls(type="mesh", long=True)
    if not nodes:
        if _m:
            _m += '\n'
        _m += 'No required mesh'

    if _m:
        conform_dialog(message=_m)
        return

    try:
        go_to_bindpose()
        _flag = True
    except Exception as e:
        print(e)

    if _flag:
        unbind_skin(nodes=nodes, joints=joints)

def set_weight_zero(mesh, skinCluster):
    """ウェイトに強制的に0 を割り当て

    Args:
        mesh ([type]): [description]
        skinCluster ([type]): [description]
    """
    sel_list = om2.MSelectionList()
    sel_list.add(mesh)

    dag_path = sel_list.getDagPath(0)
    mesh_fn = om2.MFnMesh(dag_path)

    skinNode = om2.MGlobal.getSelectionListByName(skinCluster).getDependNode(0)
    skinFn = om2anim.MFnSkinCluster(skinNode)

    indices = range(mesh_fn.numVertices)
    fnCompNew = om2.MFnSingleIndexedComponent()
    vertexComp = fnCompNew.create(om2.MFn.kMeshVertComponent)
    fnCompNew.addElements(indices)

    infDags = skinFn.influenceObjects()
    infIndices = om2.MIntArray(len(infDags), 0)
    shape = len(infDags)

    for x in range(shape):
        infIndices[x] = x

    set_weights = [0.0] * (len(indices) * shape)
    skinFn.setWeights(dag_path, vertexComp, infIndices, om2.MDoubleArray(set_weights), False)

def get_polygon_shell(node:str='', uv_pin:bool=False):
    """ポリゴンシェル（ポリゴンアイランド）のリストごとに
    ポリゴンIDがリストで入る

    Args:
        node ([str]): maya_mesh_node

    Returns:
        [list]: [[0, 1], [2, 3]]
    """
    island_list = []

    for i in range(cmds.polyEvaluate(node, face=True)):
        _li = list(set(cmds.polySelect(node, q=True, extendToShell=i, noSelection=True)))
        if not island_list:
            island_list = [_li]
        elif _li not in island_list:
            island_list = island_list + [_li]

    vertex_id_list:list = []
    vtx_list:list = []

    for island_faceids in island_list:
        v_value_max = 0.0
        v_value_dict = {}

        _vtx_list = []
        _vtx_v_value_list = []
        _vtx_id_list = []

        for island_faceid in island_faceids:
            face_name = f'{node}.f[{island_faceid}]'
            for vtx in cmds.filterExpand(cmds.polyListComponentConversion(face_name, toVertex=True), selectionMask=31):
                vtx_id = int(vtx.rsplit('[', 1)[-1][:-1])
                _uvs = cmds.filterExpand(cmds.polyListComponentConversion(vtx, toUV=True), selectionMask=35)
                if not _uvs:
                    continue
                for _uv in _uvs:
                    v_value = round(cmds.polyEditUV(_uv, q=True)[-1], 4)
                    _vtx_list.append(vtx)
                    _vtx_v_value_list.append(v_value)
                    _vtx_id_list.append(vtx_id)

                    # print(vtx, _uv)
                    # print(v_value)
                    # if uv_pin and v_value_max <= v_value:
                    #     v_value_max = v_value
                    #     vertex_id_list.append(vtx_id)
                        # print("-------------------------------")
                        # print(vtx)
                        # print(v_value)
                        # vtx_list.append(vtx)
        # print("============================")
        # print(zip(_vtx_list, _vtx_v_value_list))
        # print(_vtx_list)
        # print(_vtx_v_value_list)
        # max_v_vtxs = [vtx for i, (value, vtx) in enumerate(zip(_vtx_v_value_list, _vtx_list)) if value == max(_vtx_v_value_list)]
        # if uv_pin and max_v_vtxs:
        #     vtx_list.extend(max_v_vtxs)
        max_v_vtx_ids = [vtx for i, (value, vtx) in enumerate(zip(_vtx_v_value_list, _vtx_id_list)) if value == max(_vtx_v_value_list)]
        if uv_pin and max_v_vtx_ids:
            vertex_id_list.extend(max_v_vtx_ids)
        # print(max_v_vtxs)
        # for v, _v in zip(_vtx_list, _vtx_v_value_list):
        #     print(v, _v)
    # cmds.select(vtx_list, replace=True)
    return island_list, vertex_id_list

def save_weight_file_cmds(shape="",
                        export_path="",
                        file_name="",
                        deformer="",
                        remap="",
                        number_of_digit=8,
                        ):
    """ウェイトの書き出し

    Args:
        shape (str): mesh node name
        export_path (str): file path
        file_name (str): file name
        scene_basename (str): scene name
        deformer (str): パターンを使用する場合
    """

    # number_of_digit の桁数を元に
    # .00000001 を生成
    _zero = 0
    tolerance = float(f'.{_zero:0<{number_of_digit-1}}1')
    # print("tolerance --- ", tolerance)

    # try:
    cmds.deformerWeights(
                        file_name,
                        export = True,
                        shape = shape,
                        # deformer = deformer,
                        path = export_path,
                        positionTolerance=1,
                        # method = method,
                        # weightPrecision = number_of_digit,
                        # defaultValue = -1.0,
                        weightTolerance = tolerance,
                        vertexConnections = True,
                        worldSpace=True,
                        )
    # except Exception as e:
    #     cmds.warning(f'Could not import: {e}')


def load_weight_file_cmds(shape= "",
                        import_path="",
                        file_name="",
                        deformer="",
                        method="index",
                        remap=""):
    """ウェイトファイル読み込み
    Maya 標準機能を使った

    Args:
        shape (str): mesh node name
        import_path (str): file path
        file_name (str): file name
        scene_basename (str): scene name
        deformer (str): パターンを使用する場合
        method (str): メソッドここでは index のみ

    Returns:
        [type]: [description]
    """

    # print("remap ---- ", remap)
    # print(f"{remap}:(.*);$1")
    if remap:
        try:
            cmds.deformerWeights(
                                file_name,
                                im = True,
                                shape = shape,
                                # deformer = deformer,
                                path = import_path,
                                method = method,
                                # weightPrecision = 10,
                                defaultValue = 0.0,
                                ignoreName = False,
                                vertexConnections=True,
                                worldSpace=True,
                                remap=f"{remap}:(.*);$1"
                                # positionTolerance=0.1
                                )
        except Exception as e:
            cmds.warning(f'Could not import: {e}')
    else:
        cmds.deformerWeights(
                    file_name,
                    im = True,
                    shape = shape,
                    # deformer = deformer,
                    path = import_path,
                    method = method,
                    # weightPrecision = 10,
                    defaultValue = 0.0,
                    ignoreName = False,
                    vertexConnections=True,
                    worldSpace=True,
                    # positionTolerance=0.1
                    )
    return True


def save_weight_data(directory:str, meshes:list, number_of_digit:int=8):
    """ウェイトデータ保存

    Args:
        directory (str): _description_
        meshes (list): _description_
    """

    if not check_path_exists(directory, make_dir=True):
        return

    _length = len(meshes)
    _error_flag = _length

    scene_joint_shortname:list = [x.rsplit('|', 1)[-1] for x in cmds.ls(type='joint')]
    warning_meshes:dict ={}
    Warning_joints:list = []
    remap = ''
    with gui_util.ProgressDialog(title='Export Weight', message="Export Weight ...", maxValue=_length) as prg:
        QtCore.QCoreApplication.processEvents()
        for i, mesh in enumerate(meshes):

            prg.step(i)

            if prg.wasCanceled():
                break

            skin_cluster = get_skin_cluster(mesh)
            if not skin_cluster:
                continue

            joints = cmds.skinCluster(skin_cluster, influence=True, q=True)
            for joint in joints:
                joint_short_name = joint.rsplit('|', 1)[-1]
                _exies = cmds.ls(joint_short_name, type='joint')
                if len(_exies) != 1 and joint_short_name not in Warning_joints:
                    Warning_joints.append(joint_short_name)

            # joints, remap = check_nema_space(nodes=joints)

            exchange_name = mesh.replace('|', '__').replace(':', '_')
            file_name = f'{exchange_name}{WEIGHT_FILE_FORMAT[PROJECT_WEIGHT_FILE_FORMAT]}'

            mesh_short_name = cmds.ls(mesh, shortNames=True)[0]

            save_weight_file_cmds(
                                shape=mesh_short_name,
                                export_path=directory,
                                file_name=file_name,
                                deformer=skin_cluster,
                                remap=remap,
                                number_of_digit=number_of_digit
                                )
            _error_flag -= 1

    # _count_success(_length, _error_flag, _prefix="Export")

    if Warning_joints:
        _joints = ', '.join(Warning_joints)
        _m = f'There are duplication joints: [ { _joints} ] '
        conform_dialog(message=_m)


def load_weight_data(meshes=[], weightFilePaths=[], method="index", error_nodes=[], normalize=False):
    """ウェイトデータ読み込み

    Args:
        meshes (list, optional): _description_. Defaults to [].
        weightFilePaths (list, optional): _description_. Defaults to [].
        method (str, optional): _description_. Defaults to "index".
        normalize (bool, optional): _description_. Defaults to False.
    """
    if error_nodes:
        _m = ', '.join(error_nodes)
        conform_dialog(message=f"Multiple nodes exist: \n[ {_m} ]")
        return

    _length = len(meshes)
    _error_flag = _length
    remap = ''

    with gui_util.ProgressDialog(title='Import Weight', message="Import Weight ...", maxValue=_length) as prg:
        QtCore.QCoreApplication.processEvents()
        for i,(mesh, weight_file_path) in enumerate(zip(meshes, weightFilePaths)):
            print(mesh, " ----")
            if prg.wasCanceled():
                break
            # mesh_short_name = mesh.rsplit('|')[-1]
            mesh_short_name = cmds.ls(mesh, shortNames=True)[0]
            skin_cluster = get_skin_cluster(mesh)

            if not weight_file_path.exists():
                continue

            tree = ET.parse(weight_file_path)
            root = tree.getroot()
            joints = [x.attrib.get('source') for x in root]

            if joints:
                joints = [x for x in joints if x]
                joints, remap = check_nema_space(nodes=joints)

            if not skin_cluster:
                skin_cluster = create_skin_cluster(joints=joints, node=mesh)

            elif joints:
                add_influence(skin_cluster=skin_cluster, joints=joints)

            _message = f'import weight: [ {mesh} ]'

            prg.setLabelText(_message)
            set_weight_zero(mesh=mesh, skinCluster=skin_cluster)
            load_weight_file_cmds(
                                shape=mesh_short_name,
                                import_path="",
                                file_name=weight_file_path,
                                deformer="",
                                method=method,
                                remap=remap,
                                )
            if normalize:
                cmds.skinCluster(skin_cluster, edit=True, forceNormalizeWeights=True)
            _error_flag -= 1
            prg.step(i+1)

    # _count_success(_length, _error_flag, _prefix='Import')

def get_boundary_one_vtx(node_name:str='', polygon_shell:list=[], max_vvalue_vid:list=[]):
    """入力されたポリゴンシェルの境界にある一つの頂点と
    ポリゴンシェルの全頂点のリスト、抽出した一つの頂点の位置を返す

    Args:
        node_name (str): maya mesh node
        polygon_shell (list): polygon face ids

    Returns:
        _id [int]: 境界にある一つの頂点
        all_vtx [list]: ポリゴンシェルの頂点ID
        _position [MPoint]: 一つの頂点の場所
    """
    all_vtx = []
    _id = None
    _position = None

    selection = om2.MSelectionList()
    selection.add(node_name)
    dag_path = selection.getDagPath(0)
    space = om2.MSpace.kWorld
    mitMeshPolygonIns = om2.MItMeshPolygon(dag_path)

    for n in polygon_shell:
        mitMeshVertIns = om2.MItMeshVertex(dag_path)
        mitMeshPolygonIns.setIndex(n)
        vids = mitMeshPolygonIns.getVertices()
        all_vtx.extend(vids)

        for v in vids:
            if max_vvalue_vid and v not in max_vvalue_vid:
                continue
            mitMeshVertIns.setIndex(v)
            if mitMeshVertIns.onBoundary():
                _id = v
                _position = mitMeshVertIns.position(space)
                boundry_flag = True
                break

    return _id, list(set(all_vtx)), _position


def set_weight_data_vtx(node_name:str, weights:om2.MDoubleArray, vtx_id:list):
    """1頂点のウェイト値を vtx_id 全てに適用

    Args:
        node_name (str): maya_mesh_node
        weights (MDoubleArray): weight data
        vtx_id (list): vertex ids
    """
    selection = om2.MSelectionList()
    selection.add(node_name)

    dag_path = selection.getDagPath(0)
    fullPathName = dag_path.fullPathName()

    skinCluster = cmds.ls(cmds.listHistory(fullPathName), type='skinCluster')

    skinNode = om2.MGlobal.getSelectionListByName(skinCluster[0]).getDependNode(0)
    skinFn = om2anim.MFnSkinCluster(skinNode)

    fnCompNew = om2.MFnSingleIndexedComponent()
    vertexComp = fnCompNew.create(om2.MFn.kMeshVertComponent)
    fnCompNew.addElements(vtx_id)

    infDags = skinFn.influenceObjects()

    shape = len(infDags)
    infIndices = om2.MIntArray(shape, 0)

    for x in range(shape):
        infIndices[x] = x

    set_weights = []

    for i in vtx_id:
        set_weights.extend(weights)

    skinFn.setWeights(dag_path, vertexComp, infIndices, om2.MDoubleArray(set_weights), False)


def get_weight_data_vtx(node_name:str="", vtx_id:int=0):
    """1 頂点の生のウェイトデータだけを取って返す

    Args:
        node_name (str)): maya_mesh_node
        vtx_id (int): vertex id

    Returns:
        [MDoubleArray]: weignt data
    """
    selection = om2.MSelectionList()
    selection.add(node_name)

    dag_path = selection.getDagPath(0)
    fullPathName = dag_path.fullPathName()

    skinCluster = cmds.ls(cmds.listHistory(fullPathName), type='skinCluster')

    skinNode = om2.MGlobal.getSelectionListByName(skinCluster[0]).getDependNode(0)
    skinFn = om2anim.MFnSkinCluster(skinNode)

    indices = [vtx_id]
    fnCompNew = om2.MFnSingleIndexedComponent()
    vertexComp = fnCompNew.create(om2.MFn.kMeshVertComponent)
    fnCompNew.addElements(indices)

    weights = skinFn.getWeights(dag_path, vertexComp)[0]

    return weights

def add_influence(skin_cluster:str='', joints:list=[]):
    _length = len(joints)
    _count = 0
    _flag = True

    cmds.setAttr(f'{skin_cluster}.maintainMaxInfluences', 1)
    with gui_util.ProgressDialog(title='Add Influence', message="Add Influence ...", maxValue=_length) as prg:
        QtCore.QCoreApplication.processEvents()
        for joint in joints:
            _count += 1
            if not joint:
                continue
            _joint = cmds.ls(joint)
            if len(_joint) != 1:
                continue
            if prg.wasCanceled():
                break
            if joint not in cmds.skinCluster(skin_cluster, influence=joint, q=True):
                _flag = True
                cmds.skinCluster(skin_cluster, edit=True, useGeometry=True, polySmoothness=0.0, lockWeights=True, weight=0.0, addInfluence=joint)
                cmds.skinCluster(skin_cluster, influence=joint, e=True, lockWeights=False)
            prg.setValue(_count)
            prg.step(_count)
    # set_joint_preferred_angles(joints[-1])

def add_influence_skincluster(src_skin_cluster:str='', dst_skin_clusters:list=[]):
    joints = cmds.skinCluster(src_skin_cluster, influence=True, q=True)

    for dst_skin_cluster in dst_skin_clusters:
        add_influence(skin_cluster=dst_skin_cluster, joints=joints)

def transfer_weight(
                openTopology:bool=False,
                normalize:bool=False,
                surfaceAssociation:str='closestPoint',
                influenceAssociation:str='closestJoint',
                uv_value_pin:bool=False,
                ):
    """選択のウェイト転送

    Args:
        openTopology (bool, optional): _description_. Defaults to False.
    """
    selections = cmds.ls(orderedSelection=True, type="transform")
    _m = ''
    if not selections:
        _m = 'Select Transform Node(s)'

    if len(selections) == 1:
        _m = 'Select two or more transform nodes'

    if _m:
        conform_dialog(message=_m)
        return

    src = selections.pop(0)

    src_mesh = get_mesh_shape_node(src)
    dst_meshes = get_mesh_shape_node(selections)
    src_uv = ''
    dst_uvs = []
    could_not_copy = []
    joints:list = []

    if not src_mesh:
        conform_dialog(message='No mesh was found in the copy source')
        return

    src_mesh = src_mesh[0]

    if not dst_meshes:
        conform_dialog(message='No mesh was found at the copy destination')
        return

    src_skin_cluster = get_skin_cluster(src_mesh)
    if not src_skin_cluster:
        conform_dialog(message='There was no skin cluster in the source')
        return

    joints = cmds.skinCluster(src_skin_cluster, influence=True, q=True)
    dst_skin_clusters = []
    for dst_mesh in dst_meshes:
        dst_skin_cluster = get_skin_cluster(dst_mesh)
        # print(dst_skin_cluster, " -----skin_cluster")
        if dst_skin_cluster:
            add_influence(skin_cluster=dst_skin_cluster, joints=joints)
            dst_skin_clusters.append(dst_skin_cluster)
        else:
            joints = cmds.skinCluster(src_skin_cluster, influence=True, q=True)
            dst_skin_cluster = create_skin_cluster(joints=joints, node=dst_mesh)
            dst_skin_clusters.append(dst_skin_cluster)

    if not dst_skin_clusters:
        conform_dialog(message='There were no skin clusters at the target')

    if not src_skin_cluster or not dst_skin_clusters:
        return

    if surfaceAssociation == "UVSpace":
        src_uv = cmds.polyUVSet(src_mesh, allUVSets=True, q=True)
        if src_uv:
            src_uv = src_uv[0]
        else:
            src_uv = None
        for mesh in dst_meshes:
            uvs = cmds.polyUVSet(mesh, allUVSets=True, q=True)
            if uvs:
                dst_uvs.append(uvs[0])
            else:
                dst_uvs.append(None)
        for dst_mesh, dst_skin_cluster, dst_uv in zip(dst_meshes, dst_skin_clusters, dst_uvs):
            _error = weight_copy_uv(
                src=src_skin_cluster,
                dst=dst_skin_cluster,
                src_uv=src_uv,
                dst_uv=dst_uv,
                influenceAssociation=influenceAssociation,
                normalize=normalize
                )
            if _error:
                could_not_copy.append(dst_mesh)

    else:
        for dst_mesh, dst_skin_cluster in zip(dst_meshes, dst_skin_clusters):
            _error = weight_copy(
                src=src_skin_cluster,
                dst=dst_skin_cluster,
                surfaceAssociation=surfaceAssociation,
                influenceAssociation=influenceAssociation,
                normalize=normalize
                )
            if _error:
                could_not_copy.append(dst_mesh)

    if could_not_copy:
        _m = '\n'.join(could_not_copy)
        conform_dialog(message=f"Could not Copy \n[ {could_not_copy} ]")
        return

    if openTopology:
        _exsist_flag = True
        for mesh in dst_meshes:
            # print(mesh, " -------------------")
            # [[0, 1], [2, 3]] アイランドID リスト内に FaceID リスト
            island_ids, max_vvalue_vid = get_polygon_shell(node=mesh, uv_pin=uv_value_pin)
            # print("island_ids ----- ", island_ids)
            # print("max_vvalue_vid -- ", max_vvalue_vid)
            _length = len(island_ids)

            with gui_util.ProgressDialog(title='Progress', message='Weight adjustment in progress ...', maxValue=_length) as prg:
                QtCore.QCoreApplication.processEvents()
                for i, face_ids in enumerate(island_ids):
                    prg.step(i)
                    if prg.wasCanceled():
                        break
                    # 開いた部分の1頂点と、アイランドの全頂点、1頂点のポジション
                    _one, _island_vtx, _position = get_boundary_one_vtx(mesh, face_ids, max_vvalue_vid)
                    # print("_one -- ", _one)
                    # print("_island_vtx -- ", _island_vtx)
                    # print("face_ids -- ", face_ids)
                    # print("i -- ", i)

                    if not isinstance(_one, int) and not _one:
                        _exsist_flag = False
                        continue

                    # インデントに注意
                    # 編集でずれがち
                    _weight = get_weight_data_vtx(mesh, _one)
                    # print(_weight)
                    set_weight_data_vtx(mesh, _weight, _island_vtx)

        # if not _exsist_flag:
        #     conform_dialog(message='Spine shape should be open topology')

        if normalize:
            for dst_skin_cluster in dst_skin_clusters:
                cmds.skinCluster(dst_skin_cluster, edit=True, forceNormalizeWeights=True)


def select_transformknodes(nodes:list=[]):
    """リストウェジットで選択されたノードをMaya で選択

    Args:
        nodes (list, optional): _description_. Defaults to [].
    """
    transform_nodes = []
    for node in nodes:
        transform_node = cmds.listRelatives(node, parent=True, fullPath=True)
        if transform_node:
            transform_node = transform_node[0]
            if cmds.objExists(transform_node):
                transform_nodes.append(transform_node)
    if transform_nodes:
        cmds.select(transform_nodes, replace=True)

def overwrite_confirmation() -> bool:
    _m = 'Do you want to overwrite memory?'
    _d = gui_util.ConformDialogResult(title=TOOL_NAME, message=_m)
    result = _d.exec_()
    if not result:
        return
    else:
        return True

def add_influence_selection():
    selections = cmds.ls(selection=True, type='transform', long=True)

    if not selections:
        return

    joints = []
    meshes = []
    for node in selections:
        if cmds.nodeType(node) == 'joint':
            joints.append(node)
        children = cmds.listRelatives(node, children=True, fullPath=True, type='mesh')
        if children:
            mesh = [x for x in children if x and not cmds.getAttr("{}.intermediateObject".format(x))]
            if mesh:
                meshes.append(mesh[0])

    if not joints or not meshes:
        return

    for mesh in meshes:
        skin_cluster = get_skin_cluster(mesh)

        if not skin_cluster:
            continue

        for joint in joints:
            if joint not in cmds.skinCluster(skin_cluster, influence=joint, q=True):
                try:
                    cmds.skinCluster(skin_cluster, edit=True, useGeometry=True, polySmoothness=0.0, lockWeights=True, weight=0.0, addInfluence=joint)
                    cmds.skinCluster(skin_cluster, influence=joint, e=True, lockWeights=False)
                except Exception as e:
                    print(f'could not attach joint: [ {e} ]')

def get_joint_radius()->float:
    joint_radius = 1.0
    joints = cmds.ls(type='joint')
    if joints:
        joint_radius = cmds.getAttr(f'{joints[0]}.radius')
    return joint_radius

def join_radius_edit(radius:float=1.0)->None:
    joints = cmds.ls(type='joint')
    if not joints:
        return
    for i, joint in enumerate(joints):
        if not cmds.getAttr(f'{joint}.radius', lock=True):
            cmds.setAttr(f'{joint}.radius', radius)
        elif i == 0:
            cmds.warning(f'lock attribute: [ {joint}.radius ]')

def get_bind_nodes()->list:
    meshes = cmds.ls(type='mesh', long=True)
    bindskin_transform_mesh = {}
    joints = []
    mesh_influence = {}

    if not meshes:
        return bindskin_transform_mesh, joints, mesh_influence

    with gui_util.ProgressDialog(
                        title='Progress',
                        message='progress ...',
                        maxValue=len(meshes)) as prg:
        for i, mesh in enumerate(meshes):
            prg.step(i)
            if prg.wasCanceled():
                break
            if cmds.getAttr("{}.intermediateObject".format(mesh)):
                continue
            skin_cluster = get_skin_cluster(mesh)
            if not skin_cluster:
                continue
            parent = cmds.listRelatives(mesh, parent=True, type="transform", fullPath=True)[0]
            bindskin_transform_mesh[parent] = mesh
            _influence = cmds.skinCluster(skin_cluster, q=True, influence=True)
            joints.extend(_influence)
            mesh_influence[mesh] = _influence
    joints = list(set(joints))
    return bindskin_transform_mesh, joints, mesh_influence

def restore_bindpose() -> None:
    joints = cmds.ls(selection=True, type="joint", long=True)

    if not joints:
        cmds.warning('Select Joint')
        return

    bindPose = cmds.dagPose(q=True, bindPose=True)
    root_joints = set()
    root_joint = ''
    for joint in joints:
        for _p in get_parents(joint):
            if cmds.nodeType(_p) == 'joint':
                root_joint = _p
            root_joints.add(_p)

    root_joints = list(root_joints)
    all_joints = cmds.listRelatives(root_joints, allDescendents=True, fullPath=True, type="joint")
    do_restore_bindpose(posees=bindPose, joints=all_joints, old_selections=joints, root_joint=root_joint)

def do_restore_bindpose(posees:list=[], joints:list=[], old_selections:list=[], root_joint:str=''):
    cmds.select(joints, replace=True)
    if not posees:
        new_pose = cmds.dagPose(bindPose=True, save=True, selection=True)
    else:
        pose = posees[0]
        # for pose in posees:
        cmds.delete(pose)
        cmds.dagPose(bindPose=True, save=True, selection=True, name=pose)

    if root_joint:
        set_joint_preferred_angles(joint=root_joint)

    if old_selections:
        cmds.select(old_selections, replace=True)

