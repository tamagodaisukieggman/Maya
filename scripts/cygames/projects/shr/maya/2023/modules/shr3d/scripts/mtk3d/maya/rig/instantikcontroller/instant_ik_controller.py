# -*- coding: utf-8 -*-
import utils
import os
import json

from functools import partial
import pymel.core as pm
import maya.mel as mm
import maya.api.OpenMaya as om

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

import PySide2.QtWidgets as qw
import PySide2.QtGui as qg
import PySide2.QtCore as qc

import widgets.button as button
import widgets.custom_spinbox as custom_spinbox
import widgets.label as label

from utils.generic import undo_pm

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


# MayaQWidgetBaseMixinを継承することで、画面の裏潜りなどを防ぎ、基本的なmayaのguiの挙動を持てる
class InstantIkMainWidget(MayaQWidgetDockableMixin, qw.QDialog):
    def __init__(self):
        super(InstantIkMainWidget, self).__init__()

        # mainレイアウト設定
        self.setWindowTitle("Instant IK Controller")
        self.setMinimumWidth(380)
        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.setAttribute(qc.Qt.WA_DeleteOnClose)

        # stylesheetの設定を読み込む
        file_path = qc.QFile("{}/stylesheets/scheme.qss".format(CURRENT_PATH))
        file_path.open(qc.QFile.ReadOnly | qc.QFile.Text)
        self.stream = qc.QTextStream(file_path)
        self.setStyleSheet(self.stream.readAll())
        file_path.close()

        # --------------------------------------------------------------------------------------------------------------
        # scroll areaの設定
        scroll_area = qw.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(qc.Qt.NoFocus)
        scroll_area.setHorizontalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOff)
        self.layout().addWidget(scroll_area)

        # --------------------------------------------------------------------------------------------------------------
        # main widgetとレイアウト作成/ バーティカルに子供のwidgetを配置していく
        main_widget = qw.QWidget()
        main_widget.setObjectName('Instant IK Controller')
        main_widget_layout = qw.QVBoxLayout()
        main_widget_layout.setContentsMargins(5, 15, 5, 15)
        main_widget_layout.setAlignment(qc.Qt.AlignTop)
        main_widget.setLayout(main_widget_layout)
        scroll_area.setWidget(main_widget)

        # --------------------------------------------------------------------------------------------------------------
        # 使用するレイアウトをまとめて用意してmain_widget_layoutへ追加する
        controller_picker_layout = qw.QHBoxLayout()
        controller_picker_layout2 = qw.QHBoxLayout()
        set_parent_checkbox_layout = qw.QHBoxLayout()
        set_parent_line_edit_layout = qw.QHBoxLayout()
        create_button_layout = qw.QHBoxLayout()
        controller_picker_layout.setAlignment(qc.Qt.AlignLeft)
        controller_picker_layout2.setAlignment(qc.Qt.AlignLeft)
        set_parent_checkbox_layout.setAlignment(qc.Qt.AlignLeft)
        set_parent_line_edit_layout.setAlignment(qc.Qt.AlignLeft)
        main_widget_layout.addLayout(controller_picker_layout)
        main_widget_layout.addLayout(controller_picker_layout2)
        main_widget_layout.addLayout(SplitterLayout())
        main_widget_layout.addLayout(set_parent_checkbox_layout)
        main_widget_layout.addLayout(set_parent_line_edit_layout)
        main_widget_layout.addLayout(SplitterLayout())
        main_widget_layout.addLayout(create_button_layout)

        # --------------------------------------------------------------------------------------------------------------
        # LineEdit / ik controller creator用のテキストとlineEditを作成してwidgetに追加
        self.num_of_controls_label = qw.QLabel("num of controls:")
        self.num_of_controls_label.setAlignment(qc.Qt.AlignRight)
        self.num_of_controls_label.setMinimumWidth(100)
        self.num_of_controls_label.setMaximumWidth(100)
        self.num_of_controls_combo = qw.QComboBox()
        [self.num_of_controls_combo.addItem(i) for i in ('3', '4', '5')]
        self.num_of_controls_combo.setCurrentIndex(0)
        self.num_of_controls_combo.setMinimumWidth(60)
        self.num_of_controls_combo.setMaximumWidth(60)
        controller_picker_layout.addWidget(self.num_of_controls_label)
        controller_picker_layout.addWidget(self.num_of_controls_combo)

        # --------------------------------------------------------------------------------------------------------------
        # LineEdit / ik controller creator用のテキストとlineEditを作成してwidgetに追加

        self.controller_space_label = qw.QLabel("controller space:")
        self.controller_space_label.setAlignment(qc.Qt.AlignRight)
        self.controller_space_label.setMinimumWidth(100)
        self.controller_space_label.setMaximumWidth(100)
        self.controller_space_combo = qw.QComboBox()
        [self.controller_space_combo.addItem(i) for i in ('world', 'parent space')]
        self.controller_space_combo.setCurrentIndex(0)
        self.controller_space_combo.setMinimumWidth(100)
        self.controller_space_combo.setMaximumWidth(100)
        controller_picker_layout2.addWidget(self.controller_space_label)
        controller_picker_layout2.addWidget(self.controller_space_combo)

        # --------------------------------------------------------------------------------------------------------------
        # Check box/ set parent object用のテキストとcheckboxを作成してwidgetに追加
        self.set_instant_ik_label = qw.QLabel("1. Select the parent controller first \n2. and then select the target "
                                              "controller in turn ")

        set_parent_checkbox_layout.setContentsMargins(20, 0, 0, 0)
        set_parent_checkbox_layout.addWidget(self.set_instant_ik_label)

        # --------------------------------------------------------------------------------------------------------------
        # Create buttonの作成
        self.create_button = qw.QPushButton('Create/ Refresh')
        create_button_layout.addWidget(self.create_button)
        self.create_button.clicked.connect(self.create_ik_controller_and_picker_widget)

        # --------------------------------------------------------------------------------------------------------------
        # instant ik widget 用レイアウト
        self.instant_ik_widget_layout = qw.QVBoxLayout()
        self.instant_ik_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.instant_ik_widget_layout.setSpacing(0)
        self.instant_ik_widget_layout.setAlignment(qc.Qt.AlignTop)
        main_widget_layout.addLayout(self.instant_ik_widget_layout)

        # --------------------------------------------------------------------------------------------------------------
        self.instant_ik_controller = ""
        self.selected_object = []
        self.constraint_to_be_delete_later = []
        self.parent_controller = None
        self.killLst = []

        # --------------------------------------------------------------------------------------------------------------
        self._interp_widget = []
        self._dock_widget = self._dock_name = None
        self._create_job()

    def _create_job(self):
        self.killLst.append(pm.scriptJob(event=["SceneOpened", self._scenes_open], protected=True))
        self.killLst.append(pm.scriptJob(event=["NewSceneOpened", self._scenes_open], protected=True))
        self.killLst.append(pm.scriptJob(event=["Undo", self._do_undo], protected=True))

    def _scenes_open(self):
        # delete picker GUI
        print("delete")
        self.close()
        print("refresh")

    def _do_undo(self):
        obj = pm.objExists("instant_ik_grp")
        if not obj:
            try:
                self.delete_instant_ik_controller_widget(self.new_widget)
            except:
                pass

    def set_text_to_le(self):
        sel = pm.ls(sl=True)
        self.set_parent_name_le.setText(sel[0].name())

    def cb_callback(self):
        if self.set_instant_ik_checkbox.isChecked():
            for i in [self.set_parent_name_label, self.set_parent_name_le, self.parent_name_button]:
                i.setEnabled(True)
        else:
            for i in [self.set_parent_name_label, self.set_parent_name_le, self.parent_name_button]:
                i.setEnabled(False)

    def check_parent_controller(self, sel):
        self.parent_controller = sel.pop(0)

    @undo_pm
    def reload_instant_ik_widget(self):
        obj = pm.ls(type="implicitSphere")
        if obj:
            attrs = pm.getAttr(obj[0] + ".user_defined_attrs")
            jsn = json.loads(attrs)
            name = str(jsn["name"])
            ik_controls = list(jsn["ik_ctrl"])
            ik_handles = str(jsn["ik_handle"])
            self.constraint_to_be_delete_later = list(jsn["constraint_to_be_delete_later"])
            self.selected_object = list(jsn["selected_object"])

            self.add_instant_ik_widget(ik_controls=ik_controls, ik_handles=ik_handles, name=name)
            self.set_enable_callback(False)

    def find_the_implicit_sphere(self):
        if pm.objExists("instant_ik_grp"):
            self.reload_instant_ik_widget()
            return True
        else:
            return False

    @undo_pm
    def create_ik_controller_and_picker_widget(self):
        # sceneに既にコントローラーがないか確認する
        if self.find_the_implicit_sphere():
            pm.confirmDialog(title="Done", message="Reloaded GUI.")
            return

        # create button を押したら対象のコントローラーが3つ以上選択されているか判定する
        if 4 > len(pm.ls(sl=True)):
            pm.confirmDialog(title="Error", message="Please select at for 4 objects.")
            return
        # create buttonを押したら作成したいコントローラーの数が、num of controller comboより多いか確認する
        if int(self.num_of_controls_combo.currentText()) > len(pm.ls(sl=True)):
            pm.confirmDialog(title="Error",
                             message="The number of controllers should be less than you have selected.")
            return

        # --------------------------------------------------------------------------------------------------------------
        # controllerの作成
        self.check_parent_controller(sel=pm.ls(sl=True))
        self.instant_ik_controller = InstantIkController(num_of_controls=self.num_of_controls_combo.currentText(),
                                                         parent_controller=self.parent_controller,
                                                         world_space=self.controller_space_combo.currentText())
        self.instant_ik_controller.run_create()

        # --------------------------------------------------------------------------------------------------------------
        # pickerの作成
        ik_controls = self.instant_ik_controller.ik_controls
        ik_controls = [obj.name() for obj in ik_controls]
        ik_handles = self.instant_ik_controller.spline_ik_handle
        self.add_instant_ik_widget(ik_controls=ik_controls, ik_handles=ik_handles, name="instant_ik")
        self.set_enable_callback(value=False)

    def set_enable_callback(self, value):
        self.num_of_controls_label.setEnabled(value)
        self.create_button.setEnabled(value)
        self.num_of_controls_combo.setEnabled(value)

    @undo_pm
    def add_instant_ik_widget(self, ik_controls, ik_handles, name):
        self.new_widget = InstantIkWidget(ik_controls, ik_handles, name)
        self.instant_ik_widget_layout.addWidget(self.new_widget)
        self._interp_widget.append(self.new_widget)
        self.new_widget.bake_button.clicked.connect(partial(self.bake_fk_and_remove_instant_ik_widget, self.new_widget))
        self.new_widget.delete_and_close.clicked.connect(
            partial(self.remove_instant_ik_controller_and_widget, self.new_widget))
        self.setMinimumHeight(350)

    def bake_fk_controls(self):
        try:
            self.instant_ik_controller.bake_target(self.instant_ik_controller.selected_object)
        except:
            self.bake_target(target=self.selected_object)

    def bake_target(self, target):
        time_range = self._get_time_range()
        pm.bakeResults(target, t=(time_range[0], time_range[1]), sm=True,
                       at=["t", "tx", "ty", "tz", "r", "rx", "ry", "rz"])

    def _get_time_range(self, start_frame=None, end_frame=None):
        if start_frame is None:
            if mm.eval("timeControl -q -rv $gPlayBackSlider"):
                start_frame = mm.eval("timeControl -q -ra $gPlayBackSlider")[0]
            else:
                start_frame = pm.playbackOptions(q=True, min=True)

        if end_frame is None:
            if mm.eval("timeControl -q -rv $gPlayBackSlider"):
                end_frame = mm.eval("timeControl -q -ra $gPlayBackSlider")[1]
            else:
                end_frame = pm.playbackOptions(q=True, max=True)

        return start_frame, end_frame

    @undo_pm
    def delete_instant_ik_controller(self):
        try:
            pm.lockNode(self.instant_ik_controller.root_group, l=False)
            pm.delete(self.instant_ik_controller.constraint_to_be_delete_later)
            pm.delete(self.instant_ik_controller.root_group)
        except:
            pm.lockNode("instant_ik_grp", l=False)
            pm.delete(self.constraint_to_be_delete_later)
            pm.delete("instant_ik_grp")

    @undo_pm
    def bake_fk_and_remove_instant_ik_widget(self, interp_widget):
        self.bake_fk_controls()
        self.remove_instant_ik_controller_and_widget(interp_widget)

    @undo_pm
    def remove_instant_ik_controller_and_widget(self, interp_widget):
        self.delete_instant_ik_controller()
        self.delete_instant_ik_controller_widget(interp_widget)

    def delete_instant_ik_controller_widget(self, interp_widget):
        if interp_widget in self._interp_widget:
            self._interp_widget.remove(interp_widget)
            self.instant_ik_widget_layout.removeWidget(interp_widget)
        interp_widget.deleteLater()
        self.set_enable_callback(True)

    @undo_pm
    def delete(self, instant_widget):
        self.instant_ik_layout.removeWidget(instant_widget)
        instant_widget.deleteLater()

    @undo_pm
    def clear_all(self, *args):
        for instant_widget in self._instant_widget:
            instant_widget.crearItems()

    @undo_pm
    def connect_dock_widget(self, dock_name, dock_widget):
        self._dock_widget = dock_widget
        self._dock_name = dock_name

    @undo_pm
    def close(self):
        if self._dock_widget:
            print("dock_widget: True")
            pm.deleteUI(self._dock_name)
        else:
            print("dock_widget: None")
            qw.QDialog.close(self)

        self._dock_widget = self._dock_name = None

    def kill(self):
        for k in self.killLst:
            pm.scriptJob(kill=k, force=True)
        print("kill")

    def closeEvent(self, event):
        self.kill()
        # print(self.SCRIPT_JOB_NUMBER)
        # pm.scriptJob(kill=self.SCRIPT_JOB_NUMBER, force=True)
        # super(InstantIkMainWidget, self).closeEvent(event)


# mayaのシーンにinstant ikのコントローラーを作成する
class InstantIkController(object):
    def __init__(self, num_of_controls, parent_controller=None, world_space=None):
        self.num_of_controls = int(num_of_controls)
        self.parent_controller = parent_controller
        self.world_space = world_space
        print(self.world_space)

        # --------------------------------------------------------------------------------------------------------------
        self.selected_object = pm.ls(sl=True)
        parent_controller = self.selected_object.pop(0)
        # print(self.selected_object, parent_controller)
        self.num_of_selections = len(self.selected_object)
        self.position_of_the_selected_object = []
        self.ik_joints = []
        self.fk_joints = []
        self.locator = []
        self.locator_shape = []
        self.ik_joint_and_selected_object = {}

        self.ik_joints_space = []
        self.root_group = []
        self.implicit_sphere = []
        self.fk_group = []
        self.fk_group_space = []

        # world or parent space controller
        self.ik_controls = []
        self.world_space_control = []
        self.ik_to_ik_dummy = {}

        self.clusters_attached_to_curve_cv = []
        self.cluster_group = []
        self.dummy_spline_crv = []
        self.spline_crv = []
        self.spline_ik_handle = []
        self.instance_loc = []
        self.instance_attr_shape = []
        self.ik_controller_scale = []

        self.del_list = []
        self.constraint_to_be_delete_later = []

    @undo_pm
    def run_create(self):
        self.create_hierarchy_to_receive_fk_movements()
        self.create_spline_ik()
        self.create_root_group()
        self.create_ik_controller()
        self.group_all(self.spline_crv,
                       self.dummy_spline_crv,
                       self.clusters_attached_to_curve_cv,
                       self.spline_ik_handle,
                       self.fk_group_space,
                       self.ik_joints_space[0])

        # self.world_ik_controls
        self.bake()
        self.connect_all()
        self.constraint_to_parent()
        self.set_display_mode()
        if self.world_space == "world":
            self.ik_controls = self.world_space_control
        else:
            print("world space ha false")
        self.add_attribute_to_implicit_sphere()

    def bake(self):
        pm.refresh(su=True)
        pm.makeIdentity(self.ik_joints, apply=True, t=True, r=True, s=True)
        if self.world_space == "world":
            self.target_of_bake = (
                    self.locator + self.fk_group_space + self.root_group + self.fk_group + self.world_space_control)
        else:
            self.target_of_bake = (self.locator + self.fk_group_space + self.root_group + self.fk_group)

        self.bake_target(self.target_of_bake)
        if self.world_space == "world":
            self.set_euler_filter()
        pm.refresh(su=False)
        pm.delete(self.del_list)

    def connect_all(self):
        self._connect_to_fk()
        self._connect_to_ik()
        if self.world_space == "world":
            self._connect_world_ik_to_ik()
        # self.lock_and_hide_attr(self.world_ik_controls, attrs=["rx", "ry", "rz", "sx", "sy", "sz", "v", "ihi"])
        # self.lock_and_hide_attr(self.ik_controls, attrs=["rx", "ry", "rz", "sx", "sy", "sz", "v", "ihi"])

    def group_all(self, *args):
        [pm.parent(x, self.root_group[0]) for x in args]

    def set_display_mode(self):
        [pm.setAttr(x + ".overrideEnabled", 1) for x in self.fk_joints]
        [pm.setAttr(x + ".overrideDisplayType", 1) for x in self.fk_joints]
        [pm.setAttr(x + ".overrideEnabled", 1) for x in self.locator]
        [pm.setAttr(x + ".overrideDisplayType", 1) for x in self.locator]
        pm.hide(self.ik_joints_space)
        if self.world_space == "world":
            pm.hide(self.ik_controls)

    def constraint_to_parent(self):
        if self.parent_controller:
            print(self.fk_group[0])
            prc = pm.parentConstraint(self.parent_controller, self.fk_group[0], mo=True)
            self.constraint_to_be_delete_later.append(prc)
        else:
            pass

    def add_attribute_to_implicit_sphere(self):
        objs = [x.name() for x in self.ik_controls]
        deletes = [x.name() for x in self.constraint_to_be_delete_later]
        selected = [x.name() for x in self.selected_object]
        pm.addAttr(self.implicit_sphere, shortName="ud_attrs", longName="user_defined_attrs", dt="string")
        dicts = {}
        dicts.update(name="instant_ik")
        dicts.update(ik_ctrl=objs)
        dicts.update(ik_handle=self.spline_ik_handle[0].name())
        dicts.update(constraint_to_be_delete_later=deletes)
        dicts.update(selected_object=selected)
        jsn = json.dumps(dicts)
        pm.setAttr(self.root_group[0] + ".ud_attrs", jsn)

    def parent_cluster(self):
        fk_num = float(self.num_of_selections)
        ik_num = float(self.num_of_controls)
        val = (fk_num / ik_num)
        round_val = round(val)

        for i in range(len(self.cluster_group)):
            pos = (i + 1) * (round_val)
            pos = int(pos) - 1
            try:
                pm.parent(self.cluster_group[i], self.locator[pos])
            except:
                pos = pos - 1
                pm.parent(self.cluster_group[i], self.locator[pos])

    # fk controllerの値を流し込む構造を作成する
    def create_hierarchy_to_receive_fk_movements(self):
        obj = self.selected_object
        obj_num = self.num_of_selections
        # self.del_list = []
        for i in range(obj_num):
            name = obj[i].name()
            parent_of_the_selected_object = pm.listRelatives(obj[i], parent=True)
            locator = pm.spaceLocator(n="{}_loc".format(name))
            locator_shape = locator.getShape()
            receive_fk_grp = pm.createNode("transform", n="{}_grp".format(name))
            fk_jnt = pm.joint(n="{}_jnt".format(name))
            position_of_the_selected_object = pm.xform(obj[i], q=True, ws=True, t=True)
            pm.select(cl=True)
            ik_jnt = pm.joint(n="{}_ik_jnt".format(name))
            pm.delete(pm.parentConstraint(obj[i], ik_jnt, mo=False))

            self.fk_joints.append(fk_jnt)
            self.ik_joints.append(ik_jnt)
            self.position_of_the_selected_object.append(position_of_the_selected_object)
            self.locator.append(locator)
            self.locator_shape.append(locator_shape)
            ik_joint_and_selected_object = {ik_jnt: obj[i]}
            self.ik_joint_and_selected_object.update(ik_joint_and_selected_object)

            fk_jnt.setParent(locator)
            locator.setParent(receive_fk_grp)
            pm.delete(pm.parentConstraint(parent_of_the_selected_object, receive_fk_grp))
            pm.delete(pm.parentConstraint(obj[i], ik_jnt))
            self.del_list.append(pm.parentConstraint(obj[i], locator))

            if i > 0:
                i -= 1
                receive_fk_grp.setParent(self.fk_joints[i])
                pm.select(clear=True)
                pm.parent(self.ik_joints[i + 1], self.ik_joints[i])
            else:
                self.ik_joints_space.append(pm.createNode("transform", n="{}_ik_jnt_space".format(name)))
                pm.parent(self.ik_joints[0], self.ik_joints_space[0])
                parent_of_the_selected_object_space = pm.listRelatives(parent_of_the_selected_object, parent=True)

                fk_group_space = pm.createNode("transform", n="{}_grp_space".format(name))
                pm.delete(pm.parentConstraint(parent_of_the_selected_object_space, fk_group_space))
                pm.parent(receive_fk_grp, fk_group_space)
                self.del_list.append(pm.parentConstraint(parent_of_the_selected_object_space, fk_group_space))
                self.del_list.append(pm.parentConstraint(parent_of_the_selected_object, receive_fk_grp))
                receive_fk_grp.setParent(fk_group_space)
                self.fk_group.append(receive_fk_grp)
                self.fk_group_space.append(fk_group_space)

        # --------------------------------------------------------------------------------------------------------------
        # create tip joint
        tip_jnt = pm.createNode("joint", n="tip_jnt")
        tip_locator = pm.spaceLocator(n="tip_locator")
        dummy_tip_locator = pm.spaceLocator(n="dummy_tip_locator")
        tip_group = pm.createNode("transform", n="tip_group")
        dummy_tip_locator.setParent(tip_locator)
        tip_jnt.setParent(tip_locator)
        tip_locator.setParent(tip_group)
        pm.delete(pm.parentConstraint(self.ik_joints[-1], tip_group, mo=False))
        pm.delete(pm.parentConstraint(self.ik_joints[-2], dummy_tip_locator, mo=False))
        tip_group.setParent(self.fk_joints[-1])

        dummy_pos = pm.getAttr(dummy_tip_locator + ".translate")
        dum_x = round(dummy_pos[0] * -1)
        dum_y = round(dummy_pos[1] * -1)
        dum_z = round(dummy_pos[2] * -1)

        tip_group.tx.set(dum_x)
        tip_group.ty.set(dum_y)
        tip_group.tz.set(dum_z)

        tip_ik_jnt = pm.createNode("joint", n="tip_ik_jnt")
        pm.delete(pm.parentConstraint(tip_jnt, tip_ik_jnt, mo=False))
        tip_ik_jnt.setParent(self.ik_joints[-1])

        tip_pos = pm.xform(tip_jnt, q=True, ws=True, t=True)
        self.position_of_the_selected_object.append(tip_pos)
        self.ik_joints.append(tip_ik_jnt)
        self.fk_joints.append(tip_jnt)

    def create_spline_ik(self):
        self.dummy_spline_crv.append(pm.curve(ep=self.position_of_the_selected_object, d=1))
        pm.select(clear=True)
        spline_ik = (pm.ikHandle(name='instant_spline_ik_#',
                                 solver='ikSplineSolver',
                                 startJoint=self.ik_joints[0],
                                 endEffector=self.ik_joints[-1],
                                 numSpans=self.num_of_controls - 2))

        spline_ik_handle = spline_ik[0]
        spline_curve = spline_ik[2]
        spline_curve = pm.rename(spline_curve, 'spline_curve_#')
        pm.hide(spline_curve, spline_ik_handle)

        self.spline_crv.append(spline_curve)
        self.spline_ik_handle.append(spline_ik_handle)

    def rebuild_curve(self):
        pm.rebuildCurve(self.spline_crv, self.dummy_spline_crv, rt=2)
        pm.hide(self.dummy_spline_crv)

    def bind_spline_curve(self):
        pm.skinCluster(self.fk_joints, self.spline_crv[0])

    def bake_target(self, target):
        time_range = self._get_time_range()
        pm.bakeResults(target, t=(time_range[0], time_range[1]), sm=True,
                       at=["t", "tx", "ty", "tz", "r", "rx", "ry", "rz"])

    def set_euler_filter(self, *args):
        for jnt in self.world_space_control:
            try:
                pm.filterCurve(jnt + ".rx", jnt + ".ry", jnt + ".rz", filter="euler")
            except:
                print(attr)

    def _connect_to_fk(self):
        for src, trg in self.ik_joint_and_selected_object.items():
            self.constraint_to_be_delete_later.append(pm.orientConstraint(src, trg, mo=True))

    def _connect_to_ik(self):
        pm.parentConstraint(self.locator[0], self.ik_joints_space[0], mo=True)

    def _connect_world_ik_to_ik(self):
        for src, trg in self.ik_to_ik_dummy.items():
            pm.pointConstraint(src, trg, mo=True)

    def create_root_group(self):
        grp = pm.createNode("implicitSphere", n="instant_ik_grp_shape")
        prt = pm.listRelatives(grp, p=True)
        pm.rename(prt, "instant_ik_grp")
        pm.select(prt)
        pm.addAttr(shortName='loc_scale', longName='locator_scale', defaultValue=1.0, k=True, h=False)
        self.root_group.append(prt[0])
        self.implicit_sphere.append(grp)
        self.lock_and_hide_attr(self.root_group, attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"])
        pm.lockNode(prt, l=True)

    def _connect_attributes(self):
        for i in self.locator_shape:
            pm.connectAttr(self.root_group[0] + ".loc_scale", i + ".localScaleX")
            pm.connectAttr(self.root_group[0] + ".loc_scale", i + ".localScaleY")
            pm.connectAttr(self.root_group[0] + ".loc_scale", i + ".localScaleZ")

    def create_ik_controller(self):
        curve_cvs = pm.ls('{}.cv[:]'.format(self.spline_crv[0]), flatten=1)
        for i, cv in enumerate(curve_cvs):
            cv_cluster = pm.cluster(cv, name='spline_{}_cluster'.format(i))
            cv_cluster = cv_cluster[1]  # pm.cluster() returns [cluster, handle]
            self.clusters_attached_to_curve_cv.append(cv_cluster)

            if i > 0:
                grp = pm.createNode("transform")
                self.cluster_group.append(grp)
                cv_pos = pm.pointPosition(cv)
                ik_control = self.create_controller_shapes('instantik_spline_{}_ctrl'.format(i), cv_pos)
                pm.makeIdentity(ik_control, apply=1, t=1, r=1, s=1, n=0)
                pm.connectAttr(ik_control + ".tx", cv_cluster + ".tx")
                pm.connectAttr(ik_control + ".ty", cv_cluster + ".ty")
                pm.connectAttr(ik_control + ".tz", cv_cluster + ".tz")
                pm.hide(cv_cluster)
                pm.parent(ik_control, grp)
                self.ik_controls.append(ik_control)
            pm.hide(cv_cluster)

        if self.world_space == 'world':
            self.create_world_ik_controls()

        self.create_instance_shape()
        self.rebuild_curve()
        self.bind_spline_curve()
        self.parent_an_instance_shape_to_ik_controller()
        self.parent_cluster()

    def create_world_ik_controls(self):
        for i in self.ik_controls:
            name = i.split("_ctrl")
            ctrl = pm.duplicate(i, name=name[0] + "_world_ctrl")
            ik_to_dummy = {ctrl[0]: i}
            self.ik_to_ik_dummy.update(ik_to_dummy)
            self.world_space_control.append(ctrl[0])
            self.del_list.append(pm.parentConstraint(i, ctrl[0], mo=True))
            pm.parent(ctrl[0], "instant_ik_grp")

    def create_controller_shapes(self, prefix, pos):
        ctrl_object = pm.circle(n=prefix + '_ctrl', ch=False, normal=[1, 0, 0], radius=1)[0]
        shape_name = pm.listRelatives(ctrl_object, s=True)
        pm.rename(shape_name, prefix + "_ctrlShape")

        add_shape = pm.circle(n=prefix + '_ctlr2', ch=False, normal=[0, 1, 0], radius=1)[0]
        shape_name = pm.listRelatives(add_shape, s=True)
        pm.rename(shape_name, prefix + "_ctrl2Shape")
        pm.parent(pm.listRelatives(add_shape, s=1), ctrl_object, r=1, s=1)
        pm.delete(add_shape)

        add_shape = pm.circle(n=prefix + '_ctlr3', ch=False, normal=[0, 0, 1], radius=1)[0]
        shape_name = pm.listRelatives(add_shape, s=True)
        pm.rename(shape_name, prefix + "_ctrl3Shape")
        pm.parent(pm.listRelatives(add_shape, s=1), ctrl_object, r=1, s=1)
        pm.delete(add_shape)

        # set scale
        scale = self._distance(self.fk_joints[0], self.fk_joints[1]) * 0.8
        self.ik_controller_scale.append(scale)
        pm.setAttr(ctrl_object + ".sx", scale)
        pm.setAttr(ctrl_object + ".sy", scale)
        pm.setAttr(ctrl_object + ".sz", scale)
        pm.makeIdentity(ctrl_object, apply=True, t=True, r=True, s=True)
        pm.makeIdentity(ctrl_object, apply=False, t=True, r=True, s=True)

        # set color
        pm.setAttr(ctrl_object + ".overrideEnabled", True)
        pm.setAttr(ctrl_object + ".overrideColorRGB", *(0.03, 0.355, 0.355))
        pm.setAttr(ctrl_object + ".overrideRGBColors", 1)

        pm.move(pos[0], pos[1], pos[2], ctrl_object, absolute=1)

        return ctrl_object

    def create_instance_shape(self):
        loc = pm.spaceLocator(n="instantik_org_loc")
        shape = pm.listRelatives(loc, s=True)[0]
        shape = pm.rename(shape, "instantik_duplicate_shape")
        pm.setAttr(shape + ".v", 0)
        self.instance_attr_shape.append(shape)
        self.instance_loc.append(loc)
        self.lock_and_hide_attr(shape,
                                attrs=["localPositionX", "localPositionY", "localPositionZ", "localScaleX",
                                       "localScaleY",
                                       "localScaleZ"])

    def lock_and_hide_attr(self, objects, attrs):
        objs = []
        if isinstance(objects, list):
            objs = objects
        else:
            objs.append(objects)
        for obj in objs:
            for attr in attrs:
                pm.setAttr("{}.{}".format(obj, attr), k=False, l=True, channelBox=False)

    def parent_an_instance_shape_to_ik_controller(self):
        inst = [None] * self.num_of_controls
        for i in range(self.num_of_controls):
            inst[i] = pm.instance(self.instance_attr_shape)[0]
            sp = pm.listRelatives(inst[i], s=True)
            pm.parent(sp, self.ik_controls[i], s=True, add=True, r=True)
        pm.delete(inst, self.instance_loc)

    @staticmethod
    def _get_time_range(start_frame=None, end_frame=None):
        if start_frame is None:
            if mm.eval("timeControl -q -rv $gPlayBackSlider"):
                start_frame = mm.eval("timeControl -q -ra $gPlayBackSlider")[0]
            else:
                start_frame = pm.playbackOptions(q=True, min=True)

        if end_frame is None:
            if mm.eval("timeControl -q -rv $gPlayBackSlider"):
                end_frame = mm.eval("timeControl -q -ra $gPlayBackSlider")[1]
            else:
                end_frame = pm.playbackOptions(q=True, max=True)

        return start_frame, end_frame

    @staticmethod
    def _distance(source_jnt, child_jnt):
        dist = pm.createNode('distanceDimShape', n='deleteme_I_am_in_pain_do_it')
        s = pm.xform(source_jnt, q=True, ws=True, rp=True)
        e = pm.xform(child_jnt, q=True, ws=True, rp=True)
        pm.setAttr(dist + '.endPoint', *s)
        pm.setAttr(dist + '.startPoint', *e)
        distance = pm.getAttr(dist + '.distance')
        pm.delete(pm.listRelatives(dist, p=True))
        return int(distance)


class InstantIkWidget(qw.QFrame):
    id = ""
    callback_id = ""

    def __init__(self, ik_controls, ik_handles, name):
        super(InstantIkWidget, self).__init__()
        self.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)

        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(3, 1, 3, 3)
        self.layout().setSpacing(0)
        self.setMinimumHeight(180)
        self.rubberBand = None
        self.origin = None
        self.ik_handles = ik_handles
        self.ik_buttons = []
        self.name = name

        title_layout = qw.QHBoxLayout()
        ik_layout = qw.QHBoxLayout()
        bake_layout = qw.QHBoxLayout()

        ik_layout.setAlignment(qc.Qt.AlignLeft)
        ik_layout.setContentsMargins(0, 40, 25, 40)
        ik_layout.setSpacing(20)

        layouts = [title_layout,
                   ik_layout,
                   SplitterLayout(),
                   bake_layout]
        [self.layout().addLayout(x) for x in layouts]

        title_line = Splitter(text=self.name)
        title_layout.addWidget(title_line)

        self.ik_ctrl_lb = qw.QLabel("Ik Controller: ")
        self.ik_ctrl_lb.setAlignment(qc.Qt.AlignRight)
        self.ik_ctrl_lb.setMaximumWidth(100)
        self.ik_ctrl_lb.setMinimumWidth(100)
        ik_layout.addWidget(self.ik_ctrl_lb)
        ik_layout.setAlignment(qc.Qt.AlignLeft)

        self.bake_button = qw.QPushButton("Bake and Close")
        bake_layout.setContentsMargins(5, 10, 5, 10)
        bake_layout.setSpacing(5)
        bake_layout.addWidget(self.bake_button)

        self.delete_and_close = qw.QPushButton("Close")
        bake_layout.addWidget(self.delete_and_close)

        # select button
        self.grp = qw.QButtonGroup()
        ik_num = len(ik_controls)
        for btn in range(ik_num):
            ik_button = button.DTButton()
            ik_button.setObjectName(ik_controls[btn])
            ik_button.setCheckable(True)
            ik_layout.addWidget(ik_button)
            self.grp.addButton(ik_button)
            self.ik_buttons.append(ik_button)

        self._connect()

    def _connect(self):
        [btn.clicked.connect(self.callback) for btn in self.ik_buttons]

    def callback(self):
        pm.select(clear=True)
        buttons = self.findChildren(qw.QPushButton)
        controls_list = []

        for btn in buttons:
            if btn.isChecked():
                controls_list.append(btn)
            else:
                pass
        [pm.select(ctrl.objectName(), add=True) for ctrl in controls_list]

    @undo_pm
    def set_value(self, *args):
        pm.setAttr("{}_duplicate_shape.{}".format(self.name, args[0]), float(args[1]))

    def bake_target(self, target):
        time_range = self._get_time_range()
        pm.bakeResults(target, t=(time_range[0], time_range[1]), sm=True,
                       at=["t", "tx", "ty", "tz", "r", "rx", "ry", "rz"])

    @staticmethod
    def _get_time_range(start_frame=None, end_frame=None):
        if start_frame is None:
            if mm.eval("timeControl -q -rv $gPlayBackSlider"):
                start_frame = mm.eval("timeControl -q -ra $gPlayBackSlider")[0]
            else:
                start_frame = pm.playbackOptions(q=True, min=True)

        if end_frame is None:
            if mm.eval("timeControl -q -rv $gPlayBackSlider"):
                end_frame = mm.eval("timeControl -q -ra $gPlayBackSlider")[1]
            else:
                end_frame = pm.playbackOptions(q=True, max=True)

        return start_frame, end_frame

    @undo_pm
    def mousePressEvent(self, event):
        self.origin = event.pos()
        if not self.rubberBand:
            self.rubberBand = qw.QRubberBand(qw.QRubberBand.Rectangle, self)
        self.rubberBand.setGeometry(qc.QRect(self.origin, qc.QSize()))
        self.rubberBand.show()

    # mouseをドラッグすると四角を描画する
    @undo_pm
    def mouseMoveEvent(self, event):
        self.rubberBand.setGeometry(qc.QRect(self.origin, event.pos()).normalized())

    # mouseRelease時の挙動
    @undo_pm
    def mouseReleaseEvent(self, event):
        modifiers = qw.QApplication.keyboardModifiers()
        self.rubberBand.hide()

        modifiers = qw.QApplication.keyboardModifiers()

        # shiftが押されていた場合
        if modifiers == qc.Qt.ShiftModifier:
            print('Shift+Click')
            self.grp.setExclusive(False)
            self.findChildren(qw.QPushButton)
            selected = []
            rect = self.rubberBand.geometry()

            for child in self.findChildren(qw.QPushButton):
                if rect.intersects(child.geometry()):
                    selected.append(child)

            for j in selected:
                if j.isChecked():
                    j.click()
                else:
                    j.click()

        # controlが押されていた場合
        elif modifiers == qc.Qt.ControlModifier:
            print('Control+Click')
            self.grp.setExclusive(False)
            self.findChildren(qw.QPushButton)
            selected = []
            rect = self.rubberBand.geometry()

            for child in self.findChildren(qw.QPushButton):
                if rect.intersects(child.geometry()):
                    selected.append(child)
            for j in selected:
                if j.isChecked():
                    j.click()
                else:
                    pass

        # shift + ctrlが押されていた場合
        elif modifiers == (qc.Qt.ControlModifier | qc.Qt.ShiftModifier):
            print('Control + Shift + Click')
            self.grp.setExclusive(False)
            self.findChildren(qw.QPushButton)
            selected = []
            rect = self.rubberBand.geometry()

            for child in self.findChildren(qw.QPushButton):
                if rect.intersects(child.geometry()):
                    selected.append(child)
            for j in selected:
                if j.isChecked():
                    pass
                else:
                    j.click()

        # 何も押されていなかった場合
        else:
            print('drag Click')
            self.grp.setExclusive(False)
            getBtn = self.findChildren(qw.QPushButton)
            for i in getBtn:
                if i.isChecked():
                    i.click()
            self.grp.setExclusive(True)

            selected = []
            rect = self.rubberBand.geometry()
            for child in self.findChildren(qw.QPushButton):
                if rect.intersects(child.geometry()):
                    selected.append(child)

            for j in selected:
                self.grp.setExclusive(False)
                j.click()


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


def create(docked=True):
    global dialog
    if dialog is None:
        dialog = InstantIkMainWidget()

    if docked:
        # dialog.show(dockable=True)
        dialog.show()
    else:
        dialog.show()


def delete():
    global dialog
    if dialog is None:
        return

    dialog.deleteLater()
    dialog = None
