# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from pathlib import Path
from PySide2 import QtCore, QtGui, QtWidgets

from maya import cmds

from ...utils import gui_util

import importlib
from . import data
from . import scene_data
from . import setting

DEV_MODE = setting.load_config(config_name='DEV_MODE')
if DEV_MODE:
    importlib.reload(data)
    importlib.reload(scene_data)
    importlib.reload(setting)


HERE = Path(os.path.dirname(os.path.abspath(__file__)))
YAML_FILE_NAME = "settings.yaml"


def open_cyllista_export_window():
    """Cyllista Export Window
    """
    cylModelExporterWindow = None
    try:
        import cylModelExporterWindow
    except Exception as e:
        print(e)


    if cylModelExporterWindow:
        cylModelExporterWindow.show()

def get_check_root_nodes(ignore_check_group_name: list, project_setting:data.ProjectSettings) -> list:
    """カメラを排除したルートノードを取得
    """
    check_root_nodes:list = []
    for node in cmds.ls(assemblies=True):
        shapes = cmds.listRelatives(node, children=True, shapes=True, fullPath=True)
        if shapes and cmds.nodeType(shapes) == 'camera':
            continue
        node_data: data.RootNodeData = get_hierarchical_node_list(
                                                            root_node = node,
                                                            ignore_check_group_name = ignore_check_group_name,
                                                            project_setting = project_setting
                                                            )
        if node_data:
            check_root_nodes.append(node_data)
    return check_root_nodes


def get_dag_hierarchy(node, hierarchy=None, root_node=None, ignore_check_group_name=[]):
    if hierarchy is None:
        hierarchy = []

    children = cmds.listRelatives(node, children=True, fullPath=True, type='transform') or []
    for child in children:
        category_group: str = ''
        has_mesh: bool = False
        is_locator: bool = False

        node_type = cmds.nodeType(child)
        full_path_split_name = child.split('|')
        short_name = full_path_split_name[-1]
        deep = len(full_path_split_name)-1
        shapes = cmds.listRelatives(child, children=True, shapes=True, fullPath=True)

        if len(full_path_split_name) > 2:
            category_group = full_path_split_name[2]
        if ignore_check_group_name:
            if len(full_path_split_name) > 2 and full_path_split_name[2] in ignore_check_group_name:
                continue

        if shapes:
            new_shapes = []
            for shape in shapes:
                number = 0
                shape_full_path_name = shape
                shape_node_type = cmds.nodeType(shape_full_path_name)
                shape_short_name = shape_full_path_name.rsplit('|', 1)[-1]
                shape_deep = len(shape_full_path_name.split('|'))-1
                deep_shapes = []

                if shape_node_type == 'mesh':
                    has_mesh = True
                if shape_node_type == 'locator':
                    is_locator = True
                shepe_data = data.CustomNodeData(
                                        root_node = root_node,
                                        number = number,
                                        full_path_name = shape_full_path_name,
                                        category_group = category_group,
                                        node_type = shape_node_type,
                                        short_name = shape_short_name,
                                        deep = shape_deep,
                                        shapes = deep_shapes,
                                        has_mesh = False,
                                        is_locator = False
                                        )
                new_shapes.append(shepe_data)
            shapes = new_shapes
        else:
            shapes = []

        transform_data = data.CustomNodeData(
                                root_node = root_node,
                                number = 0,
                                full_path_name = child,
                                category_group = category_group,
                                node_type = node_type,
                                short_name = short_name,
                                deep = deep,
                                shapes = shapes,
                                has_mesh = has_mesh,
                                is_locator = is_locator
                                )
        hierarchy.append(transform_data)
        get_dag_hierarchy(child, hierarchy, root_node=root_node, ignore_check_group_name=ignore_check_group_name)

    return hierarchy

def get_hierarchical_node_list(root_node:str, ignore_check_group_name:list, project_setting:data.ProjectSettings) -> data.RootNodeData:
    """node 以下の階層にあるノード情報を集めカスタムクラスに

    Args:
        root_node (data.CustomNodeData, optional): _description_. Defaults to ''.

    Returns:
        data.RootNodeData: _description_
    """
    if not root_node:
        return

    root_node_full_path_name = cmds.ls(root_node, long=True)[0]
    root_node_node_type = cmds.nodeType(root_node_full_path_name)
    root_node_data = data.RootNodeData(
                                node_name = root_node,
                                full_path_name = root_node_full_path_name,
                                node_type = root_node_node_type,
                                project_setting = project_setting
                                )

    _data = get_dag_hierarchy(root_node_full_path_name, root_node=root_node_full_path_name, ignore_check_group_name=ignore_check_group_name)
    if _data:
        root_node_data._all_nodes = _data
    return root_node_data

def get_project_settings(scene_path:str='', lower_drive_letter:bool=False)->data.ProjectSettings:
    projeect_settings = data.ProjectSettings(scene_path=scene_path, lower_drive_letter=lower_drive_letter)
    return projeect_settings


def sort_modules(target_dict:dict, is_list:bool, order:list)->list:
    sorted_keys = sorted(target_dict, key=lambda x: order.index(x) if x in order else len(order))
    sorted_dict = {key: target_dict[key] for key in sorted_keys}
    sorted_list:list = []
    if is_list:
        [sorted_list.extend(target_dict[k]) for k in sorted_dict.keys()]
    else:
        [sorted_list.append(target_dict[k]) for k in sorted_dict.keys()]
    return sorted_list

def get_current_module_import_sentence(current_path:str):
    root_path:str = os.path.abspath(__file__)
    current_directory:str = os.path.dirname(root_path)
    root_directory:str = os.path.abspath(os.path.join(current_directory, '../../../'))
    relative_path = os.path.relpath(current_path, root_directory)
    module_name = relative_path.replace('\\', '.').rsplit('.', 1)[0]
    return module_name

def get_chckermodules()->list:
    sort_directory_dict:dict = {}

    script_path:str = os.path.abspath(__file__)
    script_dir:str = os.path.dirname(script_path)
    _sort_order_directory = setting.load_config('DIRECTORY_SORT_ORDER')
    _sort_order_file = setting.load_config('CHECKER_MODULE_SORT_ORDER')
    # 配置されている場所により変わるので注意
    # モジュールのルートを取得
    # Z:\mtk\tools_ext\maya\2022\modules\mtk\scripts\mtk\file\scene_checker から
    # Z:\mtk\tools_ext\maya\2022\modules\mtk\scripts を取り出している
    root_dir:str = os.path.abspath(os.path.join(script_dir, '../../../'))

    for _iter in HERE.iterdir():
        if _iter.is_dir():
            # _modules:list = []
            _module_dict:dict = {}
            for _iter2 in _iter.iterdir():
                if _iter2.is_file() and not _iter2.stem.startswith('__') and _iter2 not in _module_dict:
                    # relative_path = os.path.relpath(_iter2, root_dir)
                    # module_name = relative_path.replace('\\', '.').rsplit('.', 1)[0]
                    module_name = get_current_module_import_sentence(current_path=_iter2)
                    # print(module_name," -----")
                    # print(get_current_module_import_sentence(current_path=_iter2))
                    # mtk.file.scene_checker.scene.display_layer の形で文字列をリストに追加
                    _module_dict[_iter2.stem] = module_name

            if _module_dict:
                sorted_modules:list = sort_modules(target_dict=_module_dict, is_list=False, order=_sort_order_file)
                sort_directory_dict[_iter.name] = sorted_modules

    sorted_list:list = sort_modules(target_dict=sort_directory_dict, is_list=True, order=_sort_order_directory)

    return sorted_list

def exec_modules(
            action:str='check',
            check_modules:list=[],
            maya_scene_data:scene_data.MayaSceneData=None,
            project_settings:data.ProjectSettings=None,
            modify_data:list=[])->list:

    if not check_modules:
        cmds.warning('Not Found Check Modules')
        return

    if not maya_scene_data:
        cmds.warning('Not Found Check Data')
        return

    if not maya_scene_data.project:
        cmds.warning('Not Found Project Name')
        return

    all_result:list = []
    for _mod in check_modules:
        module_spec = importlib.util.find_spec(_mod)
        if module_spec is not None:
            _result = None
            submodule = importlib.import_module(_mod)
            if DEV_MODE:
                importlib.reload(submodule)
            if action == 'check':
                _result = submodule.check(maya_scene_data = maya_scene_data)
            elif action == 'modify':
                _result = submodule.modify(modify_data = modify_data)
            if _result:
                all_result.append(_result)

    return all_result

def check_data(
            check_modules: list,
            maya_scene_data: scene_data.MayaSceneData,
            check_result: data.CheckResultData,
            project_settings: data.ProjectSettings,
            execute_check_module:list = [],
            ):

    if not check_modules:
        # logger.error('Not Found Check Modules')
        cmds.error('Not Found Check Modules')
        return 'Not Found Check Modules'

    if not maya_scene_data:
        # logger.error('Not Found Check Data')
        cmds.error('Not Found Check Data')
        return 'Not Found Check Data'

    if not maya_scene_data.project:
        # logger.error('Not Found Project Name')
        cmds.error('Not Found Project Name')
        return 'Not Found Project Name'

    # チェックする項目の限定があれば適用
    if execute_check_module:
        _sort_order_file = setting.load_config('CHECKER_MODULE_SORT_ORDER')
        execute_check_module:list = list(set(execute_check_module)|set(_sort_order_file))

    progress = None
    _length :int = len(check_modules)
    if not maya_scene_data.is_batch:
        progress = gui_util.ProgressDialog()
        progress.setUp(maxValue=_length, title='Maya Scene Checker')
        progress.show()

    for count, _mod in enumerate(check_modules):
        module_spec = importlib.util.find_spec(_mod)

        if module_spec is not None:
            module_name = _mod.rsplit(".")[-1]
            submodule = None
            if execute_check_module:
                if module_name in execute_check_module:
                    submodule = importlib.import_module(_mod)
            else:
                submodule = importlib.import_module(_mod)
            if submodule:
                checker_module_name:str = submodule.CHECKER

                if DEV_MODE:
                    importlib.reload(submodule)
                checker:data.Checker = data.Checker()

                if progress:
                    progress.setValue(count)
                    progress.setLabelText(f'{checker_module_name: <50}: {count: ^4} / {_length: >4}')
                    QtCore.QCoreApplication.processEvents()
                    if progress.wasCanceled():
                        break
                checker.set_result_data(category=maya_scene_data.current_category, checker=checker_module_name, checker_path=submodule._current_file)
                # maya_scene_data.current_checker = submodule.CHECKER
                project_settings.current_checker = checker_module_name
                submodule.check(maya_scene_data = maya_scene_data, check_result = check_result, checker = checker)
                check_result.result_datas[checker_module_name] = checker.result
                # try:
                #     checker.set_result_data(category=maya_scene_data.current_category, checker=checker_module_name, checker_path=submodule._current_file)
                #     # maya_scene_data.current_checker = submodule.CHECKER
                #     project_settings.current_checker = checker_module_name
                #     submodule.check(maya_scene_data = maya_scene_data, check_result = check_result, checker = checker)
                #     check_result.result_datas[checker_module_name] = checker.result
                # except Exception as e:
                #     print(f'module import error: [{submodule.__name__, e}]')


def modify_data(results:list):
    modify_result:data.ModifyResult = data.ModifyResult()
    for result in results:
        result:data.ResultData = result
        module_spec = importlib.util.find_spec(result.checker)
        if module_spec:
            submodule = importlib.import_module(result.checker)
            if DEV_MODE:
                importlib.reload(submodule)
            submodule.modify(modify_data=result, modify_result=modify_result)
    return modify_result







