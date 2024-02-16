# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PySide2 import QtCore
# from PySide2 import QtGui
from PySide2 import QtWidgets
from maya.app.general import mayaMixin

from .ui import main_window

# Python3-
try:
    from importlib import reload
    from builtins import range
    from builtins import object
except Exception:
    pass

reload(main_window)


CHECK_BUTTON_LAYOUT_VARTICAL_ITEM_MAX_COUNT = 5


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, parent=None):

        super(View, self).__init__(parent)
        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)

        self.close_event_exec = None

        # cmdsモジュールのフレームレイアウトのような挙動を行うクラス
        # 顔系
        self.facial_target_tool_frame_layout = FrameLayout(self.ui.facial_target_type_tool_frame, self.ui.facial_target_type_tool_frame_btn)
        self.edit_rig_frame_layout = FrameLayout(self.ui.edit_rig_frame, self.ui.edit_rig_frame_btn)
        self.facial_check_frame_layout = FrameLayout(self.ui.facial_check_frame, self.ui.facial_check_frame_btn)
        self.eye_check_frame_layout = FrameLayout(self.ui.eye_check_frame, self.ui.eye_check_frame_btn)
        self.eyebrow_check_frame_layout = FrameLayout(self.ui.eyebrow_check_frame, self.ui.eyebrow_check_frame_btn)
        self.mouth_check_frame_layout = FrameLayout(self.ui.mouth_check_frame, self.ui.mouth_check_frame_btn)
        self.export_facial_target_frame_layout = FrameLayout(self.ui.export_facial_target_frame, self.ui.export_facial_target_frame_btn)
        self.export_facial_blend_target_frame_layout = FrameLayout(self.ui.export_facial_blend_target_frame, self.ui.export_facial_blend_target_frame_btn)
        # 耳系
        self.ear_target_type_tool_frame_layout = FrameLayout(self.ui.ear_target_type_tool_frame, self.ui.ear_target_type_tool_frame_btn)
        self.ear_check_frame_layout = FrameLayout(self.ui.ear_check_frame, self.ui.ear_check_frame_btn)
        self.ear_target_check_frame_layout = FrameLayout(self.ui.ear_target_check_frame, self.ui.ear_target_check_frame_btn)
        self.export_ear_target_frame_layout = FrameLayout(self.ui.export_ear_target_frame, self.ui.export_ear_target_frame_btn)

        # ボタン自動配置の為のレイアウトのlist
        # 顔系
        self.eyebrow_layout_list = [self.ui.eyebrow_check_top_layout, self.ui.eyebrow_check_mid_layout]
        self.eye_layout_list = [self.ui.eye_check_top_layout, self.ui.eye_check_mid_layout]
        self.mouth_layuout_list = [self.ui.mouth_check_top_layout, self.ui.mouth_check_mid_layout]
        self.facial_layout_list = self.eyebrow_layout_list + self.eye_layout_list + self.mouth_layuout_list
        # 耳系
        self.ear_laoyut_list = [self.ui.ear_check_top_layout, self.ui.ear_check_mid_layout]

    def closeEvent(self, event):

        if self.close_event_exec is not None:
            self.close_event_exec()

        self.deleteLater()
        super(View, self).closeEvent(event)

    def reset_facial_check_button(self):

        self.__reset_check_button(self.facial_layout_list)

    def reset_ear_check_button(self):

        self.__reset_check_button(self.ear_laoyut_list)

    def __reset_check_button(self, layout_list):

        for layout in layout_list:

            for i in range(layout.count()):

                # 子供のLayout検索
                child_layout = layout.itemAt(i).layout()
                if child_layout is None:
                    continue

                # 子供のLayoutの中身をまず削除
                for j in range(child_layout.count()):
                    w = child_layout.itemAt(j).widget()
                    if w:
                        w.deleteLater()

                # layout削除
                layout.itemAt(i).layout().deleteLater()

    def create_check_button_layout(self, parent, button_info_list, func, *args):

        layout = CheckButtonLayout(button_info_list, func, *args)
        parent.addLayout(layout)


class CheckButton(QtWidgets.QPushButton):

    def __init__(self, target_info_item=None, func=None, *args):

        super(CheckButton, self).__init__()

        label = target_info_item.label if target_info_item.label is not None else ''
        frame = target_info_item.frame if target_info_item.frame is not None else ''
        self.setText('{} ({})'.format(label, frame))

        args = [target_info_item] + list(args)
        if func:
            self.clicked.connect(lambda: func(*args))


class CheckButtonLayout(QtWidgets.QHBoxLayout):

    def __init__(self, button_info_list=[], func=None, *args):

        super(CheckButtonLayout, self).__init__()
        self.setSpacing(0)

        if button_info_list:
            for button_info in button_info_list:
                self.add_button(button_info, func, *args)
            self.set_stretch()

    def add_button(self, button_info, func, *args):

        if self.count() >= CHECK_BUTTON_LAYOUT_VARTICAL_ITEM_MAX_COUNT:
            return False

        button = CheckButton(button_info, func, *args)
        self.addWidget(button)

        return True

    def set_stretch(self):

        spacer_stretch_count = (CHECK_BUTTON_LAYOUT_VARTICAL_ITEM_MAX_COUNT) - self.count()
        add_specer = False

        # 横に並んでいるボタンの数が規定数以下ならばスペーサーを挟む
        if spacer_stretch_count >= 1:
            spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.addItem(spacer)
            add_specer = True

        for i in range(self.count()):
            if add_specer and i == self.count() - 1:
                self.setStretch(i, spacer_stretch_count)
            else:
                self.setStretch(i, 1)


class FrameLayout(object):

    def __init__(self, frame, button, button_color='#343434'):

        self.frame = frame
        self.button = button
        self.collapse = False

        self.button.clicked.connect(lambda: self.frame_layout_event())
        self.button.setStyleSheet('background-color: {}'.format(button_color))

    def frame_layout_event(self):

        self.collapse = not self.collapse
        self.frame.setHidden(self.collapse)

        if self.collapse:
            self.button.setArrowType(QtCore.Qt.RightArrow)
        else:
            self.button.setArrowType(QtCore.Qt.DownArrow)
