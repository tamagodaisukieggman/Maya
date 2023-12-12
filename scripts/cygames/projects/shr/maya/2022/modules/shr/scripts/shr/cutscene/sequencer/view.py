# -*- coding: utf-8 -*-
"""シーケンサーのView
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide6 import QtCore, QtGui, QtWidgets

from .api import *

if TYPE_CHECKING:
    from .controller import SequencerController


class MainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):

    closed = QtCore.Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setObjectName("MainWindow")
        self.setWindowTitle("ed.timeline Example - How to use ed.timeline")
        # self.resize(800, 600)

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("centralwidget")
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setObjectName("mainLayout")

        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setObjectName("verticalLayout")

        self.camera_add_button = QtWidgets.QPushButton(self.central_widget)
        self.camera_add_button.setText(QtCore.QCoreApplication.translate("MainWindow", "Camera追加", None))

        self.actor_add_button = QtWidgets.QPushButton(self.central_widget)
        self.actor_add_button.setText(QtCore.QCoreApplication.translate("MainWindow", "Actor追加", None))

        self.line = QtWidgets.QFrame(self.central_widget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.anim_add_button = QtWidgets.QPushButton(self.central_widget)
        self.anim_add_button.setText(QtCore.QCoreApplication.translate("MainWindow", "Clip追加", None))

        self.line_2 = QtWidgets.QFrame(self.central_widget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.actor_only_enable_button = QtWidgets.QPushButton(self.central_widget)
        self.actor_only_enable_button.setText(QtCore.QCoreApplication.translate("MainWindow", "通常表示", None))

        self.show_only_selected_clip_node_button = QtWidgets.QPushButton(self.central_widget)
        self.show_only_selected_clip_node_button.setText(QtCore.QCoreApplication.translate("MainWindow", "選択クリップ表示", None))

        self.timeline_view = SequencerTimelineView()

        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.addWidget(self.camera_add_button)
        self.horizontal_layout.addWidget(self.actor_add_button)
        self.horizontal_layout.addWidget(self.line)
        self.horizontal_layout.addWidget(self.anim_add_button)
        self.horizontal_layout.addWidget(self.line_2)
        self.horizontal_layout.addWidget(self.actor_only_enable_button)
        self.horizontal_layout.addWidget(self.show_only_selected_clip_node_button)

        self.vertical_layout.addLayout(self.horizontal_layout)
        self.vertical_layout.addWidget(self.timeline_view)

        self.main_layout.addLayout(self.vertical_layout)

        self.setCentralWidget(self.central_widget)
        # self.addDockWidget(QtCore.Qt.TopDockWidgetArea, DockWidget(parent=self))

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.closed.emit()
        return super().closeEvent(event)

    def init_menu_ui(self):
        """メニューに登録する関数"""
        file_menu = {
            "new": self.seq_ctrl.clear_model,
            "load": self.seq_ctrl.load,
            "save": self.seq_ctrl.save,
        }
        create_menu = {
            "add camera actor": self.seq_ctrl.create_camera_actor,
            "add actor": self.seq_ctrl.show_create_actor,
            "add motion": self.seq_ctrl.show_insert_clip,
            "add camera_actor": self.seq_ctrl.create_camera_actor
        }
        edit_menu = {
            "add sub track": self.seq_ctrl.add_sub_track,
            "0": "separator",
            "save clip": self.seq_ctrl.save_selected_clip_reference,
            "save all clips": self.seq_ctrl.save_all_reference,
            "1": "separator",
            "remove selected track": self.seq_ctrl.remove_selected_track_item,
            "remove selected clip": self.seq_ctrl.remove_selected_sequencer_clip,
        }
        view_menu = {
            "outliner": self.seq_ctrl.show_outline,
            "default view": self.seq_ctrl.show_default,
            "focus view": self.seq_ctrl.show_only_selected_clip_node
        }
        debug_menu = {
            "add empty track": self.seq_ctrl.add_empty_motion_track,
            "add empty sound track": self.seq_ctrl.add_empty_sound_track,
            "add empty clip to selected track": self.seq_ctrl.add_empty_clip_to_selected_track,
            "0": "separator",
            "print selected track data": self.seq_ctrl.print_selected_track,
            "print selected track item": self.seq_ctrl.print_selected_item,
            "print selected clips": self.seq_ctrl.print_selected_clips,
            "print selected clip property": self.seq_ctrl.print_selected_clip_property,
            "1": "separator",
            "set nothing on selected clip": self.seq_ctrl.set_nothing_on_selected_clip,
            "set check on selected clip": self.seq_ctrl.set_check_on_selected_clip,
            "set disable on selected clip": self.seq_ctrl.set_disable_on_selected_clip,
            "set edit on selected clip": self.seq_ctrl.set_edit_on_selected_clip,
            "2": "separator",
            "add track property": self.seq_ctrl.add_track_property,
            "print selected track's property": self.seq_ctrl.print_selected_track_property,
            "3": "separator",
            "rebuild": self.seq_ctrl.rebuild,
            "test": self.seq_ctrl.test,
            "delete all mseq": self.seq_ctrl.delete_all_mseq
        }
        # actor
        menu_all = {
            "File": file_menu,
            "Create": create_menu,
            "Edit": edit_menu,
            "View": view_menu,
            "Debug": debug_menu
        }
        self.setup_menu(menu_all)

    def setup_menu(self, all_menu):
        menu_bar = self.menuBar()

        for menu_name, menu_dict_ in all_menu.items():
            menu = menu_bar.addMenu(menu_name)

            for name, func in menu_dict_.items():
                if func == "separator":
                    menu.addSeparator()
                else:
                    action = QtWidgets.QAction(QtGui.QIcon(), name, self)
                    action.triggered.connect(func)
                    menu.addAction(action)

    def set_sequencer_ctrl(self, ctrl: SequencerController):
        self.seq_ctrl = ctrl
