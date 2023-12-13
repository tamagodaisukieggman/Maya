# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import shiboken2

import os

import maya.cmds as cmds


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BlendImageByQt(object):

    # ==================================================
    def __init__(self):

        self.resolution = None

        self.base_image = None
        self.blend_image_list = []

        self.blend_mode = QPainter.CompositionMode_SourceOver

    # ==================================================
    def set_all_image(self, path_list):
        """ブレンドするイメージをセット

        インデックス0をベースイメージにセット
        """

        if not path_list:
            return False

        base_path = path_list.pop(0)
        blend_path_list = path_list

        base_result = self.set_base_image(base_path)
        blend_result = self.set_image_list(blend_path_list)

        if base_result and blend_result:
            return True
        else:
            return False

    # ==================================================
    def set_base_image(self, path):

        tmp_image_list = self.__load_image([path])

        if not tmp_image_list:
            return False

        self.base_image = tmp_image_list[0]
        return True

    # ==================================================
    def set_image_list(self, path_list):

        tmp_image_list = self.__load_image(path_list)

        if not tmp_image_list:
            return False

        self.blend_image_list = tmp_image_list
        return True

    # ==================================================
    def __load_image(self, path_list):

        result_image_list = []

        for path in path_list:

            if not os.path.exists(path):
                continue

            image = QImage()
            load_result = image.load(path)

            if load_result:
                result_image_list.append(image)

        return result_image_list

    # ==================================================
    def set_blend_mode(self, blend_type):

        if blend_type == 'plus':
            self.blend_mode = QPainter.CompositionMode_Plus

        elif blend_type == 'multiply':
            self.blend_mode = QPainter.CompositionMode_Multiply

        elif blend_type == 'screen':
            self.blend_mode = QPainter.CompositionMode_Screen

        elif blend_type == 'overlay':
            self.blend_mode = QPainter.CompositionMode_Overlay

        elif blend_type == 'darken':
            self.blend_mode = QPainter.CompositionMode_Darken

        elif blend_type == 'lighten':
            self.blend_mode = QPainter.CompositionMode_Lighten

        else:
            self.blend_mode = QPainter.CompositionMode_SourceOver

    # ==================================================
    def set_resolution(self, res_x_y):

        if not res_x_y or not len(res_x_y) == 2:
            return

        self.resolution = [int(res_x_y[0]), int(res_x_y[1])]

    # ==================================================
    def blend(self, output_path):

        if not self.base_image or not output_path:
            return

        # 解像度指定がない場合はベース解像度を使用
        if not self.resolution:
            self.resolution = [self.base_image.width(), self.base_image.height()]

        # 出力イメージ用のインスタンスを準備
        result_image = QImage(self.resolution[0], self.resolution[1], QImage.Format_ARGB32_Premultiplied)
        result_painter = QPainter(result_image)
        result_painter.fillRect(result_image.rect(), Qt.transparent)

        # ベースイメージで塗りつぶし
        result_painter.setCompositionMode(QPainter.CompositionMode_DestinationOver)
        tmp_image = self.base_image.smoothScaled(self.resolution[0], self.resolution[1])
        result_painter.drawImage(0, 0, tmp_image)

        # 以降はブレンドモードを適用
        result_painter.setCompositionMode(self.blend_mode)

        # 各イメージをブレンド
        for image in self.blend_image_list:
            tmp_image = image.smoothScaled(self.resolution[0], self.resolution[1])
            result_painter.drawImage(0, 0, tmp_image)

        result_painter.end()
        result = result_image.save(output_path)

        if result:
            return output_path
