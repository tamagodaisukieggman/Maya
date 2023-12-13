# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from maya import cmds

from PySide2 import QtCore, QtWidgets, QtGui

from shr.cutscene import utility


class DisplayGridDrawer(object):
    """画面にグリッドする機能
    """
    SPLIT_COUNT = 3
    LINE_SIZE = 1

    CROSS_LINE_SIZE = 25

    def __init__(self, view_name, view_qobject):
        self.view_name = view_name
        self.view_qobject = view_qobject

        self.line_list = None
        self.is_grid_on = False

    def toggle(self):
        if not self.is_grid_on:
            self.grid_on()
        else:
            self.grid_off()

    def grid_on(self):
        self.line_list = self.__create_display_grid(self.SPLIT_COUNT, self.LINE_SIZE)

        self.is_grid_on = True

    def grid_off(self):
        self.__delete_lines(self.line_list)
        self.line_list = None

        self.is_grid_on = False

    def __create_display_grid(self, split_count, line_size):
        qsize = self.view_qobject.size()

        focus_camera_name = utility.panel.get_camera_from_model_panel(self.view_name)

        overscan = cmds.getAttr("{}.overscan".format(focus_camera_name))
        # 解像度ゲートがOnだったら
        if cmds.getAttr("{}.displayResolution".format(focus_camera_name)):
            aspect_ratio = cmds.getAttr("defaultResolution.deviceAspectRatio") * overscan
        else:
            # 現状のディスプレイからアスペクト比を作成
            aspect_ratio = qsize.width() / qsize.height() * overscan

        line_list = []

        self.__create_verticalline(self.view_qobject, line_list, aspect_ratio, split_count, line_size, overscan)

        self.__create_horizontalline(self.view_qobject, line_list, aspect_ratio, split_count, line_size, overscan)

        self.__create_crossline(self.view_qobject, line_list, line_size, self.CROSS_LINE_SIZE)

        return line_list

    def __create_line(self, view, line_list, x, y, width, height, line_size, line_type):
        line = QtWidgets.QFrame(view)
        line.setParent(view)
        line.setGeometry(QtCore.QRect(x, y, width, height))
        line.setFrameShape(line_type)
        line.setFrameShadow(QtWidgets.QFrame.Plain)
        line.setObjectName("line")
        line.setLineWidth(line_size)
        # line.setBackgroundRole
        line.setAutoFillBackground(True)
        line.setStyleSheet("QLine {background-color:black; color:black}")

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Base, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        line.setPalette(palette)

        line.show()
        line_list.append(line)

    def __delete_lines(self, line_list):
        if line_list is None:
            return

        for line in line_list:
            # line.close()
            line.setParent(None)
            line.deleteLater()
            del line

    def __create_verticalline(self, target_qobject, insert_line_list, aspect_ratio, split_count, line_size, overscan):
        """縦線を作成する

        :param target_qobject: 描画するＱWidget
        :type target_qobject: QObject
        :param insert_line_list: 作ったラインを追加するリスト
        :type insert_line_list: list
        :param aspect_ratio: アスペクト比
        :type aspect_ratio: float
        :param split_count: 分割数
        :type split_count: int
        :param line_size: 線の太さ
        :type line_size: int
        """
        qsize = target_qobject.size()
        step_width = (qsize.width() / overscan) / float(split_count)

        aspect_height_size = qsize.width() / aspect_ratio

        margin = (qsize.height() - aspect_height_size)
        half_margin = margin / 2

        start_height_point = qsize.height() - aspect_height_size - half_margin
        end_height_point = aspect_height_size

        width_half_margin = (qsize.width() - (qsize.width() / overscan)) / 2

        for i in range(0, split_count + 1):
            x = (step_width * i) + width_half_margin

            if i == split_count:
                x = x - 1

            self.__create_line(self.view_qobject,
                               insert_line_list,
                               x,
                               start_height_point,
                               line_size,
                               end_height_point,
                               line_size,
                               QtWidgets.QFrame.HLine)

    def __create_horizontalline(self, target_qobject, insert_line_list, aspect_ratio, split_count, line_size, overscan):
        """横線を作成する

        :param target_qobject: 描画するＱWidget
        :type target_qobject: QObject
        :param insert_line_list: 作ったラインを追加するリスト
        :type insert_line_list: list
        :param aspect_ratio: アスペクト比
        :type aspect_ratio: float
        :param split_count: 分割数
        :type split_count: int
        :param line_size: 線の太さ
        :type line_size: int
        """

        qsize = target_qobject.size()

        aspect_height_size = qsize.width() / aspect_ratio

        step_height = aspect_height_size / float(split_count)

        margin = (qsize.height() - aspect_height_size)
        half_margin = margin / 2

        width_half_margin = (qsize.width() - (qsize.width() / overscan)) / 2

        for i in range(0, split_count + 1):
            y = (step_height * i) + half_margin
            if i == split_count:
                y = y - 1

            self.__create_line(self.view_qobject,
                               insert_line_list,
                               width_half_margin,
                               y,
                               (qsize.width() / overscan),
                               line_size,
                               line_size,
                               QtWidgets.QFrame.VLine)

    def __create_crossline(self, target_qobject, insert_line_list, line_size, cross_line_size):
        """クロス線を作成する

        :param target_qobject: 描画するＱWidget
        :type target_qobject: QObject
        :param insert_line_list: 作ったラインを追加するリスト
        :type insert_line_list: list
        :param line_size: 線の太さ
        :type line_size: int
        :param cross_line_size: クロス線の長さ
        :type cross_line_size: int
        """
        qsize = target_qobject.size()

        center_point = (qsize.height() / 2, qsize.width() / 2)
        line_length = cross_line_size
        line_length_half = line_length / 2

        self.__create_line(self.view_qobject,
                           insert_line_list,
                           center_point[1] - line_length_half,
                           center_point[0],
                           line_length,
                           line_size,
                           line_size,
                           QtWidgets.QFrame.HLine)

        self.__create_line(self.view_qobject,
                           insert_line_list,
                           center_point[1],
                           center_point[0] - line_length_half,
                           line_size,
                           line_length,
                           line_size,
                           QtWidgets.QFrame.VLine)
