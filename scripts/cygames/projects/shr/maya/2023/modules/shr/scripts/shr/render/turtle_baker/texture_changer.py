# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

from functools import partial

import glob
import os
import sys

import maya.cmds as cmds

tool_title = 'Texture Changer'
tool_title_jp = u"カラーマップ入れ替え"
project = "mutsunokami"
toolcategory = 'Maya'
version = '1.0'

NAME = "{}_ui".format("_".join(tool_title.split()))
RADIO_BTN_COLLECTION_NAME = "{}_radio_btn_ui".format("_".join(tool_title.split()))

def create_file_node(mat, file_path):
    directory, file_name = os.path.split(file_path)
    file_node = cmds.shadingNode(
        'file',
        name="{}_{}".format(NAME, file_name.replace(".", "_")),
        asTexture=True
    )
    texture2d_node = cmds.shadingNode(
        'place2dTexture',
        name='place2dTexture',
        asUtility=True
    )
    cmds.connectAttr(
        file_node + '.outColor',
        mat + '.color',
        force=True
    )
    # cmds.connectAttr(
    #     file_node + '.outAlpha',
    #     source_material + '.opacity.opacityG',
    #     force=True
    # )
    # cmds.connectAttr(
    #     file_node + '.outAlpha',
    #     source_material + '.opacity.opacityB',
    #     force=True
    # )
    cmds.connectAttr(
        texture2d_node + '.coverage',
        file_node + '.coverage',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.translateFrame',
        file_node + '.translateFrame',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.rotateFrame',
        file_node + '.rotateFrame',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.mirrorU',
        file_node + '.mirrorU',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.mirrorV',
        file_node + '.mirrorV',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.stagger',
        file_node + '.stagger',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.wrapU',
        file_node + '.wrapU',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.wrapV',
        file_node + '.wrapV',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.repeatUV',
        file_node + '.repeatUV',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.offset',
        file_node + '.offset',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.rotateUV',
        file_node + '.rotateUV',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.noiseUV',
        file_node + '.noiseUV',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.vertexUvOne',
        file_node + '.vertexUvOne',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.vertexUvTwo',
        file_node + '.vertexUvTwo',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.vertexUvThree',
        file_node + '.vertexUvThree',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.vertexCameraOne',
        file_node + '.vertexCameraOne',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.outUV',
        file_node + '.uv',
        force=True
    )
    cmds.connectAttr(
        texture2d_node + '.outUvFilterSize',
        file_node + '.uvFilterSize',
        force=True
    )
    cmds.setAttr(
        file_node + '.fileTextureName',
        file_path,
        type='string'
    )
    return file_node


class TextureChanger(object):
    _window_width = 330
    _window_hight = 150
    frame = "{}_{}_ui".format(NAME, "frame")
    radio_btn_collection_name = RADIO_BTN_COLLECTION_NAME

    def __init__(self):
        self._clear_memory()

    def _clear_memory(self):
        self.radio_buttons = []
        self.mat_color_tex_dict = {}
        self.mat_tex_dict = {}
        self.all_suffixs = []
        self.rows = []
        self.texts = []
        self.rad_col = ""
        self.error_text = ""

    def create(self):
        try:
            cmds.deleteUI(NAME)
        except:pass

        cmds.window(NAME, title=tool_title_jp,
                            width=self._window_width,
                            height=self._window_hight,
                            resizeToFitChildren=True)

        cmds.columnLayout(adjustableColumn=True)

        cmds.frameLayout(self.frame, labelVisible=False, width=self._window_width)
        cmds.setParent("..")
        # cmds.button(label="Reload",
        #             command=partial(self._reload))
        cmds.setParent("..")
        cmds.showWindow(NAME)
        self._reload()
        cmds.scriptJob(parent=NAME, event=["PostSceneRead", partial(self._reload)])
        cmds.scriptJob(parent=NAME, event=["NewSceneOpened", partial(self._reload)])

    def _delete_check_box(self, *args):
        # _radio_button = cmds.frameLayout(self.frame, q=True, childArray=True)
        # if not self.radio_buttons:
        #     return
        if self.radio_buttons:
            cmds.deleteUI(self.radio_buttons)
        if self.texts:
            cmds.deleteUI(self.texts)
        if self.rows:
            cmds.deleteUI(self.rows)
        if self.rad_col:
            cmds.deleteUI(self.rad_col)
        if self.error_text:
            cmds.deleteUI(self.error_text)

        self._clear_memory()


    def _reload(self, *args):
        self._delete_check_box()
        _error_flag = False

        sgs = cmds.ls(type="shadingEngine")
        if sgs:
            for sg in sgs:
                _suffix_dict = {}
                connections = cmds.listConnections(sg, s=True, d=False)
                if not connections:
                    continue

                mat = cmds.ls(connections, mat=True)
                if not mat:
                    continue
                mat = mat[0]

                connections = cmds.listConnections(mat, s=True, d=False, p=True, c=True)
                if not connections:
                    continue
                
                input_index = 0
                color_texture = ""

                for i,c in enumerate(connections):
                    if c.endswith(".color"):
                        input_index = i
                    if c.endswith(".outColor") and i == input_index+1:
                        input_color = c.split(".")[0]
                        if cmds.objectType(input_color) == "file":
                            color_texture = input_color
                
                if color_texture:
                    self.mat_color_tex_dict[mat] = color_texture
                    _path = cmds.getAttr("{}.ftn".format(color_texture)).replace(os.sep, '/')
                    _directory, _basename = os.path.split(_path)
                    _file_name, _ext = _basename.split(".")
                    if "_" not in _file_name:
                        continue
                    _name, _suffix = _file_name.rsplit("_",1)
                    _all_texs = [x.replace(os.sep, '/') for x in glob.glob(os.path.join(_directory, _name + "*"))]
                    if _all_texs:
                        for _tex in _all_texs:
                            _suffix_dict[_tex.rsplit("_",1)[-1].split(".")[0]] = _tex
                        self.mat_tex_dict[mat] = _suffix_dict
        else:
            _error_flag = True
        
        self._build_ui(_error_flag)
    
    def _build_ui(self, _error_flag=False):
        if not self.mat_tex_dict or _error_flag:
            _error_message= u"\n\n適合するマテリアルかテクスチャがシーンにありません\n\n"
            self.error_text = cmds.text(label=_error_message, p=self.frame)
            return
        _all_suffixs = []
        for k,v in self.mat_tex_dict.items():
            _all_suffixs.extend(v.keys())
        _all_suffixs = sorted(list(set(_all_suffixs)))

        self.rad_col = cmds.radioCollection(self.radio_btn_collection_name, p=self.frame)
        for _suffix in _all_suffixs:
            _mats = ["[ {} ]".format(k) for k,v in self.mat_tex_dict.items() if _suffix in v]
            _row = cmds.rowLayout(nc=2, adj=2, cw2=(80, 150), cl2=["left", "left"], p=self.frame)
            
            # _rad = cmds.radioButton(label="{}  {}".format(_suffix, " ,".join(_mats)), p=self.frame)
            # _rad = cmds.radioButton(label=u"{:<20}合計[{:^5}]マテリアル".format(_suffix, len(_mats)), p=self.frame)
            _rad = cmds.radioButton(label="{:<20}".format(_suffix),
                                    w=80,
                                    h=30,
                                    bgc=(0.2, 0.2, 0.2))
            _text = cmds.text(label=u" 　  合計 [{:^5}] 個のマテリアルで使用されている".format(len(_mats)))
            cmds.setParent('..')
            cmds.radioButton(_rad, e=True, onc=partial(self._select_radio_button, _suffix))
            self.texts.append(_text)
            self.rows.append(_row)
            self.radio_buttons.append(_rad)
        cmds.setParent('..')
    
    def _select_radio_button(self, *args):
        _suffix = args[0]
        for mat,suffix_tex_dict in self.mat_tex_dict.items():
            if _suffix in suffix_tex_dict.keys():
                # 既存のファイルノードに接続するとエラーが出るので
                # 特定の名前でないと作り直す処理
                # でもエラーが出るのでつなぎ直すだけにした

                # if self.mat_color_tex_dict[mat].startswith(NAME):
                #     try:
                #         cmds.setAttr("{}.ftn".format(self.mat_color_tex_dict[mat]), suffix_tex_dict[_suffix], type = "string")
                #     except Exception as e:
                #         print(e)
                # else:
                #     file_node = create_file_node(mat, suffix_tex_dict[_suffix])
                #     self.mat_color_tex_dict[mat] = file_node
                
                try:
                    cmds.setAttr("{}.ftn".format(self.mat_color_tex_dict[mat]), suffix_tex_dict[_suffix], type = "string")
                except Exception as e:
                    print(e)



            
    
def main():
    tex_changer = TextureChanger()
    tex_changer.create()