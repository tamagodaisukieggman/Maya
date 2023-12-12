# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial
from collections import Counter
import glob
import os
import sys

import importlib

import time
from functools import wraps

from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as om2anim

from maya import cmds
import maya.mel
from mtk.utils import getCurrentSceneFilePath


CHARACTOR_PATHS = [
    "z:/mtk/work/resources/characters",
    "z:/mtk/work/noshipping/characters"
]

ENV_PATHS = [
    "z:/mtk/work/resources/env",
    "z:/mtk/work/noshipping/env"
]


# 開発中はTrue、リリース時にFalse
DEV_MODE = True

if not DEV_MODE:
    from . import logger

config_node = None
CYLISTA_SCRIPT_PATH = "Z:/cyllista/tools/maya/modules/cyllista/scripts/"


if CYLISTA_SCRIPT_PATH not in sys.path:
    sys.path.append(CYLISTA_SCRIPT_PATH)


mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

PATH = "Z:/mtk/tools/maya/modules/mtku/scripts/mtku/maya/menus/file/new_checker"
PATH = "Z:/mtk/tools/maya/2022/modules/mtk/scripts/mtk/file/new_checker"
PACKAGE = ".".join(PATH.split("/")[-3:])

# Cylista Exporter ウィンドウのクラス名
EXPORT_WINDOW_CLASS_NAME = "ExportWindow"

PHY_COLLISION_ATTRIBUTE_LIST = [
    "phyActorType",
    "phyShapeType",
    "phyCollisionTypeName",
    "phyQueryFilterPresetName"
]

PHY_COLLISION_ATTRIBUTE_VALUES = {
    "default": ["default", "default", "default", "object"],
    "col_character": ["default", "default", "default", "object_without_camera"],
    "col_player": ["default", "No Simulation", "default", "player"],
    "col_camera": ["default", "No Simulation", "default", "camera"],
    "col_detailed": ["default", "default", "detailed", "detailed"],
    "col_sight": ["default", "No Simulation", "default", "sight"],
    "col_water": ["default", "default", "default", "water_surface"]
}


def timeit(ndigits=2):
    """Print execution time [sec] of function/method
    - message: message to print with time
    - ndigits: precision after the decimal point
    """
    def outer_wrapper(func):
        # @wraps: keep docstring of "func"
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print("[ {} ] Function time for : {sec} [sec], args [{args}], kwargs [{kwargs}]".format(
                func.func_name,
                args=args,
                kwargs=kwargs,
                sec=round(end - start, ndigits))
            )
            return result
        return inner_wrapper
    return outer_wrapper


class ProgressWindowBlock(object):
    """ProgressWindowを表示させるコンテキストマネージャー
    """

    def __init__(self, title='', progress=0, minValue=0, maxValue=100, isInterruptable=True, show_progress=True):
        self._show_progress = show_progress and (not cmds.about(q=True, batch=True))

        self.title = title
        self.progress = progress
        self.minValue = minValue
        self.maxValue = maxValue
        self.isInterruptable = isInterruptable

        self._start_time = None
        self.status = None

    def __enter__(self):
        # logger.info('[ {} ] : Start'.format(self.title))

        if self._show_progress:
            cmds.progressWindow(
                title=self.title,
                progress=int(self.progress),
                status='[ {} ] : Start'.format(self.title),
                isInterruptable=self.isInterruptable,
                min=self.minValue,
                max=self.maxValue + 1
            )

        # self._start_time = datetime.datetime.now()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # logger.info('[ {} ] : End : Calculation time : {}'.format(self.title, calc_time))

        if self._show_progress:
            cmds.progressWindow(ep=1)

    def step(self, step):
        if self._show_progress:
            cmds.progressWindow(e=True, step=step)
            # cmds.progressWindow(e=True,
            #         status='[ {} / {} ] : {}'.format(self.progress, self.maxValue, self.status))

    def _set_status(self, status):
        if self._show_progress:
            # self.status = status
            cmds.progressWindow(e=True,
                                status='[ {} / {} ] : {}'.format(self.progress, self.maxValue, status))

    def _get_status(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, status=True)

    status = property(_get_status, _set_status)

    def _set_progress(self, progress):
        if self._show_progress:
            cmds.progressWindow(e=True, progress=progress)

    def _get_progress(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, progress=True)

    progress = property(_get_progress, _set_progress)

    def is_cancelled(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, ic=True)

    @staticmethod
    def wait(sec=1.0):
        cmds.pause(sec=sec)


def close_export_window():
    for child in mayaMainWindow.children():
        # print(child.__class__.__name__)
        # print(child.__class__.__name__ == EXPORT_WINDOW_CLASS_NAME)
        if child.__class__.__name__ == EXPORT_WINDOW_CLASS_NAME:
            child.close()


def check_unknown():
    _error = []
    _result = []

    unknown_plugings = cmds.unknownPlugin(query=True, list=True)
    unknown_nodes = cmds.ls(type="unknown")

    if unknown_nodes:
        for unknown_node in unknown_nodes:
            cmds.lockNode(unknown_node, l=False)
            _result.append(unknown_node)
            try:
                cmds.delete(unknown_node)
            except Exception as e:
                _error.append(unknown_node)
                print(e)

    if unknown_plugings:
        for unknown_pluging in unknown_plugings:
            try:
                # cmds.unloadPlugin(unknown_pluging, f=True)
                cmds.unknownPlugin(unknown_pluging, r=True)
                _result.append(unknown_pluging)
            except Exception as e:
                _error.append(unknown_pluging)
                print(e)

    return [_error, _result]


def check_poly_bind_data():
    _error = []
    _result = []

    _poly_bind_data = cmds.ls(type="polyBlindData")
    _poly_bind_data_template = cmds.ls(type="blindDataTemplate")
    if _poly_bind_data_template:
        _poly_bind_data.extend(_poly_bind_data_template)
        for _data in _poly_bind_data:
            try:
                cmds.delete(_data)
                _result.append(_data)
            except:
                _error.append(_data)

    return [_error, _result]


def delete_poly_bind_data():
    _poly_bind_data = cmds.ls(type="polyBlindData")
    _poly_bind_data_template = cmds.ls(type="blindDataTemplate")
    if _poly_bind_data_template:
        _poly_bind_data.extend(_poly_bind_data_template)
        # if _poly_bind_data:
        #     cmds.delete(_poly_bind_data)
    return _poly_bind_data


def open_export_window():
    """Cyllista Export Window
    """

    import cylModelExporterWindow
    cylModelExporterWindow.show()


def iterUpNode(node):
    parent = cmds.listRelatives(node, parent=True, fullPath=True)
    if parent:
        yield parent[0]
        for p in iterUpNode(parent):
            yield p


def get_nodes():
    root_nodes = cmds.ls(assemblies=True, l=True)
    nodes = [x for x in cmds.ls("mdl_*", type="transform", l=True) if x in root_nodes]
    if not nodes:
        return
    return nodes

# def check():
#     check_nodes = get_nodes()

#     import mtku.maya.menus.file.checker.model.check_mesh
#     for node in check_nodes:
#         _check_name_hierarchy_first
#     print(check_nodes," ----nodes")
#     open_export_window()
#     # cmds.scriptJob(event=["SceneOpened", partial(self.update_window)])


class Checker(object):
    NAME = "mutsunokami_mdl_checker_result_ui"
    TITLE = u"[ {} ] データとしてチェックしました。データの確認をお願いします"
    _text_a_width = 300
    _text_b_width = 100
    _button_a_width = 200
    _button_b_width = 100
    _spacing = 2
    _scroll_width = _text_a_width + _spacing + _text_b_width + _button_a_width
    _scroll_height = 200
    _frame_width = _scroll_width + 35

    _window_width = _frame_width - 10
    _window_height = 200
    _row_height = 30
    _separetor_height = 2

    _frame = "{}_frame".format(NAME)
    _scroll = "{}_scroll".format(NAME)
    _modify_btn = "{}_modify_btn".format(NAME)

    _rows = []

    modify_result_window = "{}_modify_result_window".format(NAME)
    modify_result_window_title = u"[ {} ] 個の項目を修正しました"
    modify_result_frame = "{}_modify_result_frame".format(NAME)
    modify_result_scroll = "{}_modify_result_scroll".format(NAME)
    modify_result_close_btn = "{}_modify_result_close_btn".format(NAME)

    error_result_window = "{}_error_result_window".format(NAME)
    error_result_window_title = u"[ {} ] 個の項目が修正できませんでした"
    error_result_frame = "{}_error_result_frame".format(NAME)
    error_result_scroll = "{}_error_result_scroll".format(NAME)
    error_result_close_btn = "{}_error_result_close_btn".format(NAME)

    _result_window_width = 850
    _result_window_height = 200

    def memory_clear(self):
        self.data_type = ""
        self.scene_path = ""
        self.nodes = []
        self.meshes = []
        self.results = []
        self.modifies = []
        self.modify_errors = []
        self.get_nodes()

    # def __init__(self):
    #     self.memory_clear()

    def get_nodes(self):
        scene_path = getCurrentSceneFilePath()
        if not scene_path:
            scene_path = om.MFileIO.currentFile()

        if len(scene_path.split(".")) < 2:
            self.scene_path = ""

        print(scene_path, " --- scene_path")

        if not scene_path:
            cmds.confirmDialog(
                message=u"シーンが開かれていない、もしくは保存されていないようです",
                title=u'シーンの確認',
                button=['OK'],
                defaultButton='OK',
                cancelButton="OK",
                dismissString="OK")
        else:
            self.scene_path = scene_path.replace(os.sep, '/')
            if os.path.basename(scene_path)[:4] != "mdl_":
                cmds.confirmDialog(
                    message=u"シーン名は「 mdl_ 」で始まるようにしてください",
                    title=u'シーン名の確認',
                    button=['OK'],
                    defaultButton='OK',
                    cancelButton="OK",
                    dismissString="OK")
            else:
                self.scene_type_check()
                root_nodes = cmds.ls(assemblies=True, l=True)
                nodes = [x for x in cmds.ls("mdl_*",
                                            type="transform",
                                            l=True) if x in root_nodes and not cmds.listRelatives(x, s=True)]

                # meshes = [x for x in cmds.listRelatives(nodes,
                #             allDescendents=True,
                #             fullPath=True,
                #             type="mesh")if x and not cmds.getAttr("{}.intermediateObject".format(x))]
                meshes = cmds.listRelatives(nodes, allDescendents=True, fullPath=True, type="mesh")
                if meshes:
                    meshes = [x for x in meshes if x and not cmds.getAttr("{}.intermediateObject".format(x))]

                self.nodes = nodes
                self.meshes = meshes

    def scene_type_check(self):
        flag = ""
        for _path in CHARACTOR_PATHS:
            if _path in self.scene_path.lower():
                flag = "chara"
                break

        for _path in ENV_PATHS:
            if _path in self.scene_path.lower():
                flag = "env"
                break
        self.data_type = flag

    def load_check_modules(self, node_type="node"):
        path = os.path.join(PATH, node_type)
        # print(path," ----")
        result = None
        python_files = glob.glob(path + "/*.py")

        with ProgressWindowBlock(title='...', maxValue=len(python_files)) as prg:
            prg.step(1)
            for checker in python_files:
                prg.step(1)
                prg.status = 'Check Data ...'
                if prg.is_cancelled():
                    break
                # print(checker,"---")
                checker = os.path.basename(checker).split(".")[0]
                # print(checker,"===")
                if not checker.startswith("__"):
                    modulename = "{}.{}.{}".format(PACKAGE, node_type, checker)
                    print(modulename, " ----load module")
                    exec('import {}'.format(modulename))

                    """
                    開発時のホットリロード用
                    """
                    print(DEV_MODE, sys.version_info[0], " ----- DEV_MODE")
                    if DEV_MODE:
                        exec('importlib.reload({})'.format(modulename))

                    # シーン全体でチェックする内容
                    if node_type == "scene":
                        funcname = "{}.{}".format(modulename, "main")
                        command = '{}("{}", "{}")'.format(funcname, self.data_type, self.scene_path)
                        try:
                            result = eval(command)
                        except Exception as e:
                            print(command, "----command")
                            print(e, " ---- error node")
                        print(funcname, "---funcname")
                        print(command, "--- command")
                        print("\n----result")
                        print(result, "----result")
                        if result:
                            self.results.extend(result)

                    # ルートノードを検査する
                    elif node_type == "node":
                        for node in self.nodes:
                            # print(node, "---load node module")
                            # node = node.split("|")[1]
                            funcname = "{}.{}".format(modulename, "main")
                            command = '{}("{}", "{}", "{}")'.format(funcname, self.data_type, self.scene_path, node)
                            print(command, " -- command")
                            try:
                                result = eval(command)
                            except Exception as e:
                                print(command, "----command")
                                print(e, " ---- error node")
                            print(funcname, "---funcname")
                            print(command, "--- command")
                            print("\n----result")
                            print(result)
                            if result:
                                self.results.extend(result)

                    # 各ルートノード以下にあるメッシュノードのリストを検査する
                    elif node_type == "mesh":
                        print(self.meshes, "--load meshes module")
                        funcname = "{}.{}".format(modulename, "main")
                        command = '{}("{}", "{}", {})'.format(funcname, self.data_type, self.scene_path, self.meshes)
                        print("\n\n\n")
                        print(funcname, "---funcname")
                        print(command, "--- command")
                        try:
                            result = eval(command)
                        except Exception as e:
                            # print(command, "----command")
                            print(e, " ---- error mesh")
                        print("\n----result")
                        print(result, "----result")
                        if result:
                            self.results.extend(result)

    # @timeit(ndigits=2)
    def do_check(self, *args):
        if not DEV_MODE:
            logger.send_launch(u'ツール起動')
        _error_flag = False
        _node_flag = False
        _mesh_flag = False
        self.memory_clear()
        self.close_window()
        if self.scene_path:
            print(self.nodes, self.meshes, " --- get nodes")
            self.load_check_modules("scene")
            if self.nodes:
                self.load_check_modules("node")
                _node_flag = True
            if self.meshes:
                self.load_check_modules("mesh")
                _mesh_flag = True
                print(self.results, "--- result")
            print(_node_flag, " --- _node_flag")
            print(_mesh_flag, "--- _mesh_flag")
            if not _node_flag:
                cmds.confirmDialog(
                    message=u"シーンに「mdl_」で始まるグループがありません",
                    title=u'!?',
                    button=['OK'],
                    defaultButton='OK',
                    cancelButton="OK",
                    dismissString="OK")
            elif not _mesh_flag:
                cmds.confirmDialog(
                    message=u"「mdl_」グループにメッシュがありませんでした",
                    title=u'!?',
                    button=['OK'],
                    defaultButton='OK',
                    cancelButton="OK",
                    dismissString="OK")
            else:
                _unknown = check_unknown()
                print(_unknown, " --- _unknown")
                if _unknown:
                    _unknown_error = _unknown[0]
                    _unknown_result = _unknown[1]
                    if _unknown_error:
                        _m = u"以下のノード、プラグインが削除できません\n{}\nご確認ください".format("\n".join(_unknown_error))
                        _error_flag = True

                        if not DEV_MODE:
                            logger.error(u"[ {} ] 削除できないプラグイン".format(", ".join(_unknown_error)))

                        cmds.confirmDialog(
                            message=_m,
                            title=u'!?',
                            button=['OK'],
                            defaultButton='OK',
                            cancelButton="OK",
                            dismissString="OK")
                    if _unknown_result:
                        _m = u"以下のノード、プラグインを削除しました\n\n{}".format("\n".join(_unknown_result))
                        cmds.confirmDialog(
                            message=_m,
                            title=u'不明プラグイン、ノードの削除',
                            button=['OK'],
                            defaultButton='OK',
                            cancelButton="OK",
                            dismissString="OK")
        print(_error_flag, " --- _error_flag")
        if not DEV_MODE:
            if self.data_type and self.scene_path:
                logger.info(u"[ {} ] [ {} ]".format(self.data_type, self.scene_path))
            if self.nodes:
                logger.info(u"検査したルートノード [ {} ] 個 [ {} ]".format(len(self.nodes), u", ".join(self.nodes)))
            if self.meshes:
                logger.info(u"検査したメッシュ [ {} ] 個 [ {} ]".format(len(self.meshes), u", ".join(self.meshes)))
        print(self.scene_path, " --- self.scene_path")
        print(self.data_type, "--- self.data_type")
        print(self.results, " ^^^ self.results")
        if not _error_flag:
            if self.results:

                self.result_window()
            elif self.nodes and self.meshes:
                print("000000")
                # open_export_window()

    def select_error_nodes(self, node, node_type, *args):
        """
        コンポーネントの場合一つのノードに複数のコンポーネント
        がリストに入っている
        """

        # print("select function -------")
        # print(node, "---node")
        # print(node_type, "---node type")

        if not node:
            return

        if "comp" in node_type or "influence" in node_type:
            visible_node = node[0].rsplit(".", 1)[0]
        else:
            visible_node = node

        if not cmds.objExists(visible_node):
            return

        cmds.select(node, r=True)

        if node_type == "material" or node_type == "texture":
            return

        # if node_type != "compornent":
        try:
            cmds.setAttr("{}.visibility".format(visible_node), 1)
        except:
            pass

        for n in iterUpNode(visible_node):
            try:
                cmds.setAttr("{}.visibility".format(n), 1)
            except:
                pass

        shape = cmds.listRelatives(visible_node, shapes=True, fullPath=True)
        if shape:
            try:
                cmds.setAttr("{}.visibility".format(shape[0]), 1)
            except:
                pass

        try:
            maya.mel.eval('FrameSelectedWithoutChildren;fitPanel -selectedNoChildren;')
        except:
            pass
        # else:
        #     cmds.viewFit(f=0.1)

        _outliners = [x for x in cmds.getPanel(type="outlinerPanel") if x in cmds.getPanel(vis=True)]

        if _outliners:
            [cmds.outlinerEditor(x, e=True, sc=True) for x in _outliners]

    @classmethod
    def close_window(self):

        close_export_window()

        try:
            cmds.deleteUI(self._scroll)
        except:
            pass
        try:
            cmds.deleteUI(self._frame)
        except:
            pass
        try:
            cmds.deleteUI(self.NAME)
        except:
            pass

    def add_attribute(self, node):
        node_short_name = node.split("|")[-1]
        # detaild_flag = False
        # _parent = cmds.listRelatives(node, parent=True, fullPath=True, type="transform")
        _result = []
        # for _brother in cmds.listRelatives(_parent,
        #                                     children=True,
        #                                     fullPath=True,
        #                                     type="transform"):
        #     _brother_short_name = _brother.split("|")[-1]
        #     if "col_detailed" in _brother_short_name:
        #         detaild_flag = True
        #         break

        for _attr in PHY_COLLISION_ATTRIBUTE_LIST:
            if not cmds.attributeQuery(_attr, n=node, ex=True):
                cmds.addAttr(node, longName=_attr,
                             dataType="string"
                             )
                _result.append([node, _attr])

        # # コリジョンタイプからアトリビュートを適用する準備
        # if node_short_name in PHY_COLLISION_ATTRIBUTE_VALUES:
        #     col_type = node_short_name
        # else:
        #     col_type = "default"

        # # ディテールコリジョンのあるなし、キャラクターコリジョンで分岐
        # for _attr, setting in zip(PHY_COLLISION_ATTRIBUTE_LIST, PHY_COLLISION_ATTRIBUTE_VALUES[col_type]):
        #     if (detaild_flag and
        #         node_short_name == "col_character" and
        #         "phyQueryFilterPresetName" == _attr):

        #         cmds.setAttr('{}.{}'.format(node, _attr), "object_without_camera", type="string")
        #     else:
        #         cmds.setAttr('{}.{}'.format(node, _attr), setting, type="string")

        return _result

    def chenge_collision_attr(self, node):
        node_short_name = node.split("|")[-1]
        detaild_flag = False
        _result = []
        _parent = cmds.listRelatives(node, parent=True, fullPath=True, type="transform")
        for _brother in cmds.listRelatives(_parent,
                                           children=True,
                                           fullPath=True,
                                           type="transform"):
            _brother_short_name = _brother.split("|")[-1]
            if "col_detailed" in _brother_short_name:
                detaild_flag = True
                break

        # コリジョンタイプからアトリビュートを適用する準備
        if node_short_name in PHY_COLLISION_ATTRIBUTE_VALUES:
            col_type = node_short_name
        else:
            col_type = "default"

        # ディテールコリジョンのあるなし、キャラクターコリジョンで分岐
        for _attr, setting in zip(PHY_COLLISION_ATTRIBUTE_LIST,
                                  PHY_COLLISION_ATTRIBUTE_VALUES[col_type]):
            if node_short_name == "col_character" and "phyQueryFilterPresetName" == _attr:
                if detaild_flag:
                    cmds.setAttr('{}.{}'.format(node, _attr),
                                 "object_without_camera", type="string")
                else:
                    cmds.setAttr('{}.{}'.format(node, _attr),
                                 "detailed_object_without_camera", type="string")
                _result.append([node, _attr])
            else:
                if cmds.getAttr("{}.{}".format(node, _attr)) != setting:
                    cmds.setAttr('{}.{}'.format(node, _attr), setting, type="string")
                    _result.append([node, _attr])

        return _result

    def unlock_attribute(self, node, attr):
        """
        connectionInfo を使わないとロックを解除できないケースがある
        ただ、その場合はconnectionInfoで取得する前に一度setAttrでロックを解除しておく必要があるようだ
        """
        for _axis in ["x", "y", "z"]:
            cmds.setAttr("{}.{}{}".format(node, attr, _axis), l=False)
            plug_name = cmds.connectionInfo("{}.{}{}".format(node, attr, _axis), gla=True)
            # print(plug_name, "-----plug_name")
            if plug_name:
                cmds.setAttr(plug_name, l=False)

    def reset_bind_pose(self, root_node):
        selections = cmds.ls(sl=True)
        meshes = cmds.listRelatives(root_node, allDescendents=True, fullPath=True, type="mesh")
        meshes = [x for x in meshes if x and not cmds.getAttr("{}.intermediateObject".format(x))]
        _all_joint = sorted([x for x in cmds.listRelatives(root_node,
                                                           allDescendents=True,
                                                           fullPath=True)if cmds.nodeType(x) == "joint"])

        # _all_dag_poses = cmds.listConnections(root_node, t='dagPose')
        _all_dag_poses = cmds.dagPose(root_node, q=True, bp=True)
        _counter = Counter(_all_dag_poses)

        for mesh in meshes:
            cmds.select(mesh, r=True)
            maya.mel.eval("GoToBindPose;")
        _pose = _counter.most_common()[0][0]
        cmds.delete(_all_dag_poses)
        cmds.select(_all_joint, r=True)
        cmds.dagPose(bp=True, s=True, sl=True, name=_pose)

        if selections:
            cmds.select(selections, r=True)
        else:
            cmds.select(cl=True)

    # @timeit(ndigits=2)
    def modify_data(self, *args):
        inf_num = 4

        if not self.results:
            return

        if config_node:
            config = config_node.get_config()
            inf_num = config.get("cySkinInfluenceCountMax", inf_num)

        for result in self.results:
            # text = result[0]
            _type = result[1]
            node = result[-1]

            if _type == "Bind pose":
                # dag_poses = cmds.listConnections(node, t='dagPose')
                # if not dag_poses:
                #     return

                # joints = cmds.listRelatives(node, allDescendents=True, fullPath=True, type="joint")

                # 既存のBindPoseを削除
                # cmds.delete(node)
                # BindPoseの再生成
                # joints = cmds.ls(node, dag=True, l=True)
                # cmds.dagPose(joints, bp=True, s=True, sl=True)
                self.reset_bind_pose(node)
                self.modifies.append(u"[ {} ] のバインドポーズを再設定".format(node))
                print("{:-<100}  {}".format(node, "reset bind pose"))

            if _type == "Collision Attribute":
                _collision_attr = self.add_attribute(node)
                if _collision_attr:
                    _collision_attr = _collision_attr[0]
                    print("{:-<100}  {}  [ {} ]".format(_collision_attr[0],
                                                        "Add Collision Attribute",
                                                        _collision_attr[1]))

                    self.modifies.append(u"[ {} ] に [ {} ] のコリジョンアトリビュート追加".format(_collision_attr[0],
                                                                                   _collision_attr[1]))
                _collision_attr_modify = self.chenge_collision_attr(node)

                if _collision_attr_modify and not _collision_attr:
                    _collision_attr_modify = _collision_attr_modify[0]

                    print("{:-<100}  {}  [ {} ]".format(_collision_attr_modify[0],
                                                        "Modify Collision Attribute",
                                                        _collision_attr_modify[1]))

                    self.modifies.append(u"[ {} ] の [ {} ] のコリジョンアトリビュート変更".format(_collision_attr_modify[0],
                                                                                   _collision_attr_modify[1]))

            if _type == "transform":
                """
                子のノードがロックされているとフリーズできないのでその対応
                connectionInfo を使わないといけない場面があった
                """

                _cld = cmds.listRelatives(node, allDescendents=True, fullPath=True, type="transform")
                # for _c in sorted(_cld, key=lambda x: len(x.split("|")), reverse=True):
                if _cld:
                    for _c in sorted(_cld, key=lambda x: len(x.split("|")), reverse=True):
                        cmds.lockNode(_c, lock=False)
                        for attr in ["t", "r", "s"]:
                            self.unlock_attribute(_c, attr)

                try:
                    cmds.makeIdentity(node, apply=True, t=True, r=True, s=True, n=False, pn=True)
                    self.modifies.append(u"[ {} ] のトランスフォームを [ フリーズ ]".format(node))
                    print("{:-<100}  {}".format(node, "freeze transform"))
                    # print(node, " -- freeze transform")
                except Exception as e:
                    self.modify_errors.append(u"!! [ {} ] のトランスフォームを [ フリーズ ] できない".format(node))
                    print(e, " ++ freeze transform error")
                    print("{:+<100}  {}".format(node, "freeze transform error"))

            if _type == "keyframe":
                try:
                    cmds.cutKey(node, cl=True)
                    self.modifies.append(u"[ {} ] の [ キーフレーム ] を削除".format(node))
                    print("{:-<100}  {}".format(node, "delete key frame"))
                    # print(node, " -- delete key frame")
                except Exception as e:
                    self.modify_errors.append(u"!! [ {} ] の [ キーフレーム ] を削除できない".format(node))
                    # print(e, " ++ delete key frame error")
                    print("{:+<100}  {}".format(node, "delete key frame error"))

            if _type == "history":
                _poly_bind_flag = False
                _bind_skin_flag = False

                _historys = cmds.listHistory(node, pruneDagObjects=True, interestLevel=2)
                if _historys:

                    if "skinCluster" in [cmds.nodeType(x) for x in _historys]:
                        _bind_skin_flag = True

                    if not _bind_skin_flag:
                        for _history in _historys:
                            if cmds.nodeType(_history) in ["polyBlindData", "blindDataTemplate"]:
                                try:
                                    cmds.delete(_history)
                                    _poly_bind_flag = True
                                except:
                                    pass
                        if _poly_bind_flag:
                            self.modifies.append(u"[ {} ] の [ PolyBlind ] を削除".format(node))
                            print("{:-<100}  {}".format(node, "delete history poly blind"))
                            # print(node, " -- delete history poly bind")

                        if cmds.listHistory(node, pruneDagObjects=True, interestLevel=2):
                            try:
                                cmds.bakePartialHistory(node, pc=True)
                                self.modifies.append(u"[ {} ] の [ Non Deformer History ] を削除".format(node))
                                print("{:-<100}  {}".format(node, "delete history"))
                                # print(node, " -- delete history")
                            except Exception as e:
                                self.modify_errors.append(u"!! [ {} ] の [ Non Deformer History ] を削除でない".format(node))
                                # print(node, " ++ delete history error")
                                print("{:+<100}  {}".format(node, "delete history error"))
                    else:
                        try:
                            cmds.bakePartialHistory(node, ppt=True)
                            self.modifies.append(u"[ {} ] の [ Non Deformer History ] を削除".format(node))
                            print("{:-<100}  {}".format(node, "delete history"))
                            # print(node, " -- delete history")
                        except Exception as e:
                            self.modify_errors.append(u"!! [ {} ] の [ Non Deformer History ] を削除できない".format(node))
                            # print(node, " ++ delete history error")
                            print("{:+<100}  {}".format(node, "delete history error"))

            if _type == "No polygon":
                try:
                    cmds.delete(node)
                    self.modifies.append(u"[ {} ] の [ ノード ] を削除".format(node))
                    print("{:-<100}  {}".format(node, "delete Node"))
                    # print(node, " -- delete Node")
                except Exception as e:
                    self.modify_errors.append(u"!! [ {} ] の [ ノード ] を削除できない".format(node))
                    print("{:+<100}  {}".format(node, "delete Node error"))
                    # print(node, " ++ delete Node error")

            if _type == "comp weight":
                _geometory = node[0].rsplit(".", 1)[0]
                selList = om2.MSelectionList()
                selList.add(_geometory)

                dagPath = selList.getDagPath(0)
                _ids = [int(x.split("[")[-1].split("]")[0]) for x in node]

                self.modify_weight(dagPath, _ids, inf_num)

            if _type == "Display Layer" or _type == "plugin":
                try:
                    cmds.delete(node)
                    self.modifies.append(u"[ {} ] を削除".format(node))
                    print("{:-<100}  {}".format(node, "delete Node"))
                except Exception as e:
                    self.modify_errors.append(u"!! [ {} ] を削除できない".format(node))
                    print("{:+<100}  {}".format(node, "delete Node error"))
            if _type == "Locked Normal" and self.data_type == "chara":
                try:
                    cmds.polyNormalPerVertex(node, ufn=True)
                    # cmds.polySoftEdge(node, a=180, ch=True)
                    self.modifies.append(u"[ {} ] のノーマルロックを解除".format(node))
                    cmds.bakePartialHistory(node, ppt=True)
                    print("{:-<100}  {}".format(node, "Unlock Normal"))
                except Exception as e:
                    self.modify_errors.append(u"[ {} ] のノーマルロックを解除できない".format(node))
                    print("{:+<100}  {}".format(node, "Unlock Normal error"))

        _ploly_bind_data = delete_poly_bind_data()
        if _ploly_bind_data:
            cmds.delete(_ploly_bind_data)
            print("\n{:-^50}".format(" delete poly blind data "))
            print(_ploly_bind_data)
            print("{:-^50}\n\n".format(""))

        # self.open_modify_result()
        self.open_modify_result_new()
        self.do_check()

    def modify_weight(self, dagPath, _ids, inf_num):

        round_num = 5

        skinCluster = cmds.ls(cmds.listHistory(dagPath.fullPathName()), type='skinCluster')[0]
        skinNode = om2.MGlobal.getSelectionListByName(skinCluster).getDependNode(0)
        skinFn = om2anim.MFnSkinCluster(skinNode)

        indices = _ids

        fnCompNew = om2.MFnSingleIndexedComponent()
        vertexComp = fnCompNew.create(om2.MFn.kMeshVertComponent)
        fnCompNew.addElements(indices)
        weights = skinFn.getWeights(dagPath, vertexComp)

        infDags = skinFn.influenceObjects()
        inf_length = len(infDags)
        infIndices = om2.MIntArray(len(infDags), 0)

        _stop_flag = False
        with ProgressWindowBlock(title='...', maxValue=len(indices)) as prg:
            prg.status = 'Modify Weight ...'
            prg.step(1)

            for x in range(inf_length):
                infIndices[x] = x

            joints = [infDags[inf_id].fullPathName() for inf_id in range(inf_length)]

            reshape_weights = []
            for j in range(int(len(weights[0]) / inf_length)):
                reshape_weights.append([weights[0][i + j * inf_length] for i in range(inf_length)])

            round_weights_list = []

            for i, _index in enumerate(indices):
                prg.step(1)
                prg.status = 'Modify Weight ...'
                if prg.is_cancelled():
                    _stop_flag = True
                    break

                weight_dic = dict(zip(joints, [round(x, round_num) for x in reshape_weights[i]]))
                weight_lists = []
                [weight_lists.extend([k, v]) for k, v in sorted(weight_dic.items(), key=lambda x:x[1], reverse=True)]

                _weights = weight_lists[1::2]
                _joints = weight_lists[0::2]

                if len(_weights) > inf_num:
                    _zero_weights = [0.0 for x in range(len(_weights[inf_num:]))]
                    del _weights[inf_num:]
                    _weights.extend(_zero_weights)

                if sum(_weights) != 1.0:
                    _weights[0] = round(1.0 - sum(_weights[1:]), round_num)
                round_weights_list.extend([_weights[_joints.index(_jnt)] for _jnt in joints])

        if not _stop_flag:
            skinFn.setWeights(dagPath,
                              vertexComp,
                              infIndices,
                              om2.MDoubleArray(round_weights_list),
                              False)
            self.modifies.append(u"[ {} ] の ウェイト値を修正".format(dagPath.fullPathName()))
            print("{:-<100}  {}".format(dagPath.fullPathName(), "Modify weight"))

    def close_error_result_window(self, *args):
        try:
            cmds.deleteUI(self.error_result_scroll)
        except:
            pass
        try:
            cmds.deleteUI(self.error_result_frame)
        except:
            pass
        try:
            cmds.deleteUI(self.error_result_window)
        except:
            pass

    def open_modify_result_new(self, *args):
        if self.modify_errors:
            self.close_error_result_window()
            cmds.window(
                self.error_result_window,
                title=self.error_result_window_title.format(len(self.modify_errors)),
                width=self._result_window_width,
                height=self._result_window_height
            )
            cmds.frameLayout(self.error_result_frame,
                             marginHeight=10,
                             marginWidth=10,
                             labelVisible=False,
                             width=self._result_window_width - 10)
            cmds.scrollLayout(self.error_result_scroll,
                              height=self._result_window_height - 10,
                              width=self._result_window_width - 35,
                              childResizable=True,
                              verticalScrollBarAlwaysVisible=True)
            print("\n{:-^100}".format(" Error Result "))
            for i, _mod in enumerate(self.modify_errors, 1):
                _text = u"[ {:0>5} ]  {}".format(i, _mod)
                print(_text)
                cmds.text(l=_text, align="left")
            print("{:-^100}\n\n".format(""))
            cmds.setParent("..")
            cmds.button(self.error_result_close_btn,
                        l="Close",
                        c=partial(self.close_error_result_window))

            cmds.setParent("..")
            cmds.showWindow(self.error_result_window)

        if self.modifies:
            self.close_modify_result_window()
            cmds.window(
                self.modify_result_window,
                title=self.modify_result_window_title.format(len(self.modifies)),
                width=self._result_window_width,
                height=self._result_window_height
            )
            cmds.frameLayout(self.modify_result_frame,
                             marginHeight=10,
                             marginWidth=10,
                             labelVisible=False,
                             width=self._result_window_width - 10)
            cmds.scrollLayout(self.modify_result_scroll,
                              height=self._result_window_height - 10,
                              width=self._result_window_width - 35,
                              childResizable=True,
                              verticalScrollBarAlwaysVisible=True)
            print("\n{:-^100}".format(" Modify Result "))
            for i, _mod in enumerate(self.modifies, 1):
                _text = u"[ {:0>5} ]  {}".format(i, _mod)
                print(_text)
                cmds.text(l=_text, align="left")
            print("{:-^100}\n\n".format(""))
            cmds.setParent("..")
            cmds.button(self.modify_result_close_btn,
                        l="Close",
                        c=partial(self.close_modify_result_window))

            cmds.setParent("..")

            cmds.showWindow(self.modify_result_window)

    def close_modify_result_window(self, *args):
        try:
            cmds.deleteUI(self.modify_result_scroll)
        except:
            pass
        try:
            cmds.deleteUI(self.modify_result_frame)
        except:
            pass
        try:
            cmds.deleteUI(self.modify_result_window)
        except:
            pass

    def open_modify_result(self, *args):
        if self.modify_errors:
            self.modify_errors.append(u"\n\nデータの確認をお願いします")
            cmds.confirmDialog(
                message=u"\n\n".join(self.modify_errors),
                title=u'!! 以下の項目が修正できませんでした',
                button=['OK'],
                defaultButton='OK',
                cancelButton="OK",
                dismissString="OK")

        if self.modifies:
            cmds.confirmDialog(
                message=u"\n\n".join(self.modifies),
                title=u'以下の項目を修正しました',
                button=['OK'],
                defaultButton='OK',
                cancelButton="OK",
                dismissString="OK")

    def result_window(self):
        print("close ---- ")
        self.close_window()
        print("open ---- ")
        if not self.data_type:
            _t = self.TITLE.format(u"不明")
        else:
            _t = self.TITLE.format(self.data_type)

        cmds.window(
            self.NAME,
            title=_t,
            width=self._window_width,
            height=self._window_height
        )

        cmds.frameLayout(self._frame,
                         marginHeight=10,
                         marginWidth=10,
                         labelVisible=False,
                         width=self._frame_width)

        # cmds.button(l=u"再検査", c=partial(self.do_check))

        cmds.rowLayout(nc=4, adj=4,
                       cw4=[self._text_a_width, self._spacing, self._text_b_width, self._button_a_width],
                       h=16,
                       bgc=[0.2, 0.2, 0.2]
                       )
        cmds.text(l=u"内容", al="center", w=self._text_a_width)
        cmds.text(l="")
        cmds.text(l=u"種類", al="center", w=self._text_b_width)
        cmds.text(l=u"該当ノード", al="center", w=self._button_a_width)
        cmds.setParent("..")
        cmds.scrollLayout(self._scroll,
                          height=self._scroll_height,
                          width=self._window_width,
                          childResizable=True,
                          verticalScrollBarAlwaysVisible=True)

        """
        エラーの種類別にソートして表示させるようにした
        """

        _sort_results = sorted(self.results, key=lambda x: x[1])

        if not DEV_MODE:
            logger.info(u"[ {} ] 個のエラー検出".format(len(_sort_results)))

        for result in _sort_results:
            ann = "None"
            button_name = None

            text = result[0]
            _type = result[1]
            node = result[-1]

            # logger.info(u"text [ {} ],type [ {}] ,node [ {} ]".format(text, _type, node))

            if node:
                if isinstance(node, list):
                    ann = "{}...".format(node[0])
                    button_name = node[0]
                else:
                    ann = " > ".join(node.split("|"))
                    button_name = node.split("|")[-1]

            bgc = [0.2, 0.2, 0.2]
            if "mesh" in _type:
                bgc = [0.3, 0.3, 0.5]
            elif "material" in _type:
                bgc = [0.5, 0.3, 0.3]
            elif "history" in _type:
                bgc = [0.3, 0.5, 0.3]
            elif "name" in _type:
                bgc = [0.3, 0.5, 0.5]
            elif "transform" in _type:
                bgc = [0.2, 0.3, 0.5]
            elif "joint" in _type:
                bgc = [0.5, 0.5, 0.2]
            elif "texture" in _type:
                bgc = [0.5, 0.2, 0.5]
            elif "keyframe" in _type:
                bgc = [0.6, 0.2, 0.2]
            elif "Display Layer" in _type:
                bgc = [0.3, 0.6, 0.2]
            elif "No Default" in _type:
                bgc = [0.8, 0.2, 0.2]
            elif "influence" in _type:
                bgc = [0.2, 0.5, 0.6]
            elif "weight" in _type:
                bgc = [0.3, 0.4, 0.5]
            elif "Locked Normal" in _type:
                bgc = [0.5, 0.5, 0.9]

            cmds.rowLayout(nc=4, adj=4,
                           cw4=[self._text_a_width,
                                self._spacing,
                                self._text_b_width,
                                self._button_a_width],
                           h=self._row_height
                           )

            cmds.text(l=text,
                      w=self._text_a_width,
                      h=self._row_height,
                      al="left",
                      ann="[ {} ]".format(ann)
                      )
            cmds.text(l="")
            cmds.text(l=_type,
                      w=self._text_b_width,
                      h=self._row_height,
                      al="center",
                      bgc=bgc
                      )
            # cmds.button(l=u"選択")

            cmds.button(l=button_name,
                        c=partial(self.select_error_nodes, node, _type),
                        w=self._button_a_width,
                        ann="[ {} ]".format(ann)
                        )
            cmds.setParent("..")
            cmds.separator(h=self._separetor_height)

        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2, adjustableColumn=1, columnWidth2=(100, 100))
        _btn_ann = u"[ グループノード ]のトランスフォームのフリーズ、\n"
        _btn_ann += u"ヒストリーの削除、キーフレームの削除、メッシュのないシェイプの削除、\n"
        _btn_ann += u"コリジョンアトリビュートの追加（デフォルト設定）、を行います"
        cmds.button(self._modify_btn,
                    l=u"解決できるエラーを修正し　再検査", c=partial(self.modify_data),
                    ann=_btn_ann,
                    en=False,
                    w=self._window_width / 2 - 10)
        cmds.button(
            l=u"エラーを無視して出力ウィンドウを開く", c=partial(self._open_export_window),
            w=200)
        cmds.setParent("..")

        if self.results:
            cmds.button(self._modify_btn, e=True, en=True)
        cmds.setParent("..")

        cmds.showWindow(self.NAME)

        cmds.scriptJob(parent=self.NAME, event=("SceneOpened", partial(self.close_window)))
        cmds.scriptJob(parent=self.NAME, event=("NewSceneOpened", partial(self.close_window)))

    def _open_export_window(self, *args):
        self.close_window()
        open_export_window()


def main():
    print("check scene [ mdl_ ]...")
    _ck = Checker()
    _ck.do_check()
