# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import OrderedDict
import os

from PySide2 import QtCore, QtGui, QtWidgets

import maya.cmds as cmds

from . import DEFAULT_REFERENCE_NAME, DEFAULT_REFERENCE_PATH
from . import EXT_DICT

VARIATION_SETTINGS = "{}_{}_variation_settings"
JSON_FILE_NAME = "mdl_variation[{}].dtblj"


def clean_reference_path(_path=""):
    """リファレンスファイル名のクリーンナップ
    Z:/mtk/work/resources/rigs/prop/arw/00/000/rig_prp_arw00_000.ma{1}
    という名前にされる場合があるので、{1}の部分を取って返す

    Args:
        _path ([str]): reference file path

    Returns:
        [str]: reference file path
    """
    _path, ext = os.path.splitext(_path)
    _split_index = ext.find("{")
    if _split_index != -1:
        ext = ext[:-_split_index]
    _path = _path + ext
    return _path

class ConformDialogResult(QtWidgets.QDialog):
    """[summary]

    Args:
        QtWidgets ([type]): [description]

    使い方例
    _m = u"マテリアルをアサインする対象が選ばれておりません\n"
    _m += u"マテリアルアサインをせずにマテリアルを生成しますか？"
    _d = ConformDialogResult(title=u"マテリアル生成",
                    message=_m)
    result = _d.exec_()
    if not result:
        return

    """

    def __init__(self, *args, **kwargs):
        super(ConformDialogResult, self).__init__(
            parent=kwargs.setdefault('parent', None),
            f=QtCore.Qt.WindowFlags())

        self.setWindowTitle(kwargs.setdefault('title', 'title'))

        main_layout = QtWidgets.QVBoxLayout()
        btn_layout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel(kwargs.setdefault('message', 'message'))
        self._ok_btn = QtWidgets.QPushButton('OK')
        self._cancel_btn = QtWidgets.QPushButton('Cancel')

        main_layout.addWidget(label)
        main_layout.addLayout(btn_layout)
        btn_layout.addWidget(self._ok_btn)
        btn_layout.addWidget(self._cancel_btn)
        self.setLayout(main_layout)

        self._ok_btn.clicked.connect(self._ok_btn_clicked)
        self._cancel_btn.clicked.connect(self._cancel_btn_clicked)

    def _ok_btn_clicked(self, *args):
        self.close()
        self.setResult(True)

    def _cancel_btn_clicked(self, *args):
        self.close()
        self.setResult(False)


class ConformDialog(QtWidgets.QDialog):
    """[summary]

    Args:
        QtWidgets ([type]): [description]

    使い方例
    _d = ConformDialog(title=u"一覧から選択してください",
                    message=u"マテリアルに適用するテクスチャを選択してから実行してください")
    _d.exec_()
    return
    """
    def __init__(self, *args, **kwargs):
        super(ConformDialog, self).__init__(
            parent=kwargs.setdefault('parent', None),
            f=QtCore.Qt.WindowFlags())

        self.setWindowTitle(kwargs.setdefault('title', 'title'))

        _label = QtWidgets.QLabel(kwargs.setdefault('message', 'message'))

        _btn = QtWidgets.QPushButton("OK")
        _btn.clicked.connect(self._btn_clicked)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(_label)
        layout.addWidget(_btn)
        self.setLayout(layout)

    def _btn_clicked(self, *args):
        self.close()
        self.setResult(False)


class ReferenceNodeFilePath(object):
    """リファレンス情報格納クラス

    Args:
        object ([type]): [description]
    """
    def __init__(self, node_name="", default_file_path=""):
        self.node_name = node_name
        self.default_file_path = default_file_path
        self.current_file_path = default_file_path
        self.json_path = ""

    def get_node_name(self):
        return self.node_name

    def get_current_path(self):
        return self.current_file_path

    def get_default_path(self):
        return self.default_file_path

    def get_json_path(self):
        self.get_json_file()
        return self.json_path

    def get_json_file(self):
        """現在読み込まれているモデルのバリエーションデータがあればパスを記憶
        """
        json_path, basename = os.path.split(self.current_file_path)
        json_path, _ = os.path.split(json_path)
        json_path, _ = os.path.split(json_path)

        filename, ext = basename.split(".", 1)
        chara_type_fullname = filename[4:]
        name_split = chara_type_fullname.split("_")
        chara_category = name_split[0]
        chara_type = name_split[1]
        chara_id = name_split[-1]

        current_variation = VARIATION_SETTINGS.format(chara_category, chara_type)
        current_variation = JSON_FILE_NAME.format(current_variation)
        json_path = os.path.join(json_path, current_variation).replace(os.sep, '/')
        if os.path.exists(json_path):
            self.json_path = json_path
        else:
            self.json_path = ""

    def set_default_referance_path(self):
        """ツール起動時のモデルに戻す
        """
        self.replace_referance_model()

    def replace_referance_model(self, new_file_path=""):
        """読み込まれているモデルの変更
        new_file_path がない場合はデフォルトに戻す仕様

        Args:
            new_file_path (str): モデルのファイルパス
        """
        _default_flag = False
        if not new_file_path:
            _default_flag = True
            new_file_path = self.default_file_path
            if self.current_file_path == new_file_path:
                return

        new_file_path = new_file_path.replace(os.sep, '/')
        if not _default_flag:
            _m = u"[ {} ] を\n\n{}\n\nで置き換えますか？".format(self.node_name, new_file_path)
            _d = ConformDialogResult(title=u"リファレンスの置き換え",
                            message=_m)
            result = _d.exec_()
            if not result:
                return

        _path, ext = new_file_path.split(".", 1)
        file_type = EXT_DICT.get(ext, None)

        if file_type:
            cmds.file(
                    new_file_path,
                    loadReference=self.node_name,
                    type=file_type,
                    options = "v=0;"
                    )
            self.current_file_path = new_file_path

    def __repr__(self):
        return self.node_name

def get_groups(reference_node_name):
    """リファレンス内のバリエーショングループを取り出す

    Args:
        reference_node_name (str): reference node name

    Returns:
        [dict]: グループ名: 該当ノード
    """
    group_basename_node = OrderedDict()
    if  cmds.ls(reference_node_name, type="reference"):
        for x in cmds.referenceQuery(reference_node_name, nodes=True):
            if x.split(":")[-1].startswith("sbm"):
                # LOD グループも取ってしまうが、model グループの方が先に取れるので
                # インデックスで取得してmodel ノードにあるグループを取っている
                # シーンによっては通用しないかもしれない
                node = cmds.ls(x, l=True)[0]
                if cmds.nodeType(node) != "transform":
                    continue
                # |ply00_m_000_000:mdl_mob03_m_000|ply00_m_000_000:model|ply00_m_000_000:default_grp|ply00_m_000_000:sbm0_default_002_grp
                # から「default_002_grp」を抽出したい
                name = node.split(":")[-1]
                name = name[5:]
                # group_basename_node[name] = VariationNode(node)
                group_basename_node[name] = node
    return group_basename_node




def get_json_path(scene_name = ""):

    json_path, basename = os.path.split(scene_name)
    json_path, _ = os.path.split(json_path)
    json_path, _ = os.path.split(json_path)

    filename, ext = basename.split(".", 1)
    chara_type_fullname = filename[4:]
    name_split = chara_type_fullname.split("_")
    chara_category = name_split[0]
    chara_type = name_split[1]
    chara_id = name_split[-1]

    current_variation = VARIATION_SETTINGS.format(chara_category, chara_type)

    current_variation = JSON_FILE_NAME.format(current_variation)

    json_path = os.path.join(json_path, current_variation).replace(os.sep, '/')


    if os.path.exists(json_path):
        return json_path
    else:
        return


class VariationNode(object):
    def __init__(self, node):
        self.node = node
        # name = node.split(":")[-1]
        # name = name[5:]
        # self.name = name
        self.visible = cmds.getAttr("{}.v".format(self.node))

    def set_visible(self, visible=True):
        if cmds.objExists(self.node):
            cmds.setAttr("{}.v".format(self.node), visible)
            self.visible = visible

    def __repr__(self):
        return self.node



# def get_groups():
#     group_basename_node = OrderedDict()
#     if  cmds.ls(DEFAULT_REFERENCE_NAME, type="reference"):
#         for x in cmds.referenceQuery(DEFAULT_REFERENCE_NAME, nodes=True):
#             if x.split(":")[-1].startswith("sbm"):
#                 # LOD グループも取ってしまうが、model グループの方が先に取れるので
#                 # インデックスで取得してmodel ノードにあるグループを取っている
#                 # シーンによっては通用しないかもしれない
#                 node = cmds.ls(x, l=True)[0]
#                 if cmds.nodeType(node) != "transform":
#                     continue
#                 # |ply00_m_000_000:mdl_mob03_m_000|ply00_m_000_000:model|ply00_m_000_000:default_grp|ply00_m_000_000:sbm0_default_002_grp
#                 # から「default_002_grp」を抽出したい
#                 name = node.split(":")[-1]
#                 name = name[5:]
#                 # group_basename_node[name] = VariationNode(node)
#                 group_basename_node[name] = node
#     return group_basename_node

