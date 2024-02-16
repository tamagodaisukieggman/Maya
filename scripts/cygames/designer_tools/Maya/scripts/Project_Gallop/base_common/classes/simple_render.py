# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
except Exception:
    pass


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SimpleRender(object):

    # ===============================================
    def __init__(self):

        self.render_item_list = None

        # itemで何も指定されていない場合に使用
        self.base_file_name = None
        self.base_output_dir_path = None
        self.base_camera = None

    # ===============================================
    def add_item(
        self,
        output_dir_path=None,
        file_name=None,
        camera=None,
        start_frame=None,
        end_frame=None,
        by_frame=None,
    ):

        if self.render_item_list is None:
            self.render_item_list = []

        arg_dict = {}

        if start_frame is not None:
            arg_dict['start_frame'] = start_frame

        if end_frame is not None:
            arg_dict['end_frame'] = end_frame

        if by_frame is not None:
            arg_dict['by_frame'] = by_frame

        if output_dir_path:
            arg_dict['output_dir_path'] = output_dir_path

        if file_name:
            arg_dict['file_name'] = file_name

        if camera:
            arg_dict['camera'] = camera

        this_item = SimpleRenderItem(self)
        this_item.create(**arg_dict)

        if this_item.is_ready:
            self.render_item_list.append(this_item)
            return this_item

    # ===============================================
    def set_base_file_name(self, file_name):

        if not file_name:
            return

        self.base_file_name = file_name

    # ===============================================
    def set_base_output_dir(self, output_dir_path):

        if not output_dir_path:
            return

        self.base_output_dir_path = output_dir_path

    # ===============================================
    def set_base_camera(self, camera):

        if not camera:
            return

        self.base_camera = camera

    # ===============================================
    def render(self):

        if not self.render_item_list:
            return

        # アイテムを回してレンダリング
        for item in self.render_item_list:

            item.render()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SimpleRenderItem(object):
    """
    １レンダリングごとの設定
    """

    # ===============================================
    def __init__(self, parent):

        self.parent = parent

        self.output_dir_path = None
        self.file_name = None
        self.camera = None

        self.fixed_output_dir_path = None
        self.fixed_file_name = None
        self.fixed_camera = None

        self.start_frame = None
        self.end_frame = None
        self.by_frame = None

        self.is_multi_frame = False

        self.padding_length = 4

        self.is_ready = False

    # ===============================================
    def create(
        self,
        output_dir_path=None,
        file_name=None,
        camera=None,
        start_frame=None,
        end_frame=None,
        by_frame=1
    ):

        self.is_ready = False

        self.set_start_frame(start_frame)
        self.set_end_frame(end_frame)
        self.set_by_frame(by_frame)
        self.set_output_dir(output_dir_path)
        self.set_file_name(file_name)
        self.set_camera(camera)

        self.is_ready = True

    # ===============================================
    def render(self):

        if not self.is_ready:
            return

        # 出力パスとカメラを確定
        self.__set_fixed_output_dir_path()
        self.__set_fixed_file_name()
        self.__set_fixed_camera()

        if self.fixed_output_dir_path and not os.path.isdir(self.fixed_output_dir_path):
            os.makedirs(self.fixed_output_dir_path)

        # レンダリング設定に値を代入
        cmds.setAttr('defaultRenderGlobals.imageFilePrefix',
                     self.fixed_output_dir_path + '/simple_render_tmp', type='string')
        self.__set_multi_frame_setting()
        this_camera = self.__set_renderable_camera_setting()

        # 引数の辞書を作成
        arg_dict = {}

        if this_camera:
            arg_dict[str('camera')] = this_camera

        if not self.is_multi_frame:

            if self.start_frame is not None:
                arg_dict[str('frame')] = self.start_frame

            else:
                arg_dict[str('currentFrame')] = True

            result_image_path = cmds.ogsRender(**arg_dict)
            self.__check_render_image_path(result_image_path)

        else:
            frame_list = list(range(self.start_frame, self.end_frame + self.by_frame, self.by_frame))
            for frame in frame_list:
                arg_dict[str('frame')] = frame
                result_image_path = cmds.ogsRender(**arg_dict)
                self.__check_render_image_path(result_image_path)

    # ===============================================
    def __set_fixed_output_dir_path(self):

        if self.output_dir_path:
            self.fixed_output_dir_path = self.output_dir_path

        else:
            if self.parent.base_output_dir_path:
                self.fixed_output_dir_path = self.parent.base_output_dir_path

    # ===============================================
    def __set_fixed_file_name(self):

        if self.file_name:
            self.fixed_file_name = self.file_name

        else:
            if self.parent.base_file_name:
                self.fixed_file_name = self.parent.base_file_name

    # ===============================================
    def __set_fixed_camera(self):

        if self.camera:
            self.fixed_camera = self.camera

        else:
            if self.parent.base_camera:
                self.fixed_camera = self.parent.base_camera

    # ===============================================
    def __set_multi_frame_setting(self):

        # multiFrame指定
        cmds.setAttr('defaultRenderGlobals.animation', self.is_multi_frame)

        if self.is_multi_frame:

            # 範囲指定
            cmds.setAttr('defaultRenderGlobals.startFrame', int(self.start_frame))
            cmds.setAttr('defaultRenderGlobals.endFrame', int(self.end_frame))
            cmds.setAttr('defaultRenderGlobals.byFrameStep', int(self.by_frame))

            # 接尾語指定
            cmds.setAttr('defaultRenderGlobals.putFrameBeforeExt', True)
            cmds.setAttr('defaultRenderGlobals.extensionPadding', self.padding_length)

    # ===============================================
    def __set_renderable_camera_setting(self):

        this_camera = None

        if self.camera:
            this_camera = self.camera

        elif self.parent.base_camera:
            this_camera = self.parent.base_camera

        if not this_camera:
            return

        cam_list = cmds.ls(typ='camera')

        for cam in cam_list:

            if cam is this_camera:
                cmds.setAttr(cam + '.renderable', True)

        return this_camera

    # ===============================================
    def __check_render_image_path(self, result_image_path):
        """
        cmds.ogsRenderでレンダリングされた画像が意図したファイル名で保存され、
        且つtmpファイルが残らないようにする。
        元々はogsRenderでレンダリングすると「_tmp」suffixが付く時と付かない時があるのでその対策で作られたっぽい。
        ogsRenderはdefaultRenderGlobals.imageFilePrefixのパスで書き出すが、Maya2022だと
        日本語のファイル名（例：【 フェイスタイプ一覧 chr1011_00 】）だと出力ファイルが文字化けする。
        (戻り値は文字化けしないので不整合が出る) のでここでリネームする。
        Args:
            result_image_path (str): cmds.ogsRenderの戻り値のパス
        """
        if not os.path.isfile(result_image_path):
            cmds.warning('レンダリング済みの画像が見つかりません: ' + str(result_image_path))
            return

        file_extension = os.path.splitext(result_image_path)[1]

        if self.is_multi_frame:
            current_frame = int(cmds.currentTime(q=True))
            frame_str = format(str(current_frame), '0>{}'.format(self.padding_length))
            intended_file_path = self.fixed_output_dir_path + '/' + \
                self.fixed_file_name + '.' + frame_str + file_extension
        else:
            intended_file_path = self.fixed_output_dir_path + \
                '/' + self.fixed_file_name + file_extension

        if not result_image_path == intended_file_path:
            # 既存のファイルがあるとrenameできないので破棄
            if os.path.isfile(intended_file_path):
                os.remove(intended_file_path)
            if os.path.isfile(result_image_path):
                os.rename(result_image_path, intended_file_path)

    # ===============================================
    def set_output_dir(self, output_dir_path):

        if not output_dir_path:
            return

        self.output_dir_path = output_dir_path

    # ===============================================
    def set_file_name(self, file_name):

        if not file_name:
            return

        self.file_name = file_name

    # ===============================================
    def set_start_frame(self, frame):

        self.is_multi_frame = False

        if frame is None:
            return

        self.start_frame = frame

        self.__check_is_multi_frame()

    # ===============================================
    def set_end_frame(self, frame):

        self.is_multi_frame = False

        if frame is None:
            return

        self.end_frame = frame

        self.__check_is_multi_frame()

    # ===============================================
    def set_by_frame(self, frame):

        if frame is None:
            return

        self.by_frame = frame

    # ===============================================
    def set_camera(self, camera):

        if not camera:
            return

        self.camera = camera

    # ===============================================
    def set_padding_length(self, length):

        if not length:
            return

        self.padding_length = int(length)

    # ===============================================
    def __check_is_multi_frame(self):

        if not self.start_frame or not self.end_frame:
            self.is_multi_frame = False
            return

        if self.start_frame < self.end_frame:
            self.is_multi_frame = True
            return

        self.is_multi_frame = False
