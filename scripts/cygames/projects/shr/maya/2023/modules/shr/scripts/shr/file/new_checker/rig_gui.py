# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from functools import partial
import glob
import os

import sys
import importlib

import maya.OpenMaya as om
from maya import cmds
import maya.mel

# from mtk.maya.utils.perforce import MtkP4

from . import node_check
from . import TITLE
from . import TOOL_NAME
from ...utils import getCurrentSceneFilePath


# 開発中はTrue、リリース時にFalse
DEV_MODE = True

if DEV_MODE:
    importlib.reload(node_check)


PATH = "Z:/mtk/tools/maya/2022/modules/mtk/scripts/mtk/file/new_checker"
PATH = 'C:/cygames/shrdev/shr/tools/in/ext/maya/2022/modules/shr/scripts/shr/file/new_checker'
PACKAGE = ".".join(PATH.split("/")[-3:])

EXT_DICT = {
    "ma": "mayaAscii",
    "mb": "mayaBinary"
}

ALLSET_NAME = "AllSet"
CTRLSET_NAME = "CtrlSet"
ANIMJTSET_NAME = "AnimJtSet"

# NAME = "mutsunokami_rig_checker_result_ui"


def _confirm_dialog(message, title=""):
    if not title:
        title = TITLE
    rflag = False
    flag = True
    while flag:
        result = cmds.confirmDialog(title=title,
                                    messageAlign="center",
                                    message=message,
                                    button=["OK", "Cansel"],
                                    defaultButton="OK",
                                    cancelButton="Cansel",
                                    dismissString="Cansel")
        if result == "Cansel":
            rflag = False
            flag = False
        else:
            rflag = True
            flag = False
    return rflag


def _message_dialog(message, title=""):
    if not title:
        title = TITLE

    cmds.confirmDialog(
        message=message,
        title=title,
        button=['OK'],
        defaultButton='OK',
        cancelButton="OK",
        dismissString="OK")

    print(u"{}".format(message))


def close_window():
    if cmds.window(TOOL_NAME, ex=True):
        cmds.deleteUI(TOOL_NAME)
    # try:
    #     cmds.deleteUI(NAME)
    # except:pass


class Checker(object):
    # NAME = "mutsunokami_rig_checker_result_ui"
    NAME = TOOL_NAME
    WINDOW = ""
    TITLE = u"以下の項目を確認してください"
    _text_a_width = 200
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
    scene_path = None
    ext = "ma"

    # def __init__(self):
    #     self.TITLE = u"以下の項目を確認してください"
    #     self._frame = "{}_frame".format(self.NAME)
    #     self._scroll = "{}_scroll".format(self.NAME)
    #     self._modify_btn = "{}_modify_btn".format(self.NAME)

    def memory_clear(self):
        self.convert_flag = False
        self.results = []
        self.modifies = []
        self.modify_errors = []

    def close_window(self):
        # print(cmds.window(NAME, ex=True), " ---- wind")
        # if cmds.window(self.NAME, ex=True):
        #     cmds.deleteUI(self.NAME)
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

    def get_scene_path(self):
        """
        cmds だとシーンパスをとれないシーンがあったので、
        それの対処としてAPI でパスを取得
        z:\mtk\work\resources\env\r000\s001_cage001\model\mdl_r000_s001_cage001_000.ma
        2021/01/08 現在
        """
        scene_path = getCurrentSceneFilePath()
        if not scene_path:
            scene_path = om.MFileIO.currentFile()

        """
        API でシーンパスを取ると、シーンが開かれていない場合、
        「Z:/mtk/work/resources/env/cmn/cmn_barrel000/untitled」
        のような形になるので、拡張子がないものはシーンパスがないものとして処理
        """
        if len(scene_path.split(".")) < 2:
            self.scene_path = None
        else:
            u"""
            Work エクスプローラから開くとドライブレターが小文字になる
            P4 モジュールでは認識されないのでドライブレターを大文字にする
            小文字のままだとP4 モジュールで認識してもらえない
            """

            drive, _ = os.path.splitdrive(scene_path)
            drive = drive.upper()
            scene_path = os.path.join(drive, _)

            self.scene_path = scene_path.replace(os.sep, '/')
            # self.ext = scene_path.rsplit(".", 1)[-1].lower()
            self.ext = os.path.basename(scene_path).split(".")[1].lower()

    def check_unknown(self):
        _unknown = node_check.check_unknown()
        _error_flag = False
        if _unknown:
            _unknown_error = _unknown[0]
            _unknown_result = _unknown[1]
            if _unknown_error:
                _error_flag = True
                _m = u"以下のノード、プラグインが削除できません\n"
                _m += u"{}\nご確認ください".format("\n".join(_unknown_error))
                _error_flag = True
                _message_dialog(_m)

            if _unknown_result:
                _m = u"以下のノード、プラグインを削除しました\n\n{}".format("\n".join(_unknown_result))
                _message_dialog(_m)

        return _error_flag

    def load_check_modules(self, node_type="rig", convert_scene_flag=False):
        path = os.path.join(PATH, node_type)

        """
        Z:/mtk/tools/maya/modules/mtku/scripts/mtku/maya/menus/file/new_checker/[rig]
        にある「py」ファイル、ファイル名が「__」（アンダーバー二つ）で始まらないもののみを
        読み込む
        """
        if convert_scene_flag:
            checker = os.path.join("check_convert_scene")
            self.load_moduls(node_type, checker)
        else:
            for checker in sorted(glob.glob(path + "/*.py")):
                checker = os.path.basename(checker).split(".")[0]

                if "check_convert_scene" == checker:
                    continue

                if not checker.startswith("__"):
                    self.load_moduls(node_type, checker)

    def load_moduls(self, node_type, checker):
        result = None
        modulename = "{}.{}.{}".format(PACKAGE, node_type, checker)

        exec('import {}'.format(modulename))
        print(modulename, " ---- module load")
        u"""
        開発時のホットリロード用
        """
        if DEV_MODE:
            exec('importlib.reload({})'.format(modulename))

        funcname = "{}.{}".format(modulename, "main")
        command = '{}("{}")'.format(funcname, self.scene_path)

        try:
            result = eval(command)
        except Exception as e:
            print(command, "----command")
            print(e, " ---- error node")

        if result:
            self.results.extend(result)

    def do_check(self):

        self.memory_clear()
        self.get_scene_path()
        print(self.scene_path, " ---  self.scene_path")
        if not self.scene_path:
            _message_dialog(u"シーンを開いてから実行してください")
            return

        if self.check_unknown():
            return

        basename = os.path.basename(self.scene_path)
        namebase, ext = os.path.splitext(basename)

        if namebase.endswith("_convert"):
            self.convert_flag = True
            self.load_check_modules(convert_scene_flag=True)
        else:
            self.load_check_modules(convert_scene_flag=False)

        if self.results:
            self.result_window()
        else:
            self.save_scene()
        # print("\n\n")
        # print("check------")
        # print cmds.window("mutsunokami_rig_checker_result_ui",ex=1)
        # print("\n\n")

    def save_scene(self):
        return
        _save_flag = False

        file_status_ext = MtkP4.status_ext([self.scene_path])

        """
        P4 のステータス確認
        None P4管理のファイルでない
        checkout されておらず、latest 最新バージョンでない場合はシーンの保存をしない
        """
        if file_status_ext:
            if file_status_ext[self.scene_path]["action"] != "checkout":
                if file_status_ext[self.scene_path]["action"] != "latest":
                    _m = u"チェックは全て完了しました\n\n"
                    _m += u"シーンは最新バージョンではありませんので、シーンの保存は行いませんでした\n"
                    _m += u"最新のシーンを取得した後、再度ツールを実行してください"
                    _message_dialog(_m)

                    return

        if cmds.file(self.scene_path, q=True, w=True):
            cmds.file(save=True, force=True, type=EXT_DICT[self.ext])
            _save_flag = True
        elif file_status_ext[self.scene_path]["action"]:
            flag = True
            while flag:
                _m = u'シーンに問題はありませんでした\n\n'
                _m = u'ファイルがチェックアウトされておりません\n'
                _m += u'チェックアウトしてからシーンを上書き保存しますか？'

                result = _confirm_dialog(_m)

                if not result:
                    _message_dialog(u"シーンは保存されませんでした")
                    return
                else:
                    flag = False
            try:
                MtkP4.edit([self.scene_path])
                cmds.file(save=True, force=True, type=EXT_DICT[self.ext])
                _save_flag = True

            except Exception as e:
                print(e)
                _m = u"!! シーンを保存できませんでした"
                cmds.error(_m)
                _message_dialog(_m)

        if _save_flag:
            _m = u"シーンを上書き保存しました\n\n"
            _m += u"[ {} ]".format(self.scene_path)
            _message_dialog(_m)

            print("\n")
            print("save scene -- [ {} ]".format(self.scene_path.replace(os.sep, '/')))
            print("\n")

    def result_window(self):
        self.close_window()
        # if cmds.window(self.NAME, ex=True):
        #     cmds.deleteUI(self.NAME)
        cmds.window(
            self.NAME,
            title=self.TITLE,
            width=self._window_width,
            height=self._window_height
        )

        cmds.frameLayout(self._frame,
                         marginHeight=10,
                         marginWidth=10,
                         labelVisible=False,
                         width=self._frame_width)

        cmds.rowLayout(nc=4,
                       adj=2,
                       cw4=[self._text_a_width,
                            self._spacing,
                            self._text_b_width,
                            self._button_a_width],
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

        for result in self.results:

            ann = u"None"
            button_name = None

            text = result[0]
            _type = result[1]
            node = result[-1]

            if node:
                if isinstance(node, list):
                    ann = u"{}...".format(node[0])
                    button_name = node[0]
                else:
                    ann = u" > ".join(node.split("|"))
                    button_name = node.split("|")[-1]
            else:
                # ann = "{}...".format("")
                button_name = "None"

            bgc = [0.2, 0.2, 0.2]
            if ANIMJTSET_NAME in _type:
                bgc = [0.3, 0.3, 0.5]
            elif CTRLSET_NAME in _type:
                bgc = [0.5, 0.3, 0.3]
            elif "reference" in _type:
                bgc = [0.3, 0.5, 0.3]
            elif "name" in _type:
                bgc = [0.3, 0.5, 0.5]
            elif "transform" in _type:
                bgc = [0.2, 0.3, 0.5]
            elif "joint" in _type:
                bgc = [0.5, 0.5, 0.2]
            elif "group" in _type:
                bgc = [0.5, 0.2, 0.5]
            elif "keyframe" in _type:
                bgc = [0.6, 0.2, 0.2]
            elif "Display Layer":
                bgc = [0.3, 0.7, 0.2]
            elif "No Default":
                bgc = [0.8, 0.2, 0.2]

            cmds.rowLayout(nc=4, adj=2,
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
                      ann=u"[ {} ]".format(ann)
                      )
            cmds.text(l="")
            cmds.text(l=_type,
                      w=self._text_b_width,
                      h=self._row_height,
                      al="center",
                      bgc=bgc
                      )

            if button_name != "None":
                ann = u"[ {} ]".format(ann)
                ann += u"\n[ Ctrl ] キーを押しながらで追加選択"
            cmds.button(l=button_name,
                        c=partial(self.select_error_nodes, node, _type),
                        w=self._button_a_width,
                        ann=u"{}".format(ann)
                        )
            cmds.setParent("..")
            cmds.separator(h=self._separetor_height)

        cmds.setParent("..")

        _btn_ann = u"sets へのメンバー追加、不要なコンストレイントの削除、\n"
        _btn_ann += u"リファレンスデータのネームスペースの修正、\n"
        _btn_ann += u"キーフレームの削除、トランスフォームのリセットを行います"

        cmds.button(self._modify_btn,
                    l=u"解決できるエラーを修正し　再検査",
                    c=partial(self.modify_data),
                    ann=_btn_ann,
                    en=True)

        if self.convert_flag:
            cmds.button(self._modify_btn, e=True, en=False)

        # if self.results:
        #     cmds.button(self._modify_btn, e=True, en=True)

        cmds.setParent("..")

        cmds.showWindow(self.NAME)

        cmds.scriptJob(parent=self.NAME, event=("SceneOpened", partial(self.close_window)))
        cmds.scriptJob(parent=self.NAME, event=("NewSceneOpened", partial(self.close_window)))

    def create_sets(self, sets_name):
        # return cmds.sets(sets_name)
        return cmds.createNode("objectSet", n=sets_name, ss=True)

    def modify_data(self, *args):

        self.close_window()

        _all_joint_nodes = cmds.ls(type="joint")
        _reference_nodes = [x for x in cmds.ls(type='reference',
                                               long=True) if "sharedReferenceNode" != x.split(":")[-1]]

        check_joints = []

        if _reference_nodes:
            check_joints = list(set(_all_joint_nodes) &
                                set(cmds.referenceQuery(_reference_nodes, nodes=True)))

        _all_set = None
        _ctrl_set = None
        _anim_jnt_set = None

        if cmds.objExists(ALLSET_NAME):
            _all_set = cmds.ls(ALLSET_NAME, type="objectSet")

        if cmds.objExists(CTRLSET_NAME):
            _ctrl_set = cmds.ls(CTRLSET_NAME, type="objectSet")

        if cmds.objExists(ANIMJTSET_NAME):
            _anim_jnt_set = cmds.ls(ANIMJTSET_NAME, type="objectSet")

        for result in self.results:
            # text = result[0]
            _type = result[1]
            node = result[-1]

            if _type == "{} {}".format(ALLSET_NAME, "name"):
                _all_set = cmds.rename(node, ALLSET_NAME)

            if _type == ALLSET_NAME:
                _all_set = self.create_sets(ALLSET_NAME)

            if _type == "reference":
                _reference_nodes = [x for x in cmds.ls(type='reference',
                                                       long=True) if "sharedReferenceNode" != x]
                if _reference_nodes:
                    referance_path = cmds.referenceQuery(_reference_nodes, f=True)
                    cmds.file(referance_path, removeReference=True)
                    _ref = cmds.file(referance_path,
                                     r=True,
                                     type="mayaAscii",
                                     ignoreVersion=True,
                                     gl=True,
                                     mergeNamespacesOnClash=False,
                                     namespace=":",
                                     options="v=0;")

                    if not cmds.objExists(ANIMJTSET_NAME):
                        _anim_jnt_set = self.create_sets(ANIMJTSET_NAME)
                        cmds.sets(_anim_jnt_set, edit=True, forceElement=ALLSET_NAME)

                    # _all_joint_nodes = cmds.ls(type="joint")
                    # _reference_nodes = [x for x in cmds.ls(type='reference',
                    #                                         long=True) if "sharedReferenceNode" != x]

                    # check_joints = list(set(_all_joint_nodes) &
                    #                     set(cmds.referenceQuery(_reference_nodes, nodes=True)))

                    _root_node = []
                    for _r in cmds.referenceQuery(_reference_nodes, n=True):
                        long_name = cmds.ls(_r, l=True)[0]
                        if (cmds.nodeType(_r) == "transform"
                                and len(long_name.split("|")) == 2
                                and _r.startswith("mdl_")
                                and not _r.endswith("RN")):
                            _root_node.append(_r)
                            break

                    _model_group = cmds.ls("|root|model", l=True)
                    if _root_node and _model_group:
                        cmds.parent(_root_node, _model_group)

                    if check_joints:
                        for jnt in check_joints:
                            try:
                                cmds.sets(jnt, edit=True, forceElement=ANIMJTSET_NAME)
                                _text = u"[ {} ] を [ {} ] のメンバーに".format(jnt, ANIMJTSET_NAME)
                                self.modifies.append(_text)
                            except Exception as e:
                                _text = u"[ {} ] を [ {} ] のメンバーにできない".format(jnt, ANIMJTSET_NAME)
                                self.modify_errors.append(_text)
                                print(e, " ++ anim jnt sets error")
                                print("{:+<100}  {} {}".format(jnt, ANIMJTSET_NAME, "anim jnt sets error"))

            if _type == "{} {}".format(CTRLSET_NAME, "name"):
                _ctrl_set = cmds.rename(node, CTRLSET_NAME)

            if _type == CTRLSET_NAME:
                if not cmds.objExists(CTRLSET_NAME):
                    _ctrl_set = self.create_sets(CTRLSET_NAME)

                if node and node != _ctrl_set:
                    try:
                        cmds.sets(node, edit=True, forceElement=CTRLSET_NAME)
                        _text = u"[ {} ] を [ {} ] のメンバーに".format(node, CTRLSET_NAME)
                        self.modifies.append(_text)
                    except Exception as e:
                        # _text = u"[ {} ] を [ {} ] のメンバーにできない".format(node, CTRLSET_NAME)
                        # self.modify_errors.append(_text)
                        print(e, " ++ ctrl sets error")
                        print("{:+<100}  {} {}".format(node, CTRLSET_NAME, "ctrl sets error"))
                # else:

                #     _ctrl_nodes = [x for x in cmds.ls("*_ctrl",
                #             type="transform") if cmds.listRelatives(x, p=False, type="nurbsCurve")]
                #     if _ctrl_nodes:
                #         cmds.sets(_ctrl_nodes, edit=True, forceElement=_ctrl_set)

            if not cmds.sets(_all_set, q=True):
                cmds.sets(_ctrl_set, edit=True, forceElement=ALLSET_NAME)

            _set_members = cmds.sets(_all_set, q=True)
            # _anim_jnt_set = self.create_sets(ANIMJTSET_NAME)
            # else:
            #     if _ctrl_set not in _set_members:
            #         cmds.sets(_ctrl_set, edit=True, forceElement=_all_set)

            if _type == "{} {}".format(ANIMJTSET_NAME, "name"):
                _anim_jnt_set = cmds.rename(node, ANIMJTSET_NAME)

            if _type == ANIMJTSET_NAME:
                if not cmds.objExists(ANIMJTSET_NAME):
                    _anim_jnt_set = self.create_sets(ANIMJTSET_NAME)

                if node and node != _anim_jnt_set:
                    try:
                        cmds.sets(node, edit=True, forceElement=ANIMJTSET_NAME)
                        _text = u"[ {} ] を [ {} ] のメンバーに".format(node, ANIMJTSET_NAME)
                        self.modifies.append(_text)
                    except Exception as e:
                        # _text = u"[ {} ] を [ {} ] のメンバーにできない".format(node, ANIMJTSET_NAME)
                        # self.modify_errors.append(_text)
                        print(e, " ++ sets error")
                        print("{:+<100}  {} {}".format(node, ANIMJTSET_NAME, "sets error"))
                elif not node and check_joints:
                    for jnt in check_joints:
                        try:
                            cmds.sets(jnt, edit=True, forceElement=ANIMJTSET_NAME)
                            _text = u"[ {} ] を [ {} ] のメンバーに".format(jnt, ANIMJTSET_NAME)
                            self.modifies.append(_text)
                        except Exception as e:
                            _text = u"[ {} ] を [ {} ] のメンバーにできない".format(jnt, ANIMJTSET_NAME)
                            self.modify_errors.append(_text)
                            print(e, " ++ anim jnt sets error")
                            print("{:+<100}  {} {}".format(jnt, ANIMJTSET_NAME, "anim jnt sets error"))

            if _anim_jnt_set not in _set_members:
                cmds.sets(_anim_jnt_set, edit=True, forceElement=ALLSET_NAME)
            # _anim_jnt_set = cmds.ls(ANIMJTSET_NAME, type="objectSet")
            # if _anim_jnt_set:
            #     try:
            #         cmds.sets(_anim_jnt_set, edit=True, forceElement=_all_set)
            #         _text = u"[ {} ] を [ {} ] のメンバーに".format(_anim_jnt_set, _all_set)
            #         self.modifies.append(_text)
            #     except Exception as e:
            #         _text = u"[ {} ] を [ {} ] のメンバーにできない".format(_anim_jnt_set, _all_set)
            #         self.modify_errors.append(_text)
            #         print(e, " ++ sets error")
            #         print("{:+<100}  {} {}".format(_anim_jnt_set, _all_set, "sets error"))

            # _ctrl_set = cmds.ls(CTRLSET_NAME, type="objectSet")
            # if _ctrl_set:
            #     try:
            #         cmds.sets(_ctrl_set, edit=True, forceElement=_all_set)
            #         _text = u"[ {} ] を [ {} ] のメンバーに".format(_ctrl_set, _all_set)
            #         self.modifies.append(_text)
            #     except Exception as e:
            #         _text = u"[ {} ] を [ {} ] のメンバーにできない".format(_ctrl_set, _all_set)
            #         self.modify_errors.append(_text)
            #         print(e, " ++ sets error")
            #         print("{:+<100}  {} {}".format(_ctrl_set, _all_set, "sets error"))

            if _type == "keyframe":
                try:
                    cmds.cutKey(node, cl=True)
                    self.modifies.append(u"[ {} ] の [ キーフレーム ] を削除".format(node))
                    print("{:-<100}  {}".format(node, "delete key frame"))
                except Exception as e:
                    _m = u"!! [ {} ] の [ キーフレーム ] を削除できない".format(node)
                    self.modify_errors.append(_m)
                    print(e, " ++ delete key frame error")
                    print("{:+<100}  {}".format(node, "delete key frame error"))

            if _type == "transform":
                u"""
                子のノードがロックされているとフリーズできないのでその対応
                connectionInfo を使わないといけない場面があった
                スケールを使わない（キーを打てない）リグがあるため機構追加
                """
                for _attr in ["t", "r", "s"]:
                    if self.unlock_attribute(node, _attr):
                        _r = self.reset_attribute_values(node, _attr)
                        if _r:
                            self.modifies.append(u"[ {} ] の [ {} ] をリセット".format(node, _attr))
                            print("{:-<100}  {} [ {} ]".format(node, "reset attribute", _attr))
                        elif _r == -1:
                            self.modify_errors.append(u"[ {} ] の [ {} ] をリセットできない".format(
                                node, _attr))
                            print("{:+<100}  {} [ {} ]".format(node, "can not reset attribute", _attr))

            if _type == "constraint":
                """
                コンストレイントノードを削除
                """
                _constraints = cmds.listRelatives(node, type="constraint", fullPath=True)
                for _constraint in _constraints:
                    try:
                        cmds.delete(_constraint)
                        self.modifies.append(u"[ {} ] を削除".format(_constraint))
                        print("{:-<100}  {}".format(_constraint, "delete constraint"))
                    except Exception as e:
                        self.modify_errors.append(u"[ {} ] を削除できない".format(_constraint))
                        print("{:+<100}  {}".format(_constraint, "delete constraint error"))

            if _type == "unnecessary":
                """
                仕様にないノードを削除する
                リファレンスは削除できないので、必要があれば作る
                """
                continue
                try:
                    cmds.delete(node)
                    self.modifies.append(u"[ {} ] の [ ノード ] を削除".format(node))
                    print("{:-<100}  {}".format(node, "delete Node"))
                except Exception as e:
                    self.modify_errors.append(u"!! [ {} ] の [ ノード ] を削除できない".format(node))
                    print("{:+<100}  {}".format(node, "delete Node error"))

            if _type == "Display Layer" or _type == "plugin":
                try:
                    cmds.delete(node)
                    self.modifies.append(u"[ {} ] の [ ノード ] を削除".format(node))
                    print("{:-<100}  {}".format(node, "delete Node"))
                except Exception as e:
                    self.modify_errors.append(u"!! [ {} ] の [ ノード ] を削除できない".format(node))
                    print("{:+<100}  {}".format(node, "delete Node error"))

        if self.modify_errors:
            self.open_modify_error()
        if self.modifies:
            self.open_modify_result()

        self.do_check()

    def reset_attribute_value(self, node, attr):
        """
        単体のアトリビュート用、使用していない
        """
        _values = abs(round(cmds.getAttr("{}.{}".format(node, attr))))
        _reset = 0.0
        _flag = False

        if attr[0] == "s":
            _reset = 1.0
            if _values != _reset:
                cmds.setAttr("{}.{}".format(node, attr), _reset)
                _flag = True
        else:
            if _values != _reset:
                cmds.setAttr("{}.{}".format(node, attr), _reset)
                _flag = True
        return _flag

    def reset_attribute_values(self, node, attr):
        """
        スケールの場合は「1.0」がデフォルト値、それ以外は「0.0」がデフォルト値
        デフォルト値ではないものをデフォルト値にする
        値の設定に失敗したら「-1」を返す
        """
        _values = [abs(round(x)) for x in cmds.getAttr("{}.{}".format(node, attr))[0]]
        _axis = ["x", "y", "z"]

        _flag = -1

        _reset = 0.0
        if attr == "s":
            _reset = 1.0

        if _values != [_reset, _reset, _reset]:
            for axis in _axis:
                _attr = "{}{}".format(attr, axis)
                if _attr in cmds.listAttr(node, sn=True, k=True):
                    cmds.setAttr("{}.{}".format(node, _attr), _reset)
                    _flag = True
        else:
            _flag = False

        return _flag

    def unlock_attribute(self, node, attr):
        u"""
        connectionInfo を使わないとロックを解除できないケースがある
        ただ、その場合はconnectionInfoで取得する前に一度setAttrでロックを解除しておく必要があるようだ
        """
        _flag = False
        try:
            cmds.setAttr("{}.{}".format(node, attr), l=False)
            plug_name = cmds.connectionInfo("{}.{}".format(node, attr), gla=True)
            # print(attr, " attr---")
            # print(plug_name)
            if plug_name:
                cmds.setAttr(plug_name, l=False)
            _flag = True
        except:
            pass
        return _flag

    def open_modify_error(self):
        cmds.confirmDialog(
            message=u"\n".join(self.modify_errors),
            title=u'!! 修正できませんでした',
            button=['OK'],
            defaultButton='OK',
            cancelButton="OK",
            dismissString="OK")

    def open_modify_result(self):
        cmds.confirmDialog(
            message=u"\n".join(self.modifies),
            title=u'修正項目',
            button=['OK'],
            defaultButton='OK',
            cancelButton="OK",
            dismissString="OK")

    def select_error_nodes(self, node, node_type, *args):
        # print("select function -------")
        # print(node, "---node")
        # print(node_type, "---node type")

        if not node:
            return

        modifiers = cmds.getModifiers()

        if "comp" in node_type:
            visible_node = node[0].rsplit(".", 1)[0]
        else:
            visible_node = node

        if not cmds.objExists(visible_node):
            return

        if (modifiers & 4) > 0:
            cmds.select(node, add=True)
        else:
            cmds.select(node, r=True)

        if node_type == "material" or node_type == "texture":
            return

        # if node_type != "compornent":
        if "visibility" in cmds.listAttr(visible_node):
            if self.unlock_attribute(visible_node, "visibility"):
                cmds.setAttr("{}.visibility".format(visible_node), 1)
                for n in node_check.iterUpNode(visible_node):
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

        _outliners = [x for x in cmds.getPanel(type="outlinerPanel") if x in cmds.getPanel(vis=True)]

        if _outliners:
            [cmds.outlinerEditor(x, e=True, sc=True) for x in _outliners]


def main():
    _ck = Checker()
    _ck.do_check()

    if not DEV_MODE:
        logger.send_launch(u'ツール起動')
