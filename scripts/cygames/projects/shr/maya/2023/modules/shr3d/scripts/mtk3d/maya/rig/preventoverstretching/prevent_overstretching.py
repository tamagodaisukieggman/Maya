# -*- coding: utf-8 -*-
import os
import sys

import math

import maya.cmds as mc
import pymel.core as pm

from functools import wraps

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

import PySide2.QtWidgets as qw
import PySide2.QtGui as qg
import PySide2.QtCore as qc

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


def undo_redo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        is_error = False
        pm.undoInfo(ock=True)
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e)
            is_error = True
        finally:
            pm.undoInfo(cck=True)
            if is_error:
                raise
            return result

    return wrapper


def cycle_check_on_off(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        is_error = False
        pm.cycleCheck(evaluation=False)
        try:
            result = func(*args, **kwargs)
        except Exception:
            is_error = True
        finally:
            pm.cycleCheck(evaluation=True)
            if is_error:
                raise
            return result

    return wrapper


class PreventOverstretching(MayaQWidgetBaseMixin, qw.QDialog):
    def __init__(self):
        super(PreventOverstretching, self).__init__()

        # mainレイアウト設定
        self.setWindowTitle("Prevent Overstretching Tool")
        self.setMinimumWidth(380)
        self.setMaximumHeight(130)
        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 5)
        self.layout().setSpacing(0)

        # --------------------------------------------------------------------------------------------------------------
        # stylesheetの設定を読み込む
        file_path = qc.QFile("{}/stylesheets/scheme.qss".format(CURRENT_PATH))
        file_path.open(qc.QFile.ReadOnly | qc.QFile.Text)
        self.stream = qc.QTextStream(file_path)
        self.setStyleSheet(self.stream.readAll())
        file_path.close()

        # --------------------------------------------------------------------------------------------------------------
        # main widgetとレイアウト作成/ バーティカルに子供のwidgetを配置していく
        main_widget = qw.QWidget()
        main_widget.setObjectName('Prevent Overstretching Tool')
        main_widget_layout = qw.QVBoxLayout()
        main_widget_layout.setContentsMargins(5, 5, 5, 10)
        main_widget_layout.setAlignment(qc.Qt.AlignTop)
        main_widget.setLayout(main_widget_layout)
        self.layout().addWidget(main_widget)

        # --------------------------------------------------------------------------------------------------------------
        # 使用するレイアウトをまとめて用意してmain_widget_layoutへ追加する
        namespace_selection_layout = qw.QHBoxLayout()
        hand_selection_button_layout = qw.QHBoxLayout()
        bake_and_delete_button_layout = qw.QHBoxLayout()
        main_widget_layout.addLayout(namespace_selection_layout)
        main_widget_layout.addLayout(SplitterLayout())
        main_widget_layout.addLayout(hand_selection_button_layout)
        main_widget_layout.addLayout(SplitterLayout())
        main_widget_layout.addLayout(bake_and_delete_button_layout)

        # --------------------------------------------------------------------------------------------------------------
        # ベイク対象のロケーターを格納する
        self.group_of_locator_to_be_bake = []

        # ベイク対象のコントローラーを格納する
        self.grp_of_controller_to_be_bake = []

        # --------------------------------------------------------------------------------------------------------------
        # namespace selection の作成
        self.namespace_selection_lb = qw.QLabel("namespace:")
        self.nmsp_cb = qw.QComboBox()

        # Create buttonの作成
        self.left_hand_button = qw.QPushButton('L hand IK')
        self.right_hand_button = qw.QPushButton('R hand IK')
        self.both_hand_button = qw.QPushButton('Both hand IK')
        self.bake_and_delete_button = qw.QPushButton("Bake and Delete")
        self.delete_button = qw.QPushButton("Delete")

        self.hand_button_group = [self.left_hand_button, self.right_hand_button, self.both_hand_button]
        self.bake_and_close_group = [self.bake_and_delete_button, self.delete_button]

        # ボタンをレイアウトに追加
        [namespace_selection_layout.addWidget(btn) for btn in
         [self.namespace_selection_lb, self.nmsp_cb]]
        [hand_selection_button_layout.addWidget(btn) for btn in self.hand_button_group]
        [bake_and_delete_button_layout.addWidget(btn) for btn in self.bake_and_close_group]

        # --------------------------------------------------------------------------------------------------------------
        # set namespace
        self.get_namespaces()

        # --------------------------------------------------------------------------------------------------------------
        # check rig type
        self._check_rig_type()
        # --------------------------------------------------------------------------------------------------------------
        # connecting buttons and methods
        [btn.clicked.connect(self._callback) for btn in self.hand_button_group]

        self.bake_and_delete_button.clicked.connect(self._bake_and_delete_prevent_controller)
        self.delete_button.clicked.connect(self.do_delete_controller)

        # --------------------------------------------------------------------------------------------------------------
        self._create_job()

    def get_namespaces(self):
        self.nmsp_cb.clear()
        references = pm.ls(type="reference")
        for rf in references:
            split_namespace = rf.split(":")
            num_of_namespace = len(split_namespace)
            if num_of_namespace == 1:
                for ns in split_namespace:
                    pure_namespace = ns.split("RN")
                    if pure_namespace[0]:
                        self.nmsp_cb.addItem(pure_namespace[0])

    def _scenes_open(self):
        self.get_namespaces()
        self._check_rig_type()

    def _create_job(self):
        pm.scriptJob(event=['SceneOpened', self._scenes_open], protected=True)

    def name_check(self, directions):
        for d in directions:
            self._set_rig_type(self.nmsp_cb.currentText(), d)
            if pm.objExists(self.ctrl_dict["arm_ik"]):
                return True
            else:
                pm.confirmDialog(title="Error",
                                 message="{} does not exist.".format(self.ctrl_dict["arm_ik"]))
                return False

    def prevent_locator_check(self, directions):
        for d in directions:
            if not pm.objExists("{}_ik_stretch_ctrl_grp".format(d)):
                return True
            else:
                pm.confirmDialog(title="Error",
                                 message="{}_ik_stretch_ctrl_grp already exist.".format(d))
                return False

    def _bake_and_delete_prevent_controller(self):
        if self.grp_of_controller_to_be_bake:
            self.lock_node(lock=False)
            self.do_bake_result(selected=self.grp_of_controller_to_be_bake)
            self.do_delete_controller()
            pm.select(cl=True)
            self.grp_of_controller_to_be_bake = []
            self.group_of_locator_to_be_bake = []
            print(self.grp_of_controller_to_be_bake)
        else:
            pm.warning("There is no controller.")

    def do_delete_controller(self):
        if self.grp_of_controller_to_be_bake:
            self.lock_node(lock=False)
            pm.delete(self.group_of_locator_to_be_bake)
            self.grp_of_controller_to_be_bake = []
            self.group_of_locator_to_be_bake = []
            print(self.grp_of_controller_to_be_bake)
        else:
            pm.warning("There is no controller.")

    def _lock_attributes(self, objs, attrs=None):
        if attrs is None:
            attrs = ["rx", "ry", "rz", "sx", "sy", "sz", "v"]
        for ob in objs:
            for attr in attrs:
                pm.setAttr("{}.{}".format(ob, attr), lock=True)

    def lock_node(self, lock=True):
        print(self.group_of_locator_to_be_bake)
        [pm.lockNode(ob, lock=lock) for ob in self.group_of_locator_to_be_bake]

    def _callback(self):
        sender = self.sender()
        if sender is self.left_hand_button:
            if self.name_check(directions=["L"]):
                if self.prevent_locator_check(directions="L"):
                    self.run_create(directions=["L"])
        if sender is self.right_hand_button:
            if self.name_check(directions=["R"]):
                if self.prevent_locator_check(directions="R"):
                    self.run_create(directions=["R"])
        if sender is self.both_hand_button:
            if self.name_check(directions=["L", "R"]):
                if self.prevent_locator_check(directions=["L", "R"]):
                    self.run_create(directions=["L", "R"])

            # self.run_create(directions=["R"])

    def get_distance(self,a,b):
        distance = math.sqrt(pow(a[0]-b[0],2)+pow(a[1]-b[1],2)+pow(a[2]-b[2],2))
        return distance

    # @undo_redo
    # @cycle_check_on_off
    def run_create(self, directions):
        selected_later = []
        delete_list = []
        dict_of_targets_to_connect_point = {}
        dict_of_targets_to_connect_aim = {}

        for direction in directions:
            self._set_rig_type(self.nmsp_cb.currentText(), direction)
            arm_start_loc = self.create_arm_start_dummy_locator(direction)

            ik_stretch_ctrl_g = pm.spaceLocator(n="{}_ik_stretch_ctrl_grp".format(direction))
            ik_point = pm.spaceLocator(n="{}_ik_point".format(direction))
            ik_stretch_ctrl = pm.spaceLocator(n="{}_ik_stretch_ctrl".format(direction))
            ik_point_g = pm.spaceLocator(n="{}_ik_point_grp".format(direction))
            get_ik = pm.spaceLocator(n="{}_get_ik".format(direction))

            self.group_of_locator_to_be_bake.extend(
                [arm_start_loc, ik_stretch_ctrl_g, ik_point, ik_stretch_ctrl, ik_point_g])

            pm.parent(ik_stretch_ctrl, ik_point)
            pm.parent(get_ik, ik_point)
            pm.parent(ik_point, ik_stretch_ctrl_g)
            pm.parent(ik_point_g, ik_stretch_ctrl_g)

            # print([arm_start_loc,ik_point],ik_stretch_ctrl)
            pm.pointConstraint(arm_start_loc, ik_stretch_ctrl_g)
            a_const = pm.aimConstraint(self.ctrl_dict["arm_ik"], ik_point)
            p_const_2 = pm.pointConstraint(self.ctrl_dict["arm_ik"], ik_stretch_ctrl)
            a_point = pm.xform(pm.PyNode(self.ctrl_dict["arm_ik"]),q=1,ws=1,rp=1)
            b_point = pm.xform(arm_start_loc,q=1,ws=1,rp=1)
            
            distance = self.get_distance(a_point,b_point)
            
            #腕の長さの1/2程度の位置を移動値とする
            move_val = distance+distance/2

            pm.move(move_val, 0, 0, get_ik, ls=True)
            p_const_3 = pm.pointConstraint(get_ik, ik_point_g)

            # append to delete list

            [delete_list.append(x) for x in [p_const_2, p_const_3, a_const, get_ik]]

            objs = [ik_point_g, ik_stretch_ctrl_g]
            self._lock_attributes(objs)
            [selected_later.append(ctrl) for ctrl in [ik_point_g, ik_point, ik_stretch_ctrl]]

            controllers = [self.ctrl_dict["arm_ik"], self.ctrl_dict["arm_pv"], self.ctrl_dict["shoulder"]]
            for ctrl in controllers:
                self.grp_of_controller_to_be_bake.append(ctrl)

            # set to dictionary
            point_dict = {
                "{}_ik_stretch_ctrl".format(direction): self.ctrl_dict["arm_ik"]}
            dict_of_targets_to_connect_point.update(point_dict)

            aim_dict = {"{}_ik_point_grp".format(direction): "{}_ik_point".format(direction)}
            dict_of_targets_to_connect_aim.update(aim_dict)

        # --------------------------------------------------------------------------------------------------------------
        # bake
        pm.select(selected_later, r=True)
        self.do_bake_result(selected_later)

        # delete constraint
        pm.delete(delete_list)

        # connect
        for k, v in dict_of_targets_to_connect_point.items():
            pm.pointConstraint(k, v)

        for k, v in dict_of_targets_to_connect_aim.items():
            pm.aimConstraint(k, v)

        self.lock_node(lock=True)
        pm.select(cl=True)

    def do_bake_result(self, selected):
        pm.refresh(su=True)
        start_frame = pm.playbackOptions(q=True, min=True)
        end_frame = pm.playbackOptions(q=True, max=True)
        pm.bakeResults(selected, t=(start_frame, end_frame), sm=True)
        pm.refresh(su=False)

    def create_arm_start_dummy_locator(self, *args):
        arm_start_loc = pm.spaceLocator(n="{}_arm_start".format(args[0]))
        pm.parent(arm_start_loc, self.ctrl_dict["shoulder"])
        pm.delete(pm.parentConstraint(self.ctrl_dict["upArm_jtProxy"], arm_start_loc, mo=False))
        print(type(self.ctrl_dict["shoulder"]), self.ctrl_dict["shoulder"])
        return arm_start_loc

    def _check_rig_type(self):
        if pm.objExists("*:arm_L"):
            self.controller_type = "est"
            print("In the scene is the eST3 rig")
        elif pm.objExists("*:hand_L_ik_ctrl"):
            self.controller_type = "cyrig"
            print("In the scene is the cyrig")
    
    #rigの種類に合わせ
    def _set_rig_type(self, nmsp, direction):
        if self.controller_type == "est":
            print("set rig type = est")
            self.ctrl_dict = {"shoulder": "{}:shoulder_{}".format(nmsp, direction),
                              "upArm_jtProxy": "{}:upArm_jtProxy_{}".format(nmsp, direction),
                              "arm_ik": "{}:arm_{}".format(nmsp, direction),
                              "arm_pv": "{}:arm_poleVector_{}".format(nmsp, direction)}

        elif self.controller_type == "cyrig":
            print("set rig type cyrig")
            self.ctrl_dict = {"shoulder": "{}:clavicle_{}_ikAutoRot_ctrl_ikAutoShoulder_ctrl".format(nmsp, direction),
                              "upArm_jtProxy": "{}:upperarm_{}_proxy_jnt".format(nmsp, direction),
                              "arm_ik": "{}:hand_{}_ik_ctrl".format(nmsp, direction),
                              "arm_pv": "{}:upperarm_{}_ik_pv_ctrl".format(nmsp, direction)}


class Splitter(qw.QWidget):
    def __init__(self, text=None, shadow=True, color=(150, 150, 150)):
        super(Splitter, self).__init__()

        # レイアウト
        self.setMinimumHeight(2)
        self.setLayout(qw.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(qc.Qt.AlignVCenter)

        # Line
        first_line = qw.QFrame()
        first_line.setFrameStyle(qw.QFrame.HLine)
        self.layout().addWidget(first_line)

        # 描画スタイルの設定
        main_color = 'rgba( %s, %s, %s, 255)' % color
        shadow_color = 'rgba( 45,  45,  45, 255)'

        bottom_border = ''
        if shadow:
            bottom_border = 'border-bottom:1px solid %s;' % shadow_color

        style_sheet = "border:0px solid rgba(0,0,0,0); \
                       background-color: %s; \
                       max-height:1px; \
                       %s" % (main_color, bottom_border)

        first_line.setStyleSheet(style_sheet)

        # テキストが無ければreturnを返してボーダーのみ描画
        if text is None:
            return

        # テキストがあれば、上記で定義したラインの幅を5に設定
        first_line.setMaximumWidth(5)
        # テキストのフォントを設定
        font = qg.QFont()
        font.setBold(True)

        text_width = qg.QFontMetrics(font)
        width = text_width.width(text) + 6

        # labelとしてテキストを設定
        label = qw.QLabel()
        label.setText(text)
        label.setFont(font)
        label.setMaximumWidth(width)
        label.setAlignment(qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)

        self.layout().addWidget(label)

        # テキストがあった場合にテキストに続けてラインを描画する
        second_line = qw.QFrame()
        second_line.setFrameStyle(qw.QFrame.HLine)
        second_line.setStyleSheet(style_sheet)
        self.layout().addWidget(second_line)


class SplitterLayout(qw.QHBoxLayout):
    def __init__(self):
        qw.QHBoxLayout.__init__(self)
        self.setContentsMargins(20, 2, 20, 2)

        splitter = Splitter(shadow=False, color=(100, 100, 100))
        splitter.setFixedHeight(1)

        self.addWidget(splitter)


dialog = None


def create(docked=False):
    global dialog
    if dialog is None:
        dialog = PreventOverstretching()

    if docked:
        dialog.show(dockable=True)
    else:
        dialog.show()


def delete():
    global dialog
    if dialog is None:
        return

    dialog.deleteLater()
    dialog = None
