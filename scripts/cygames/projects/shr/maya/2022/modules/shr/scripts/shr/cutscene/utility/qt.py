# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import os
from functools import partial

from maya import OpenMayaUI, utils, cmds
from shiboken2 import wrapInstance
from PySide2 import QtWidgets
from PySide2.QtCore import QSettings, QObject, QTimer, QEvent
from PySide2.QtWidgets import QLineEdit, QCheckBox, QComboBox, QSpinBox, QListWidget

from tatool import config


def convert_qwidget_from_modeleditor(name):
    """モデルエディターをQWidgetに変換する

    :param name: modeleditr名
    :type name: str
    :return: qwidget
    :rtype: PySide2.WtWidgets.QWidget
    """
    view = None
    view = OpenMayaUI.M3dView()

    view.getM3dViewFromModelPanel(name, view)
    view_widget = wrapInstance(int(view.widget()), QtWidgets.QWidget)

    return view_widget


def convert_qwidget_from_panel(name):
    target_panel = OpenMayaUI.MQtUtil.findControl(name)
    if not target_panel:
        return

    target_panel_qobject = wrapInstance(int(target_panel), QtWidgets.QWidget)
    return target_panel_qobject


class QtSettings(object):
    def __init__(self, tool_name, config_name="settings"):
        self.config_name = config_name + ".ini"

        self.tool_setting = QSettings(self.__create_tool_path(tool_name), QSettings.IniFormat)
        self.tool_setting.setIniCodec("utf-8")

    def save_settings(self, saved_widgets):
        """セーブする

        :param saved_widgets: セーブしたいWidgetsのリスト
        :type saved_widgets: List
        """
        for saved_widget in saved_widgets:
            self.__save_widgets_object_value(saved_widget)

    def save_geometry(self, widget_object):
        """ウィンドウサイズをセーブする
        """
        self.tool_setting.setValue("ui_geometry", widget_object.saveGeometry())

    def load_settings(self, loaded_widgets):
        """ロードする

        :param loaded_widgets: ロードしたいWidgetsのリスト
        :type loaded_widgets: List
        """
        for loaded_widget in loaded_widgets:
            self.__load_widgets_object_value(loaded_widget)

    def load_geometry(self, widget_object):
        """ウィンドウサイズをロードする
        """
        widget_object.restoreGeometry(self.tool_setting.value("ui_geometry"))

    def __load_widgets_object_value(self, view_object):
        if self.tool_setting.value(view_object.objectName()) is not None:
            if type(view_object) == QLineEdit:
                view_object.setText(self.tool_setting.value(view_object.objectName()))

            elif type(view_object) == QCheckBox:
                view_object.setChecked(bool(self.tool_setting.value(view_object.objectName())))

            elif type(view_object) == QComboBox:
                view_object.setCurrentIndex(int(self.tool_setting.value(view_object.objectName())))

            elif type(view_object) == QSpinBox:
                view_object.setValue(int(self.tool_setting.value(view_object.objectName())))

            # elif type(view_object) == QListWidget:
            #     list_count = view_object.count

            #     for count in range(0, list_count):
            #         view_object.item
            #     view_object.setValue((self.tool_setting.value(view_object.objectName())))
            else:
                raise QtSettingsNoSupportTypeError("No Support Type.. [ {} ]".format(type(view_object)))

    def __save_widgets_object_value(self, view_object):
        if type(view_object) == QLineEdit:
            self.tool_setting.setValue(view_object.objectName(), view_object.text())

        elif type(view_object) == QCheckBox:
            self.tool_setting.setValue(view_object.objectName(), view_object.isChecked())

        elif type(view_object) == QComboBox:
            self.tool_setting.setValue(view_object.objectName(), view_object.currentIndex())

        elif type(view_object) == QSpinBox:
            self.tool_setting.setValue(view_object.objectName(), view_object.value())

        elif type(view_object) == QListWidget:
            list_count = view_object.count()
            for count in range(0, list_count):
                self.tool_setting.setValue(view_object.objectName(), view_object.item(count))

        else:
            raise QtSettingsNoSupportTypeError("No Support Type.. [ {} ]".format(type(view_object)))

    def __create_tool_path(self, tool_name):
        too_settings_folder_path = config.get_config_path(tool_name)

        ui_settings_path = os.path.join(too_settings_folder_path, self.config_name)

        return ui_settings_path

    def load_in_dict(self, loaded_widgets):
        """辞書でロードする

        存在しない設定だとwidgetsのデフォルト値を利用。

        :return: 設定
        :rtype: dict
        """
        result_data = dict()

        for loaded_widget in loaded_widgets:
            self.__add_to_dict_if_it_exists(result_data, loaded_widget)

        return result_data

    def __add_to_dict_if_it_exists(self, insert_dict, view_object):
        insert_dict[view_object.objectName()] = self.__get_the_value_if_it_exists(view_object)

    def __get_the_value_if_it_exists(self, view_object):
        if type(view_object) == QLineEdit:
            return self.tool_setting.value(view_object.objectName(), view_object.text())

        elif type(view_object) == QCheckBox:
            return bool(self.tool_setting.value(view_object.objectName(), view_object.isChecked()))

        elif type(view_object) == QComboBox:
            return int(self.tool_setting.value(view_object.objectName(), view_object.currentIndex()))

        elif type(view_object) == QSpinBox:
            return int(self.tool_setting.value(view_object.objectName(), view_object.value()))


class QtSettingsNoSupportTypeError(Exception):
    """QtSettingsのサポート外タイプエラー"""
    pass


class PanelInMouseLoopEventCallbackRegister(object):
    """パネルの上のマウス移動イベントに関数登録する機能

    """

    def __init__(self, panel_name, loop_callback, once_callback=None, interval_millsecond=25):
        self.panel_name = panel_name
        self.interval_millsecond = interval_millsecond
        self.event_filter = PanelInMouseLoopEventFilter(loop_callback, once_callback, self.interval_millsecond)

        self.camera_sequencer_widgets = None

    def set_event(self):
        qobject = convert_qwidget_from_panel(self.panel_name)
        if not qobject:
            return

        self.camera_sequencer_widgets = qobject
        self.camera_sequencer_widgets.installEventFilter(self.event_filter)

    def remove_event(self):
        qobject = convert_qwidget_from_panel(self.panel_name)
        if not qobject:
            self.camera_sequencer_widgets = None

        if self.camera_sequencer_widgets:
            self.camera_sequencer_widgets.removeEventFilter(self.event_filter)


class PanelInMouseLoopEventFilter(QObject):
    """QtEventFilter

    指定間隔でMouseがPanel内にある時に定期実行
    """

    def __init__(self, loop_call_back, once_call_back=None, interval_millsecond=50):
        super(PanelInMouseLoopEventFilter, self).__init__()
        self.__loop_timer = QTimer()

        self.__loop_timer.timeout.connect(partial(self.collect_call_back, loop_call_back))

        self.__once_timer = QTimer()
        self.__once_timer.timeout.connect(partial(self.collect_call_back, once_call_back))

        self.__interval_millsecond = interval_millsecond

    def collect_call_back(self, call_backs):
        if not call_backs:
            return

        if cmds.play(query=True, state=True):
            return

        if type(call_backs) == list:
            for call_back in call_backs:
                call_back()
        else:
            call_backs()

    def eventFilter(self, widget, event):
        if event.type() == QEvent.Enter:
            # 重たいので、指定ミリ秒操作がなかったらリフレッシュさせる
            self.__loop_timer.start(self.__interval_millsecond)
            self.__loop_timer.setSingleShot(False)

            self.__once_timer.start(self.__interval_millsecond)
            self.__once_timer.setSingleShot(True)

        if event.type() == QEvent.Leave:
            self.__loop_timer.stop()
            self.__loop_timer.setSingleShot(True)

        return False
