# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance

import codecs
from collections import OrderedDict
import csv
import fnmatch
from functools import partial
import glob
import io
import json
import re
import os
import sys
from timeit import default_timer as timer
import time
import traceback

from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui
import maya.api.OpenMaya as om2

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQWidgetDockableMixin

WINDOW_TITLE = 'Status Checker'
WINDOW_OPTIONVAR = 'Status_Checker'

class StatusChecker(MayaQWidgetDockableMixin, QMainWindow):
    # QMainWindowを継承するとmenubarの使える幅が広い
    def __init__(self, *args, **kwargs):
        super(StatusChecker, self).__init__(*args, **kwargs)

        self.project = None
        self.icons_path = '{}/{}'.format('/'.join(__file__.replace('\\', '/').split('/')[0:-1]), 'icons')

        self.ui_values = OrderedDict()
        self.status_name_list = []
        self.progress_cbx_list = OrderedDict()
        self.temp_directory = '{}_{}.txt'.format(os.getenv('TEMP').replace('\\', '/'), WINDOW_OPTIONVAR)

        self.assets = OrderedDict()
        self.assets_sections = OrderedDict()
        self.assets_search = OrderedDict()
        self.expire_date_search = OrderedDict()
        self.status_search = OrderedDict()
        self.progress_search = OrderedDict()
        self.show_wids = []
        self.hide_wids = []
        self.cur_assets = OrderedDict()
        self.fileName = None

        self.data_path = None
        self.config_file = None
        self.config = None
        self.expire_limit = None
        self.expire_date = None
        # self.cur_assets_dict = OrderedDict()

        self.start_sort_date = OrderedDict()
        self.end_sort_date = OrderedDict()

        self.sort_types = ['Name:Ascending', 'Name:Descending',
                           'Priority:Ascending', 'Priority:Descending',
                           'Start Date:Ascending', 'Start Date:Descending',
                           'End Date:Ascending', 'End Date:Descending']

        self.showhide_check_types = ['All Show', 'Hide:Unchecked', 'Hide:Checked']


        self.expire_limit_colors = None
        self.today_qdate = QDate.currentDate()

        self.setWindowTitle(WINDOW_TITLE)


    def layout(self):
        self.setGeometry(10, 10, 1080, 900) # (left, top, width, height)
        self.top_wid = QWidget()
        self.setCentralWidget(self.top_wid)

        self.top_qvbl = QVBoxLayout()
        self.top_wid.setLayout(self.top_qvbl)
        # self.top_qvbl.addStretch(True)

        # Auto Save
        self.auto_save_qcbx = QCheckBox('Auto Save')
        # self.auto_save_qcbx.stateChanged.connect(self.search_functions)
        self.top_qvbl.addWidget(self.auto_save_qcbx)

        # Search Assets
        self.search_assets_qhbl = QHBoxLayout()
        self.top_qvbl.addLayout(self.search_assets_qhbl)
        self.search_assets_qhbl.addWidget(QLabel('Search Assets'))

        self.search_assets_le = QLineEdit()
        self.search_assets_qhbl.addWidget(self.search_assets_le)
        self.search_assets_le.textChanged.connect(self.search_functions)

        # Search Status
        self.search_status_qhbl = QHBoxLayout()
        self.top_qvbl.addLayout(self.search_status_qhbl)
        self.search_status_qhbl.addWidget(QLabel('Search Status'))

        self.search_status_le = QLineEdit()
        self.search_status_qhbl.addWidget(self.search_status_le)
        self.search_status_le.textChanged.connect(self.search_functions)

        # Search progress
        self.search_progress_qhbl = QHBoxLayout()
        self.top_qvbl.addLayout(self.search_progress_qhbl)
        self.search_progress_qhbl.addWidget(QLabel('Search Progress'))

        self.search_progress_le = QLineEdit()
        self.search_progress_qhbl.addWidget(self.search_progress_le)
        self.search_progress_le.textChanged.connect(self.search_progress)

        # Calender
        # self.calender_lay = QHBoxLayout()
        # self.top_qvbl.addLayout(self.calender_lay)
        #
        # self.calendar_wid = QCalendarWidget()
        # self.calendar_wid.setFirstDayOfWeek(Qt.Monday)
        # self.calendar_wid.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        # self.calendar_wid.setSelectedDate(QDate.currentDate())
        #
        # self.calender_lay.addWidget(self.calendar_wid)
        #
        # self.calender_func_lay = QVBoxLayout()
        # self.calender_lay.addLayout(self.calender_func_lay)
        #
        # today_btn = QPushButton('Today')
        # self.calender_func_lay.addWidget(today_btn)
        # today_btn.clicked.connect(self.set_currentDate)

        # Search dateEdit
        self.search_dateEdit_lay = QHBoxLayout()
        self.search_dateEdit_lay.setAlignment(Qt.AlignLeft)
        self.top_qvbl.addLayout(self.search_dateEdit_lay)

        self.search_dateEdit_switch_cb = QCheckBox('Search Expire Date')
        self.search_dateEdit_switch_cb.stateChanged.connect(self.search_functions)
        self.search_dateEdit_lay.addWidget(self.search_dateEdit_switch_cb)

        now = QDate.currentDate()
        self.search_start_dateEdit = QDateEdit(self)
        self.search_start_dateEdit.setDate(now.addDays(-20))
        self.search_start_dateEdit.setCalendarPopup(True)
        self.search_start_dateEdit.dateChanged.connect(self.search_functions)
        self.search_dateEdit_lay.addWidget(self.search_start_dateEdit)

        self.search_dateEdit_lay.addWidget(QLabel('~'))

        self.search_end_dateEdit = QDateEdit(self)
        self.search_end_dateEdit.setDate(now.addDays(20))
        self.search_end_dateEdit.setCalendarPopup(True)
        self.search_end_dateEdit.dateChanged.connect(self.search_functions)
        self.search_dateEdit_lay.addWidget(self.search_end_dateEdit)

        self.search_dateEdit_lay.addWidget(QLabel('Sort Order:'))

        self.sort_qcbx = QComboBox()
        self.sort_qcbx.addItems(self.sort_types)
        self.sort_qcbx.currentIndexChanged.connect(self.sort_wid)
        self.search_dateEdit_lay.addWidget(self.sort_qcbx)

        self.search_dateEdit_lay.addWidget(QLabel('Show Hide Checked:'))

        self.showhide_checked_qcbx = QComboBox()
        self.showhide_checked_qcbx.addItems(self.showhide_check_types)
        self.showhide_checked_qcbx.currentIndexChanged.connect(self.showhide_checked)
        self.search_dateEdit_lay.addWidget(self.showhide_checked_qcbx)

        self.refresh_btn = QPushButton('', self)
        self.refresh_btn.clicked.connect(self.refresh_UI)
        self.refresh_btn.setIcon(QIcon('{}/refresh.png'.format(self.icons_path)))
        self.search_dateEdit_lay.addWidget(self.refresh_btn)

        #
        # layout = QGridLayout()
        # layout.addWidget(self.dateEdit)
        # layout.addWidget(self.lbl)
        # # self.setLayout(layout)
        # self.top_qvbl.addLayout(layout)

        # Status List
        self.main_widget = QScrollArea()
        self.top_qvbl.addWidget(self.main_widget)
        # self.setCentralWidget(self.main_widget)
        self.main_widget.setWidgetResizable(True)

        # QWidgetをひとつ挟む
        inner = QWidget()
        self.status_qhbl = QVBoxLayout(inner)
        self.status_qhbl.setAlignment(Qt.AlignTop)
        inner.setLayout(self.status_qhbl)
        self.main_widget.setWidget(inner)

    def set_currentDate(self):
        self.calendar_wid.setSelectedDate(QDate.currentDate())

    def widgets(self):
        try:
            self.remove_assets_sections()
        except:
            pass

        self.sorted_assets = self.config['assets']
        # if file_encoding == 'shift-jis':
        #     self.sorted_assets = [asset.encode('shift-jis') for asset in self.sorted_assets]

        self.sorted_assets.sort()

        try:
            self.update_priority()

            self.sorted_assets = []
            for m in self.priority_sort_assets.keys():
                self.sorted_assets.append(m)

        except:
            pass

        self.cur_checkBox_wids = OrderedDict()
        self.cur_priority_wids = OrderedDict()
        self.cur_expire_date_wids = OrderedDict()

        for asset in self.sorted_assets:
            self.assets[asset] = OrderedDict()

            if not asset in self.config['exclude']:
                self.build_statusBox(asset)

        # Set current
        self.start_sort_date = OrderedDict()
        self.end_sort_date = OrderedDict()
        for asset in self.sorted_assets:
            try:
                self.cur_assets[asset]['checkBox'].setChecked(self.cur_assets_dict[asset]['checkBox'])
            except:
                pass

            try:
                self.cur_assets[asset]['priority'].setCurrentText(self.cur_assets_dict[asset]['priority'])
            except:
                pass

            try:
                self.cur_assets[asset]['description'][1].setPlainText(self.cur_assets_dict[asset]['description'])
            except:
                pass

            try:
                self.expire_date = self.cur_assets_dict[asset]['expire_date']
                start_dateEdit, end_dateEdit = self.cur_assets[asset]['expire_date']

                start_dateEdit.setDate(QDate(*self.expire_date[0]))
                end_dateEdit.setDate(QDate(*self.expire_date[1]))

                self.start_sort_date[asset] = QDate(*self.expire_date[0])
                self.end_sort_date[asset] = QDate(*self.expire_date[1])
            except:
                pass

        for asset in self.sorted_assets:
            self.cur_checkBox_wids[asset].stateChanged.connect(self.save_current)
            self.cur_priority_wids[asset].currentIndexChanged.connect(self.save_current)

            start_dateEdit, end_dateEdit = self.cur_expire_date_wids[asset]
            start_dateEdit.dateChanged.connect(self.save_current)
            end_dateEdit.dateChanged.connect(self.save_current)
            self.change_expire_days_color(end_dateEdit)

        # auto complete
        self.completer = QCompleter(self)
        self.completer.setModel(QStringListModel(self.sorted_assets))
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.search_assets_le.textChanged.connect(self.search_paths)
        self.search_assets_le.setCompleter(self.completer)

        if self.config['status']:
            status_completer = QCompleter(self.config['status'])
            self.search_status_le.setCompleter(status_completer)

        if self.config['progress'].keys():
            progress_completer = QCompleter(self.config['progress'].keys())
            self.search_progress_le.setCompleter(progress_completer)


    def set_status(self):
        # Sort Assets
        # asset_sorted_list = sorted(self.assets.items(), key=lambda x:x[0])
        #
        # self.assets = OrderedDict()
        # for m in asset_sorted_list:
        #     self.assets[m[0]] = m[1]

        for asset, status in self.ui_values.items():
            if not asset in self.assets.keys():
                self.assets[asset] = OrderedDict()
                for stn, sts in status.items():
                    self.assets[asset][stn] = sts.currentText()

        for asset, status in self.assets.items():
            if not asset in self.config['exclude']:
                self.set_progress(asset, status)

        self.get_ui_status()


    def create_menubar(self):
        self.menu_bar = self.menuBar()

        # Files
        self.file_menu = self.menu_bar.addMenu('File')
        self.create_file_menus(self.file_menu)

        # Edit
        self.edit_menu = self.menu_bar.addMenu('Edit')
        self.create_edit_menus(self.edit_menu)

    def buildUI(self):
        # get config
        self.get_config()
        self.expire_limit_colors = self.config['expire_limit_colors']

        # self.save_config()
        self.get_current()
        print('Get Current')

        # UI
        self.layout()
        self.widgets()
        self.create_menubar()
        print('Build GUI')

        # Set init file
        try:
            self.set_init_file()
        except Exception as e:
            print(traceback.format_exc())

        print('Set Init File')

        # init set
        self.init_setting()
        print('Set Init Setting')

    def init_setting(self):
        # Name sort
        self.sort_qcbx.setCurrentText(self.sort_types[1])
        self.sort_qcbx.setCurrentText(self.sort_types[0])

        # Save Current
        self.save_current() # 新規アセットが追加されたら更新されないためSaveする

    def create_file_menus(self, actions_menu):
        file_menus = OrderedDict()
        file_menus['whatsNew'] = {'cmd':partial(self.whatsNew)}
        file_menus['Import Assets Status'] = {'cmd':partial(self.file_transfer, 'open')}
        file_menus['Save Assets Status'] = {'cmd':partial(self.save_assets_status)}
        file_menus['Save Assets Status As....'] = {'cmd':partial(self.file_transfer, 'save')}
        file_menus['Save CSV As....'] = {'cmd':partial(self.file_transfer, 'save_csv')}
        file_menus['Save CSV Status List As....'] = {'cmd':partial(self.file_transfer, 'save_csv_status_list')}

        for action_name, action_setting in file_menus.items():
            # Check Max Influences
            if 'separator' in action_name:
                actions_menu.addSeparator()
            else:
                self.cmi_action = QAction(QIcon(''),
                                         action_name,
                                         self,
                                         statusTip=action_name,
                                         triggered=action_setting['cmd'])
                actions_menu.addAction(self.cmi_action)

    def create_edit_menus(self, actions_menu):
        file_menus = OrderedDict()
        file_menus['List Assets'] = {'cmd':partial(self.print_assets)}

        for action_name, action_setting in file_menus.items():
            # Check Max Influences
            if 'separator' in action_name:
                actions_menu.addSeparator()
            else:
                self.cmi_action = QAction(QIcon(''),
                                         action_name,
                                         self,
                                         statusTip=action_name,
                                         triggered=action_setting['cmd'])
                actions_menu.addAction(self.cmi_action)

    def build_statusBox(self, asset):
        self.ui_values[asset] = OrderedDict()

        wid = QWidget()
        self.status_qhbl.addWidget(wid)
        wid.setFixedHeight(80)
        # wid.setStyleSheet("background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); ")
        # wid.setStyleSheet("margin:5px; border:0.1px solid rgb(0, 255, 0); ")

        qhbox = QHBoxLayout()
        wid.setLayout(qhbox)
        qhbox.setAlignment(Qt.AlignLeft)

        self.assets_sections[asset] = wid
        self.assets_search[asset] = wid

        # asset check
        self.asset_chb = QCheckBox()
        qhbox.addWidget(self.asset_chb)

        self.cur_checkBox_wids[asset] = self.asset_chb

        self.cur_assets[asset] = OrderedDict()
        self.cur_assets[asset]['checkBox'] = self.asset_chb

        # Priority
        self.cur_cbx = QComboBox()
        self.cur_cbx.resize(self.cur_cbx.sizeHint())
        self.cur_cbx.addItems([str(p) for p in self.config['priority']])
        # self.cur_cbx.setFixedWidth(40)
        qhbox.addWidget(self.cur_cbx)

        self.cur_priority_wids[asset] = self.cur_cbx

        self.cur_assets[asset]['priority'] = self.cur_cbx

        # Calender
        cal_v_wid = QWidget()
        qhbox.addWidget(cal_v_wid)

        cal_qvbox = QVBoxLayout()
        cal_v_wid.setLayout(cal_qvbox)

        self.start_dateEdit = QDateEdit(self)
        self.start_dateEdit.setDate(QDate.currentDate())
        self.start_dateEdit.setCalendarPopup(True)
        cal_qvbox.addWidget(self.start_dateEdit)

        self.end_dateEdit = QDateEdit(self)
        self.end_dateEdit.setDate(QDate.currentDate())
        self.end_dateEdit.setCalendarPopup(True)
        self.end_dateEdit.dateChanged.connect(self.notice_expire_days)
        cal_qvbox.addWidget(self.end_dateEdit)

        self.cur_assets[asset]['expire_date'] = [self.start_dateEdit, self.end_dateEdit]

        self.cur_expire_date_wids[asset] = [self.start_dateEdit, self.end_dateEdit]

        self.expire_date_search[asset] = [self.start_dateEdit, self.end_dateEdit, wid]

        asset_v_wid = QWidget()
        qhbox.addWidget(asset_v_wid)

        asset_qvbox = QVBoxLayout()
        asset_v_wid.setLayout(asset_qvbox)

        # asset QLabel
        self.asset_le = QLineEdit()
        self.asset_le.setText(asset)
        self.asset_le.setReadOnly(True)
        self.asset_le.resize(self.asset_le.sizeHint())
        asset_qvbox.addWidget(self.asset_le)

        self.status_search[asset] = OrderedDict()

        # description
        self.asset_dcp_btn = QPushButton('{}:description'.format(asset))
        self.asset_dcp_btn.clicked.connect(self.description_window)
        asset_qvbox.addWidget(self.asset_dcp_btn)

        dcpt_dlg = QDialog()
        dcpt_lay = QVBoxLayout()
        dcpt_editor = QTextEdit()
        # self.dcpt_editor.setPlainText('Hellow PySide!!') # plain_text

        dcpt_dlg.setLayout(dcpt_lay)
        dcpt_lay.addWidget(dcpt_editor)

        dcpt_ok_btn = QPushButton('OK')
        dcpt_ok_btn.clicked.connect(self.save_current)
        dcpt_lay.addWidget(dcpt_ok_btn)

        dcpt_dlg.setWindowTitle('{}:description'.format(asset))

        self.cur_assets[asset]['description'] = [dcpt_dlg, dcpt_editor]


        # Status
        self.status_name_list = self.config['status']

        status_wid_list = OrderedDict()
        for stn in self.status_name_list:
            v_wid = QWidget()
            qhbox.addWidget(v_wid)

            qvbox = QVBoxLayout()
            v_wid.setLayout(qvbox)
            status_wid_list[stn] = qvbox

            self.status_search[asset][stn] = v_wid

            # status QLabel
            qlabel = QLabel(stn)
            qlabel.resize(qlabel.sizeHint())
            qvbox.addWidget(qlabel)


        # Progress
        self.progress_cbx_list[asset] = OrderedDict()
        for stn, qv_wid in status_wid_list.items():
            # QComboBox
            status_cbx = QComboBox()
            # status_cbx.resize(status_cbx.sizeHint())
            status_cbx.setEditable(True)
            status_cbx.addItems(self.config['progress'].keys())
            status_cbx.currentIndexChanged.connect(self.change_status)

            qv_wid.addWidget(status_cbx)
            self.progress_cbx_list[asset][stn] = status_cbx

            self.ui_values[asset][stn] = status_cbx
            # print(self.assets)
            self.assets[asset][stn] = status_cbx.currentText()


    def set_progress(self, asset, status):
        self.progress_search[asset] = OrderedDict()
        for stn, sts in status.items():
            # print(setting, status_slot)
            if stn in self.progress_cbx_list[asset].keys():
                status_cbx = self.progress_cbx_list[asset][stn]
                status_cbx.setCurrentText(sts)

                self.progress_search[asset][status[stn]] = self.assets_sections[asset]

                # else:
                #     self.assets[asset].pop(stn)
                #
            # except KeyError:
            #     self.assets.pop(asset)
            #     print(traceback.format_exc())

    def change_status(self, index):
        sender = self.sender()
        # self.get_ui_status()
        try:
            bg_color = self.config['progress'][sender.currentText()]
            sender.setStyleSheet("background:{}".format(bg_color))
        except:
            sender.setStyleSheet("background:Window")

        if self.auto_save_qcbx.isChecked():
            self.save_assets_status()

    def get_ui_status(self):
        # print(self.ui_values)
        for asset, status in self.ui_values.items():
            for stn, sts in status.items():
                self.assets[asset][stn] = sts.currentText()

                try:
                    bg_color = self.config['progress'][sts.currentText()]
                    sts.setStyleSheet("background:{}".format(bg_color))
                except:
                    sts.setStyleSheet("background:Window")

    def description_window(self):
        sender = self.sender()

        text = sender.text()
        asset = text.split(':description')[0]

        dcpt_dlg, dcpt_editor = self.cur_assets[asset]['description']
        dcpt_dlg.exec_()


    def clear_description_window(self, event):
        self.dcpt_lay.removeWidget(self.dcpt_editor)
        # self.dcpt_editor.deleteLater()
        # self.dcpt_editor = None

        self.dcpt_lay.removeWidget(self.dcpt_ok_btn)
        # self.dcpt_ok_btn.deleteLater()
        # self.dcpt_ok_btn = None

    def update_priority(self):
        priority = [self.cur_assets_dict[asset]['priority'] for asset in self.sorted_assets]
        assets_sort = OrderedDict(zip(self.sorted_assets, priority))
        self.priority_sort_assets = OrderedDict(sorted(assets_sort.items(), key=lambda x:x[1], reverse=True))

    def update_expire_date(self):
        for asset in self.sorted_assets:
            expire_date = self.cur_assets_dict[asset]['expire_date']
            self.start_sort_date[asset] = QDate(*expire_date[0])
            self.end_sort_date[asset] = QDate(*expire_date[1])

    def showhide_checked(self):
        for asset in self.sorted_assets:
            if 'All Show' == self.showhide_checked_qcbx.currentText():
                self.assets_sections[asset].show()

            elif 'Hide:Unchecked' == self.showhide_checked_qcbx.currentText():
                if not self.cur_checkBox_wids[asset].isChecked():
                    self.assets_sections[asset].hide()
                else:
                    self.assets_sections[asset].show()

            elif 'Hide:Checked' == self.showhide_checked_qcbx.currentText():
                if self.cur_checkBox_wids[asset].isChecked():
                    self.assets_sections[asset].hide()
                else:
                    self.assets_sections[asset].show()


    def sort_wid(self):
        # sort name
        if 'Name:Descending' == self.sort_qcbx.currentText():
            sort_objects = OrderedDict(sorted(self.assets.items(), key=lambda x:x[0], reverse=True))
        if 'Name:Ascending' == self.sort_qcbx.currentText():
            sort_objects = OrderedDict(sorted(self.assets.items(), key=lambda x:x[0]))

        # sort Priority
        if 'Priority:Descending' == self.sort_qcbx.currentText():
            sort_objects = OrderedDict(sorted(self.priority_sort_assets.items(), key=lambda x:x[1], reverse=True))
        if 'Priority:Ascending' == self.sort_qcbx.currentText():
            sort_objects = OrderedDict(sorted(self.priority_sort_assets.items(), key=lambda x:x[1]))

        # sort start date
        if 'Start Date:Descending' == self.sort_qcbx.currentText():
            sort_objects = OrderedDict(sorted(self.start_sort_date.items(), key=lambda x:x[1], reverse=True))
        if 'Start Date:Ascending' == self.sort_qcbx.currentText():
            sort_objects = OrderedDict(sorted(self.start_sort_date.items(), key=lambda x:x[1]))

        # sort end date
        if 'End Date:Descending' == self.sort_qcbx.currentText():
            sort_objects = OrderedDict(sorted(self.end_sort_date.items(), key=lambda x:x[1], reverse=True))
        if 'End Date:Ascending' == self.sort_qcbx.currentText():
            sort_objects = OrderedDict(sorted(self.end_sort_date.items(), key=lambda x:x[1]))

        for asset, obj in sort_objects.items():
            wid = self.assets_sections[asset]
            layout = wid.parentWidget().layout()
            layout.removeWidget(wid)

        i = 0
        for asset, obj in sort_objects.items():
            wid = self.assets_sections[asset]
            layout = wid.parentWidget().layout()
            layout.insertWidget(i, wid)
            i += 1


    def notice_expire_days(self, finished_cbx):
        sender = self.sender()

        expire = sender.date()
        between_date = int(self.today_qdate.daysTo(expire))

        # between_date = 0 - dif_date
        if 0 >= between_date:
            between_date = 0

        max_date = max([int(d) for d in self.expire_limit_colors.keys()])
        if max_date == between_date:
            between_date = max_date

        if max_date < between_date:
            sender.setStyleSheet("background:Window")
        else:
            sender.setStyleSheet("background:{}".format(self.expire_limit_colors[str(between_date)]))

    def change_expire_days_color(self, date_edit):
        expire = date_edit.date()
        between_date = int(self.today_qdate.daysTo(expire))

        # between_date = 0 - dif_date
        if 0 >= between_date:
            between_date = 0

        max_date = max([int(d) for d in self.expire_limit_colors.keys()])
        if max_date == between_date:
            between_date = max_date

        if max_date < between_date:
            date_edit.setStyleSheet("background:Window")
        else:
            date_edit.setStyleSheet("background:{}".format(self.expire_limit_colors[str(between_date)]))


    def remove_assets_sections(self):
        # self.stock_widgets
        for wid in self.assets_sections.values():
            self.status_qhbl.removeWidget(wid)
            wid.deleteLater()
            wid = None
            # self.clearLayout(lay)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                    del(widget)
                else:
                    self.clearLayout(item.layout())
                    del(item)

    def search_assets(self):
        search_txt = self.search_assets_le.text()
        filtered = list(set(fnmatch.filter(self.assets_search.keys(), search_txt)))

        extract = [extra for extra in self.assets_search.keys() if not extra in filtered]

        if not filtered:
            for wid in self.assets_search.values():
                # wid.show()
                self.show_wids.append(wid)

        else:
            for extract_txt in extract:
                # self.assets_search[extract_txt].hide()
                self.hide_wids.append(self.assets_search[extract_txt])

                if 'Hide:Unchecked' == self.showhide_checked_qcbx.currentText():
                    if not self.cur_checkBox_wids[extract_txt].isChecked():
                        self.hide_wids.append(self.assets_sections[extract_txt])
                    else:
                        self.show_wids.append(self.assets_sections[extract_txt])

                elif 'Hide:Checked' == self.showhide_checked_qcbx.currentText():
                    if self.cur_checkBox_wids[extract_txt].isChecked():
                        self.hide_wids.append(self.assets_sections[extract_txt])
                    else:
                        self.show_wids.append(self.assets_sections[extract_txt])


        for searched_txt in filtered:
            if not searched_txt in extract:
                # self.assets_search[searched_txt].show()
                self.show_wids.append(self.assets_search[searched_txt])

                if 'Hide:Unchecked' == self.showhide_checked_qcbx.currentText():
                    if not self.cur_checkBox_wids[searched_txt].isChecked():
                        self.hide_wids.append(self.assets_sections[searched_txt])
                    else:
                        self.show_wids.append(self.assets_sections[searched_txt])

                elif 'Hide:Checked' == self.showhide_checked_qcbx.currentText():
                    if self.cur_checkBox_wids[searched_txt].isChecked():
                        self.hide_wids.append(self.assets_sections[searched_txt])
                    else:
                        self.show_wids.append(self.assets_sections[searched_txt])


    def search_status(self):
        search_txt = self.search_status_le.text()

        status_list = []
        for asset, status in self.status_search.items():
            for stn, tv_wid in status.items():
                status_list.append(stn)

        filtered = list(set(fnmatch.filter(status_list, search_txt)))

        extract = [extra for extra in status_list if not extra in filtered]

        if not filtered:
            for asset, status in self.status_search.items():
                for stn, wid in status.items():
                    # wid.show()
                    self.show_wids.append(wid)

        else:
            for extract_txt in extract:
                for asset, status in self.status_search.items():
                    for stn, wid in status.items():
                        if stn == extract_txt:
                            # wid.hide()
                            self.hide_wids.append(wid)

        for searched_txt in filtered:
            if not searched_txt in extract:
                for asset, status in self.status_search.items():
                    for stn, wid in status.items():
                        if stn == searched_txt:
                            # wid.show()
                            self.show_wids.append(wid)


    def search_expire_date(self):
        set_start_date = self.search_start_dateEdit.date()
        set_end_date = self.search_end_dateEdit.date()

        for asset, between_date in self.expire_date_search.items():
            start_date = between_date[0].date()
            end_date = between_date[1].date()
            if self.search_dateEdit_switch_cb.isChecked():
                if set_start_date <= start_date and end_date <= set_end_date:
                    # between_date[2].show()
                    self.show_wids.append(between_date[2])
                else:
                    # between_date[2].hide()
                    self.hide_wids.append(between_date[2])
            else:
                # between_date[2].show()
                self.show_wids.append(between_date[2])

    def search_progress(self):
        search_txt = self.search_progress_le.text()

        status_list = []
        for asset, status in self.progress_search.items():
            for sts, tv_wid in status.items():
                status_list.append(sts)

        filtered = list(set(fnmatch.filter(status_list, search_txt)))

        extract = [extra for extra in status_list if not extra in filtered]

        if not filtered:
            for asset, status in self.progress_search.items():
                for sts, wid in status.items():
                    wid.show()
                    # self.show_wids.append(wid)
                    # if wid in self.hide_wids:
                    #     self.hide_wids.remove(wid)

        else:
            for extract_txt in extract:
                for asset, status in self.progress_search.items():
                    for sts, wid in status.items():
                        if sts == extract_txt:
                            wid.hide()
                            # self.hide_wids.append(wid)
                            # if wid in self.show_wids:
                            #     self.show_wids.remove(wid)

        for searched_txt in filtered:
            if not searched_txt in extract:
                for asset, status in self.progress_search.items():
                    for sts, wid in status.items():
                        if sts == searched_txt:
                            wid.show()
                            # self.show_wids.append(wid)
                            # if wid in self.hide_wids:
                            #     self.hide_wids.remove(wid)


    def search_functions(self):
        self.show_wids = []
        self.hide_wids = []

        self.search_assets()

        self.search_status()

        self.search_expire_date()

        # self.search_progress()
        self.show_wids = list(set(self.show_wids))
        self.hide_wids = list(set(self.hide_wids))
        [sw.show() for sw in self.show_wids]
        [hw.hide() for hw in self.hide_wids]

        # self.refresh_UI()

    def refresh_UI(self):
        self.search_functions()
        self.sort_wid()
        self.showhide_checked()

    def print_assets(self):
        print(self.assets)
        print([asset.decode(encoding="utf-8") for asset in self.assets.keys()])

    def file_transfer(self, file_by=None):
        last_path = self.open_file(self.temp_directory)
        if last_path == False or not os.path.isdir(last_path):
            last_path = os.path.expanduser('~') + '/Desktop'

        if file_by == 'open':
            (self.fileName, selectedFilter) = QFileDialog.getOpenFileName(self, 'Open file', last_path, "JSON (*.json)")
            if self.fileName != "":
                # QMessageBox.information(self, "File", fileName)
                self.assets = json_transfer(self.fileName, 'import')
                self.set_status()

        elif file_by == 'save':
            (self.fileName, selectedFilter) = QFileDialog.getSaveFileName(self, 'Save file', last_path, "JSON (*.json)")
            if self.fileName != "":
                # QMessageBox.information(self, "File", fileName)
                self.get_ui_status()
                json_transfer(self.fileName, 'export', self.assets)

        elif file_by == 'save_csv':
            (self.fileName_csv, selectedFilter) = QFileDialog.getSaveFileName(self, 'Save file', last_path, "CSV (*.csv)")
            if self.fileName_csv != "":
                # QMessageBox.information(self, "File", fileName)
                self.get_ui_status()
                csv_transfer(self.status_name_list, self.fileName_csv, 'export', self.assets, self.cur_assets_dict)

        elif file_by == 'save_csv_status_list':
            (self.fileName_csv, selectedFilter) = QFileDialog.getSaveFileName(self, 'Save file', last_path, "CSV (*.csv)")
            if self.fileName_csv != "":
                # QMessageBox.information(self, "File", fileName)
                self.get_ui_status()
                csv_transfer(self.status_name_list, self.fileName_csv, 'export', self.assets, self.cur_assets_dict, True)

        if self.fileName != "":
            self.write_file(self.temp_directory, '/'.join(self.fileName.split('/')[0:-1:]))

    def save_assets_status(self):
        self.get_ui_status()
        json_transfer(self.fileName, 'export', self.assets)

    def open_file(self, directory):
        try:
            with open(directory) as openfile:
                last_path = openfile.read()

            return last_path
        except:
            return False

    def write_file(self, directory, string_to_write):
        with open(str(directory),"w") as openfile:
            openfile.write(string_to_write)

    def write_csv(self):
        csv_transfer(fileName=None, operation=None, export_values=self.assets)

    def set_init_file(self):
        self.fileName = self.config['init_file']
        if not os.path.isfile(self.fileName):
            self.fileName = replace_for_user(self.fileName)

        if os.path.isfile(self.fileName):
            self.assets = json_transfer(self.fileName, 'import')
            # if file_encoding == 'shift-jis':
            #     for asset, value in self.assets.items():
            #         self.assets[asset.encode('shift-jis')] = value
            #         del(self.assets[asset])

            self.set_status()

    def whatsNew(self):
        self.whatsNew_fileName = self.config['whatsNew']
        if not os.path.isfile(self.whatsNew_fileName):
            self.whatsNew_fileName = replace_for_user(self.whatsNew_fileName)

        if os.path.isfile(self.whatsNew_fileName):
            print('READ whatsNew:{}'.format(self.whatsNew_fileName))
            with codecs.open(self.whatsNew_fileName, 'r', encoding='utf-8') as f:
                data = f.read()

            dcpt_dlg = QDialog()
            dcpt_lay = QVBoxLayout()
            dcpt_editor = QTextEdit()
            font = QFont()

            dcpt_editor.setPlainText(data) # plain_text
            dcpt_editor.setReadOnly(True)

            font.setPointSize(16)
            dcpt_editor.setFont(font)

            dcpt_dlg.setLayout(dcpt_lay)
            dcpt_lay.addWidget(dcpt_editor)
            dcpt_dlg.setWindowTitle('whatsNew')

            dcpt_dlg.exec_()

        else:
            print('{} is not found.'.format(self.whatsNew_fileName))


    def get_config(self):
        try:
            if self.project:
                pj_path = 'projects/{}/'.format(self.project)
                print('Load Project Config:', self.project)
            else:
                pj_path = ''

            self.data_path = '{}/{}'.format('/'.join(__file__.replace('\\', '/').split('/')[0:-1]), 'data')
            self.config_file = '{}/{}config.json'.format(self.data_path, pj_path)

            try:
                with codecs.open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f, 'utf-8', object_pairs_hook=OrderedDict, strict=False)
            except:
                print(traceback.format_exc())
                with open(self.config_file, 'r', encoding="utf-8") as f:
                    self.config = json.load(f, object_pairs_hook=OrderedDict, strict=False)

        except Exception as e:
            print(traceback.format_exc())

    def save_config(self):
        json_transfer(self.config_file, 'export', self.config)

    def get_current(self):
        try:
            self.current_file = self.config['cur_file']
            if not os.path.isfile(self.current_file):
                self.current_file = replace_for_user(self.current_file)

            if not os.path.isfile(self.current_file):
                self.data_path = '{}/{}'.format('/'.join(__file__.replace('\\', '/').split('/')[0:-1]), 'data')
                self.current_file = '{}/current.json'.format(self.data_path)

            try:
                with codecs.open(self.current_file, 'r', encoding='utf-8') as f:
                    self.cur_assets_dict = json.load(f, 'utf-8', object_pairs_hook=OrderedDict)

            except:
                print(traceback.format_exc())
                with open(self.current_file, 'r', encoding="utf-8") as f:
                    self.cur_assets_dict = json.load(f, object_pairs_hook=OrderedDict)

        except Exception as e:
            print(traceback.format_exc())

    def save_current(self):
        for asset, cur_dict in self.cur_assets.items():
            self.cur_assets_dict[asset] = OrderedDict()
            for type, chb in cur_dict.items():
                if type == 'checkBox':
                    self.cur_assets_dict[asset][type] = chb.isChecked()
                elif type == 'priority':
                    self.cur_assets_dict[asset][type] = chb.currentText()
                elif type == 'expire_date':
                    self.cur_assets_dict[asset][type] = [[chb[0].date().year(), chb[0].date().month(), chb[0].date().day()],
                                                         [chb[1].date().year(), chb[1].date().month(), chb[1].date().day()]]
                elif type == 'description':
                    self.cur_assets_dict[asset][type] = chb[1].toPlainText()


        json_transfer(self.current_file, 'export', self.cur_assets_dict)
        # text = json.dumps(self.cur_assets_dict, sort_keys=True, ensure_ascii=False, indent=4)
        # with open(self.current_file, "w") as fh:
        #     fh.write(text.encode("utf-8"))

        self.update_priority()
        self.update_expire_date()

    def search_paths(self):
        # path = str(path.split('*')[-1])
        search_paths = [s for s in self.load_values['path']]
        filtered = list(set(fnmatch.filter(search_paths, self.sender().text())))
        # self.model().setStringList(filtered)
        if not filtered:
            self.completer.model().setStringList(self.load_values['path'])

        else:
            self.completer.model().setStringList(filtered)

        self.completer.popup()


class PathCompleter(QCompleter):
    def __init__(self, *args):
        super().__init__(*args)

    def setModel(self, model):
        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(model)
        self.proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        super().setModel(self.proxyModel)

    def updatePattern(self, patternStr):
        self.proxyModel.setFilterWildcard(patternStr)


def json_transfer(fileName=None, operation=None, export_values=None):
    if operation == 'export':
        try:
            # print(type(export_values.keys()[0]))
            # 'shift-jis'
            with codecs.open(fileName, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)

        except:
            print(traceback.format_exc())
            with open(fileName, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)

    elif operation == 'import':
        try:
            with codecs.open(fileName, 'r', encoding='utf-8') as f:
                return json.load(f, 'utf-8', object_pairs_hook=OrderedDict)

        except:
            print(traceback.format_exc())
            with open(fileName, 'r', encoding="utf-8") as f:
                return json.load(f, object_pairs_hook=OrderedDict)


def csv_transfer(status_list=None, fileName=None, operation=None, export_values=None, cur_assets_dict=None, from_status=None):
    # sys.getdefaultencoding()

    # --------------------------------------------------------------------------
    if from_status:
        new_export_values = OrderedDict()
        for name, val in export_values.items():
            for k, v in val.items():
                new_key = u'{}.{}'.format(k, v)
                new_export_values[new_key] = []

        for con_val in new_export_values.keys():
            for name, val in export_values.items():
                for k, v in val.items():
                    if con_val.split('.')[0] == k:
                        if con_val.split('.')[1] == v:
                            new_export_values[con_val].append(name)

        dct_arr = []
        for con_val, names in new_export_values.items():
            add_arr = []
            add_arr.append(con_val.encode('cp932'))
            dct_arr.append(add_arr)

            for n in names:
                sub_add_arr = []
                sub_add_arr.append('')
                sub_add_arr.append(n.encode('cp932'))
                dct_arr.append(sub_add_arr)

            ept_add_arr = []
            ept_add_arr.append('')
            dct_arr.append(ept_add_arr)


    elif not from_status:
        labels = ['Name'] + status_list
        if cur_assets_dict:
            labels.append('StartDate')
            labels.append('EndDate')

        labels = [l.encode('cp932') for l in labels]

        dct_arr = []
        for name, val in export_values.items():

            new_export_values = OrderedDict()
            new_export_values['Name'] = name.encode('cp932')

            for k,v in val.items():
                new_export_values[k.encode('cp932')] = v.encode('cp932')

            if cur_assets_dict:
                new_export_values['StartDate'] = cur_assets_dict[name]['expire_date'][0]
                new_export_values['EndDate'] = cur_assets_dict[name]['expire_date'][1]

            dct_arr.append(new_export_values)

    if operation == 'export':
        with codecs.open(fileName, 'w') as fin:
            if from_status:
                writer = csv.writer(fin, lineterminator='\n')
                for elem in dct_arr:
                    writer.writerow(elem)

            elif not from_status:
                writer = csv.DictWriter(fin, fieldnames=labels)
                writer.writeheader()
                for elem in dct_arr:
                    writer.writerow(elem)


def replace_for_user(replace_file):
    return replace_file.replace(replace_file.split('Users')[1].split('/')[1], os.getenv('USER'))


if __name__ == '__main__':
    ui = StatusChecker()
    ui.buildUI()
    ui.show(dockable=True)
