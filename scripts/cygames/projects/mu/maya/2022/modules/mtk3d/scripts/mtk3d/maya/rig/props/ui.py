# -*- coding: utf-8 -*-
from maya import cmds, mel
from maya import OpenMayaUI as omui

import maya.api.OpenMaya as om
import maya.mel as mm

from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

try:
    from mtk3d.maya.rig.props import common as props_common
except ImportError:
    print('ImportError')


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class PropSpaceDialog(QtWidgets.QDialog):
    dig_instance = None

    @classmethod
    def show_dialog(cls):
        if not cls.dig_instance:
            cls.dig_instance = PropSpaceDialog()

        if cls.dig_instance.isWindow():
            cls.dig_instance.show()
        else:
            cls.dig_instance.raise_()
            cls.dig_instance.activateWindow()

    side_param = ['_L_', '_R_']

    def __init__(self, parent=maya_main_window()):
        super(PropSpaceDialog, self).__init__(parent)
        self.setWindowTitle(u'Prop Space Dialog')
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.namespaces = None
        self.callback = None

        # 弓用ウィジェット
        self.bow_label = QtWidgets.QLabel(u'弓用ロケータの作成')
        self.bow_checkbox = QtWidgets.QCheckBox(u'左手からロケータの親を拘束する')
        self.bow_button = QtWidgets.QPushButton(u'弓用のロケータを作成する')
        self.bow_select_button = QtWidgets.QPushButton(u'ロケータを選択する')
        self.bow_bake_button = QtWidgets.QPushButton(u'ベイクする')
        self.bow_del_button = QtWidgets.QPushButton(u'弓用のロケータ郡を削除する')

        # 弓用レイアウト
        bow_layout = QtWidgets.QVBoxLayout()
        bow_layout.addWidget(self.bow_label)
        bow_layout.addWidget(self.bow_checkbox)
        bow_layout.addWidget(self.bow_button)
        bow_layout.addWidget(self.bow_select_button)
        bow_layout.addWidget(self.bow_bake_button)
        bow_layout.addWidget(self.bow_del_button)

        # 剣用ウィジェット
        self.sword_label = QtWidgets.QLabel(u'剣用ロケータの作成')
        self.sword_combobox = QtWidgets.QComboBox()
        self.sword_locs_refresh_button = QtWidgets.QPushButton()
        self.sword_locs_refresh_button.setIcon(QtGui.QIcon(':refresh.png'))
        # self.sword_button = QtWidgets.QPushButton(u'剣用のロケータを作成する')
        self.sword_button_v2 = QtWidgets.QPushButton(u'剣用のロケータを作成する')
        self.sword_select_button = QtWidgets.QPushButton(u'ロケータを選択する')
        self.sword_bake_button = QtWidgets.QPushButton(u'ベイクする')
        self.sword_del_button = QtWidgets.QPushButton(u'剣用のロケータ郡を削除する')

        self.sword_side_label = QtWidgets.QLabel(u'自動で回転させる手首')
        self.sword_l_radiobutton = QtWidgets.QRadioButton(u'Left')
        self.sword_r_radiobutton = QtWidgets.QRadioButton(u'Right')
        self.sword_r_radiobutton.setChecked(1)

        # 剣用レイアウト
        sword_layout = QtWidgets.QVBoxLayout()
        sword_type_layout = QtWidgets.QHBoxLayout()

        sword_type_layout.addWidget(self.sword_side_label)
        sword_type_layout.addWidget(self.sword_l_radiobutton)
        sword_type_layout.addWidget(self.sword_r_radiobutton)

        sword_layout.addWidget(self.sword_label)

        sword_layout.addLayout(sword_type_layout)

        sword_locs_layout = QtWidgets.QHBoxLayout()
        sword_locs_layout.addWidget(self.sword_combobox)
        sword_locs_layout.addWidget(self.sword_locs_refresh_button)

        sword_layout.addLayout(sword_locs_layout)

        # sword_layout.addWidget(self.sword_button)
        sword_layout.addWidget(self.sword_button_v2)
        sword_layout.addWidget(self.sword_select_button)
        sword_layout.addWidget(self.sword_bake_button)
        sword_layout.addWidget(self.sword_del_button)

        # メインレイアウト
        main_layout = QtWidgets.QVBoxLayout(self)
        self.ns_label = QtWidgets.QLabel(u'ネームスペース')
        self.ns_combobox = QtWidgets.QComboBox(self)
        main_layout.addWidget(self.ns_label)
        main_layout.addWidget(self.ns_combobox)

        # Propsレイアウト
        props_layout = QtWidgets.QHBoxLayout()
        props_layout.addLayout(bow_layout)

        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.VLine | QtWidgets.QFrame.Sunken)

        props_layout.addWidget(frame)

        props_layout.addLayout(sword_layout)

        # add mainlayout
        main_layout.addLayout(props_layout)

        self.connection()

        # ネームスペース取得
        self.get_current_namespaces()

        # 剣用のロケータ取得
        self.get_current_sword_loc()

        # MEventMessageの割り当て
        self.connectCallBack()

    def connection(self):
        self.ps = props_common.PropSpace()
        self.bow_button.clicked.connect(self.bow_do_PropSpace)
        self.bow_select_button.clicked.connect(self.bow_sel_loc)
        self.bow_bake_button.clicked.connect(self.bow_bake_ctrl)
        self.bow_del_button.clicked.connect(self.bow_del_grp)

        # self.sword_button.clicked.connect(self.sword_do_PropSpace)
        self.sword_button_v2.clicked.connect(self.sword_do_PropSpace_v2)
        self.sword_locs_refresh_button.clicked.connect(self.get_current_sword_loc)
        self.sword_select_button.clicked.connect(self.sword_sel_loc)
        self.sword_bake_button.clicked.connect(self.sword_bake_ctrl)
        self.sword_del_button.clicked.connect(self.sword_del_grp)

        self.ns_combobox.currentTextChanged.connect(self.set_namespace)
        self.sword_combobox.currentTextChanged.connect(self.set_prop_space_loc)

    def bow_do_PropSpace(self):
        checked = self.bow_checkbox.isChecked()
        if checked:
            self.ps.parentConst_piv_hand_obj = True
        else:
            self.ps.parentConst_piv_hand_obj = False

        self.ps.sword_enable = None

        self.ps.main()

    def bow_bake_ctrl(self):
        self.ps.bake_set()

    def bow_del_grp(self):
        self.ps.delete_prop_space_grp()

    def bow_sel_loc(self):
        if cmds.objExists(self.ps.ikHandle_loc[0]):
            cmds.select(self.ps.ikHandle_loc[0])

    def sword_do_PropSpace(self):
        sel = cmds.ls(os=1)
        if not sel:
            om.MGlobal.displayError(u'剣のリグに入っているPropSpaceロケータを選択してください')
            return
        else:
            obj = sel[0]
            self.ps.sword_enable = True

        self.ps.piv_obj = obj

        if self.sword_l_radiobutton.isChecked():
            self.ps.rot_obj = self.ps.rot_obj.replace(self.side_param[1], self.side_param[0])
        elif self.sword_r_radiobutton.isChecked():
            self.ps.rot_obj = self.ps.rot_obj.replace(self.side_param[0], self.side_param[1])

        self.ps.main()
        self.ps.sword_enable = None

    def sword_do_PropSpace_v2(self):
        self.ps.ply00_mtk_bakes_v2()
        cmds.ogs(reset=True)

    def sword_bake_ctrl(self):
        self.ps.bake_set()

    def sword_del_grp(self):
        self.ps.delete_prop_space_grp()

    def sword_sel_loc(self):
        if cmds.objExists(self.ps.ikHandle_loc[0]):
            cmds.select(self.ps.ikHandle_loc[0])

    def get_current_namespaces(self, *args):
        exclude_list = ['UI', 'shared']

        current = cmds.namespaceInfo(cur=True)
        cmds.namespace(set=':')
        self.namespaces = ['{}'.format(ns) for ns in cmds.namespaceInfo(lon=True) if ns not in exclude_list]
        cmds.namespace(set=current)

        # Reference Nodes
        rn = cmds.ls(type="reference", r=1)
        for i in rn:
            ref_ns = i.split("RN")
            ns = '{0}'.format(ref_ns[0])
            if not ns in self.namespaces:
                self.namespaces.append(ns)

        if self.namespaces == []:
            self.namespaces = ''

        self.ns_combobox.clear()
        self.ns_combobox.addItem('')
        for ns in self.namespaces:
            self.ns_combobox.addItem(ns)

        self.ps = props_common.PropSpace()
        self.get_current_sword_loc()

    def set_namespace(self, namespace):
        if namespace != '':
            self.ps.namespace = '{0}:'.format(namespace)
        else:
            self.ps.namespace = '{0}'.format(namespace)

        if self.ps.namespace != '':
            print('Current Namespace {0}'.format(self.ps.namespace))

    def get_current_sword_loc(self):
        locs = cmds.ls('prop_space_loc', r=1)
        self.sword_combobox.clear()
        self.sword_combobox.addItem('')
        for loc in locs:
            self.sword_combobox.addItem(loc)

    def set_prop_space_loc(self, loc):
        sel = cmds.ls(os=1)
        if loc:
            cmds.select(loc, r=1)
            self.ps.space_loc = loc
        else:
            pass

    def closeEvent(self, event):
        if self.callback:
            om.MEventMessage.removeCallback(self.callback)
            self.callback = None

    def connectCallBack(self):
        self.callback = om.MEventMessage.addEventCallback('SceneOpened', self.get_current_namespaces)


if __name__ == "__main__":
    try:
        ui.close()
        ui.deleteLater()
    except:
        pass

    ui = PropSpaceDialog()
    ui.show()
