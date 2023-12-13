# -*- coding: utf-8 -*-
# import utils
import os
import json

from functools import partial
import pymel.core as pm
import maya.mel as mm
import maya.api.OpenMaya as om

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import PySide2.QtWidgets as qw
import PySide2.QtGui as qg
import PySide2.QtCore as qc

from .widgets import button as button
from .widgets import custom_spinbox as custom_spinbox
from .widgets import label as label

from .utils.generic import undo_pm

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
        main_widget_layout.setContentsMargins(5, 5, 5, 5)
        main_widget_layout.setAlignment(qc.Qt.AlignTop)
        main_widget.setLayout(main_widget_layout)
        scroll_area.setWidget(main_widget)

        # --------------------------------------------------------------------------------------------------------------
        # 使用するレイアウトをまとめて用意してmain_widget_layoutへ追加する
        name_label_and_line_edit_layout = qw.QHBoxLayout()
        controller_picker_layout = qw.QHBoxLayout()
        create_button_layout = qw.QHBoxLayout()
        name_label_and_line_edit_layout.setAlignment(qc.Qt.AlignLeft)
        controller_picker_layout.setAlignment(qc.Qt.AlignLeft)
        main_widget_layout.addLayout(name_label_and_line_edit_layout)
        main_widget_layout.addLayout(controller_picker_layout)
        main_widget_layout.addLayout(SplitterLayout())
        main_widget_layout.addLayout(create_button_layout)

        # --------------------------------------------------------------------------------------------------------------
        # コントローラーの名前設定用のlineEdit
        name_label = qw.QLabel("Name:")
        name_label.setAlignment(qc.Qt.AlignRight)
        name_label.setMinimumWidth(100)
        name_label.setMaximumWidth(100)
        self.name_line_edit = qw.QLineEdit()
        self.name_line_edit.setMinimumWidth(180)
        self.name_line_edit.setMaximumWidth(180)
        name_label_and_line_edit_layout.addWidget(name_label)
        name_label_and_line_edit_layout.addWidget(self.name_line_edit)

        # --------------------------------------------------------------------------------------------------------------
        # validator/ 名前の先頭に数字を付けられなくする
        reg_ex = qc.QRegExp("^(?!^\\d)[/a-zA-Z_\\d]+")
        text_validator = qg.QRegExpValidator(reg_ex, self.name_line_edit)
        self.name_line_edit.setValidator(text_validator)

        # --------------------------------------------------------------------------------------------------------------
        # LineEdit / ik controller creator用のテキストとlineEditを作成してwidgetに追加
        num_of_controls_label = qw.QLabel("num of controls:")
        num_of_controls_label.setAlignment(qc.Qt.AlignRight)
        num_of_controls_label.setMinimumWidth(100)
        num_of_controls_label.setMaximumWidth(100)
        self.num_of_controls_combo = qw.QComboBox()
        [self.num_of_controls_combo.addItem(i) for i in ('3', '4', '5')]
        self.num_of_controls_combo.setCurrentIndex(0)
        self.num_of_controls_combo.setMinimumWidth(60)
        self.num_of_controls_combo.setMaximumWidth(60)
        controller_picker_layout.addWidget(num_of_controls_label)
        controller_picker_layout.addWidget(self.num_of_controls_combo)

        # --------------------------------------------------------------------------------------------------------------
        # Create buttonの作成
        self.create_button = qw.QPushButton('Create')
        create_button_layout.addWidget(self.create_button)
        self.create_button.clicked.connect(self.create_ik_controller_and_picker_widget)

        # todo : あとでGUIのリフレッシュ機能を追加予定
        # self.reload_button = qw.QPushButton("Reload")
        # self.reload_button.setMaximumWidth(70)
        # create_button_layout.addWidget(self.reload_button)
        # self.reload_button.clicked.connect(self.reload_instant_ik_widget)

        # --------------------------------------------------------------------------------------------------------------
        # instant ik widget 用レイアウト
        self.instant_ik_widget_layout = qw.QVBoxLayout()
        self.instant_ik_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.instant_ik_widget_layout.setSpacing(0)
        self.instant_ik_widget_layout.setAlignment(qc.Qt.AlignTop)
        main_widget_layout.addLayout(self.instant_ik_widget_layout)

        # --------------------------------------------------------------------------------------------------------------
        self.instant_ik_controller = ""

        # --------------------------------------------------------------------------------------------------------------
        self._interp_widget = []
        self._dock_widget = self._dock_name = None

    def reload_instant_ik_widget(self):
        obj = pm.ls(type="implicitSphere")
        if obj:
            attrs = pm.getAttr(obj[0] + ".user_defined_attrs")
            jsn = json.loads(attrs)
            name = str(jsn["name"])
            ik_controls = list(jsn["ik_ctrl"])
            ik_handles = str(jsn["ik_handle"])

            print(name, ik_controls, ik_handles)
            print(type(name), type(ik_controls), type(ik_handles))

            self.add_instant_ik_widget(ik_controls=ik_controls, ik_handles=ik_handles, name=name)
            self.create_button.setEnabled(False)
            self.num_of_controls_combo.setEnabled(False)
            self.name_line_edit.setEnabled(False)

    def find_the_implicit_sphere(self):
        pass

    def create_ik_controller_and_picker_widget(self, **kwargs):
        if self.name_line_edit.text() == "":
            pm.confirmDialog(title="Error", message="Please set Name.")
            return

        if 3 > len(pm.ls(sl=True)):
            pm.confirmDialog(title="Error", message="Please select at least three objects.")
            return

        if int(self.num_of_controls_combo.currentText()) > len(pm.ls(sl=True)):
            pm.confirmDialog(title="Error",
                             message="The number of controllers should be less than you have selected.")
            return

        # --------------------------------------------------------------------------------------------------------------
        self.instant_ik_controller = InstantIkController(name_line_edit=self.name_line_edit,
                                                         num_of_controls=self.num_of_controls_combo.currentText())
        self.instant_ik_controller.run_create()

        # --------------------------------------------------------------------------------------------------------------
        # create picker widget
        ik_controls = self.instant_ik_controller.ik_controls
        ik_controls = [obj.name() for obj in ik_controls]
        ik_handles = self.instant_ik_controller.spline_ik_handle

        self.add_instant_ik_widget(ik_controls=ik_controls, ik_handles=ik_handles, name=self.name_line_edit.text())
        self.create_button.setEnabled(False)
        self.num_of_controls_combo.setEnabled(False)
        self.name_line_edit.setEnabled(False)

    def add_instant_ik_widget(self, ik_controls, ik_handles, name):
        new_widget = InstantIkWidget(ik_controls, ik_handles, name)
        self.instant_ik_widget_layout.addWidget(new_widget)
        self._interp_widget.append(new_widget)
        new_widget.bake_button.clicked.connect(partial(self.bake_fk_and_remove_instant_ik_widget, new_widget))
        new_widget.delete_and_close.clicked.connect(partial(self.remove_instant_ik_controller_and_widget, new_widget))
        self.setMinimumHeight(350)

    def enable_create_button(self):
        self.create_button.setEnabled(True)
        self.num_of_controls_combo.setEnabled(True)
        self.name_line_edit.setEnabled(True)

    def bake_fk_controls(self):
        self.instant_ik_controller.bake_target(self.instant_ik_controller.selected_object)

    def delete_instant_ik_controller(self):
        pm.delete(self.instant_ik_controller.constraint_to_be_delete_later)
        pm.delete(self.instant_ik_controller.root_group)

    def bake_fk_and_remove_instant_ik_widget(self, interp_widget):
        self.bake_fk_controls()
        self.remove_instant_ik_controller_and_widget(interp_widget)

    def remove_instant_ik_controller_and_widget(self, interp_widget):
        self.delete_instant_ik_controller()
        if interp_widget in self._interp_widget:
            self._interp_widget.remove(interp_widget)
            self.instant_ik_widget_layout.removeWidget(interp_widget)
        interp_widget.deleteLater()
        self.enable_create_button()

    # def delete(self, instant_widget):
    #     self.instant_ik_layout.removeWidget(instant_widget)
    #     instant_widget.deleteLater()

    # def clear_all(self, *args):
    #     for instant_widget in self._instant_widget:
    #         instant_widget.crearItems()

    # def connect_dock_widget(self, dock_name, dock_widget):
    #     self._dock_widget = dock_widget
    #     self._dock_name = dock_name
    #
    # def close(self):
    #     if self._dock_widget:
    #         pm.deleteUI(self._dock_name)
    #     else:
    #         qw.QDialog.close(self)
    #     self._dock_widget = self._dock_name = None


class InstantIkController(object):
    def __init__(self, name_line_edit, num_of_controls):
        self.name_line_edit = name_line_edit
        self.num_of_controls = int(num_of_controls)

        # --------------------------------------------------------------------------------------------------------------
        self.selected_object = pm.ls(sl=True)
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
        self.ik_controls = []
        self.clusters_attached_to_curve_cv = []
        self.cluster_group = []
        self.dummy_spline_crv = []
        self.spline_crv = []
        self.spline_ik_handle = []
        self.instance_loc = []
        self.instance_attr_shape = []
        self.ik_controller_scale = []
        self.constraint_to_be_delete_later = []

    @undo_pm
    def run_create(self):
        self.create_hierarchy_to_receive_fk_movements()
        self.create_spline_ik()
        self.create_ik_controller()
        self.create_root_group()
        self.add_attribute_to_implicit_sphere()
        self.group_all(self.spline_crv,
                       self.dummy_spline_crv,
                       self.clusters_attached_to_curve_cv,
                       self.spline_ik_handle,
                       self.fk_group_space,
                       self.ik_joints_space[0])

    def group_all(self, *args):
        [pm.parent(x, self.root_group[0]) for x in args]

    def add_attribute_to_implicit_sphere(self):
        objs = []
        for obj in self.ik_controls:
            objs.append(obj.name())
        pm.addAttr(self.implicit_sphere, shortName="ud_attrs", longName="user_defined_attrs", dt="string")
        # poses = []
        dicts = {}
        dicts.update(name=self.name_line_edit.text())
        dicts.update(ik_ctrl=objs)
        dicts.update(ik_handle=self.spline_ik_handle[0].name())
        # poses.append(dicts)
        jsn = json.dumps(dicts)
        print(jsn)
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
        del_list = []
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
            del_list.append(pm.parentConstraint(obj[i], locator))

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
                del_list.append(pm.parentConstraint(parent_of_the_selected_object_space, fk_group_space))
                del_list.append(pm.parentConstraint(parent_of_the_selected_object, receive_fk_grp))
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

        # --------------------------------------------------------------------------------------------------------------
        pm.refresh(su=True)
        pm.makeIdentity(self.ik_joints, apply=True, t=True, r=True, s=True)
        target_of_bake = (self.locator + self.fk_group_space + self.root_group + self.fk_group)
        self.bake_target(target_of_bake)
        pm.refresh(su=False)
        pm.delete(del_list)

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

    def _connect_to_fk(self):
        for src, trg in self.ik_joint_and_selected_object.items():
            self.constraint_to_be_delete_later.append(pm.orientConstraint(src, trg, mo=True))

    def _connect_to_ik(self):
        pm.parentConstraint(self.locator[0], self.ik_joints_space[0], mo=True)

    def create_root_group(self):
        grp = pm.createNode("implicitSphere", n="instant_ik_{}_grp_shape".format(self.name_line_edit.text()))
        prt = pm.listRelatives(grp, p=True)
        pm.rename(prt, "instant_ik_{}_grp".format(self.name_line_edit.text()))
        pm.select(prt)
        pm.addAttr(shortName='loc_scale', longName='locator_scale', defaultValue=1.0, k=True, h=False)
        self.root_group.append(prt[0])
        self.implicit_sphere.append(grp)
        self.lock_and_hide_attr(self.root_group, attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"])

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
                ik_control = self.create_controller_shapes('{}_spline_{}_ctrl'.format(self.name_line_edit.text(), i),
                                                           cv_pos)
                pm.makeIdentity(ik_control, apply=1, t=1, r=1, s=1, n=0)
                pm.connectAttr(ik_control + ".tx", cv_cluster + ".tx")
                pm.connectAttr(ik_control + ".ty", cv_cluster + ".ty")
                pm.connectAttr(ik_control + ".tz", cv_cluster + ".tz")
                pm.hide(cv_cluster)
                pm.parent(ik_control, grp)
                self.ik_controls.append(ik_control)
            pm.hide(cv_cluster)

        self.create_instance_shape(attrs=["twist", "roll"])
        self.rebuild_curve()
        self.bind_spline_curve()
        self.connect_attrs_from_instance_shape()
        self.parent_an_instance_shape_to_ik_controller()
        self.parent_cluster()
        self._connect_to_fk()
        self._connect_to_ik()
        self.lock_and_hide_attr(self.ik_controls, attrs=["rx", "ry", "rz", "sx", "sy", "sz", "v", "ihi"])

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

    def create_instance_shape(self, attrs):
        loc = pm.spaceLocator(n=self.name_line_edit.text() + "_org_loc")
        shape = pm.listRelatives(loc, s=True)[0]
        shape = pm.rename(shape, "{}_duplicate_shape".format(self.name_line_edit.text()))
        [pm.addAttr(shape, longName=attr, at='float', defaultValue=0.0, k=True) for attr in attrs]
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

    def connect_attrs_from_instance_shape(self):
        pm.connectAttr(self.instance_attr_shape[0] + ".twist", self.spline_ik_handle[0] + ".twi", f=True)
        pm.connectAttr(self.instance_attr_shape[0] + ".roll", self.spline_ik_handle[0] + ".rol", f=True)

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
        self.setMinimumHeight(200)
        self.rubberBand = None
        self.origin = None
        self.ik_handles = ik_handles
        self.ik_buttons = []
        self.name = name

        title_layout = qw.QHBoxLayout()
        ik_layout = qw.QHBoxLayout()
        twist_layout = qw.QHBoxLayout()
        roll_layout = qw.QHBoxLayout()
        bake_layout = qw.QHBoxLayout()

        ik_layout.setAlignment(qc.Qt.AlignLeft)
        ik_layout.setContentsMargins(0, 40, 25, 40)
        ik_layout.setSpacing(20)

        layouts = [title_layout,
                   ik_layout,
                   SplitterLayout(),
                   twist_layout,
                   roll_layout,
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

        self.twist_sb = custom_spinbox.CustomSpinBox(custom_spinbox.CustomSpinBox.double_spinbox)
        self.roll_sb = custom_spinbox.CustomSpinBox(custom_spinbox.CustomSpinBox.double_spinbox)
        self.twist_lb = label.CustomLabel("Twist: ")
        self.roll_lb = label.CustomLabel("Roll: ")
        self.key_twist = qw.QPushButton("Key")
        self.key_roll = qw.QPushButton("Key")
        self.key_twist.setMaximumWidth(50)
        self.key_roll.setMaximumWidth(50)
        self.twist_lb.setAlignment(qc.Qt.AlignRight)
        self.roll_lb.setAlignment(qc.Qt.AlignRight)

        [twist_layout.addWidget(x) for x in [self.twist_lb, self.twist_sb, self.key_twist]]
        twist_layout.setAlignment(qc.Qt.AlignLeft)
        twist_layout.setContentsMargins(0, 5, 0, 5)
        twist_layout.setSpacing(5)

        roll_layout.addWidget(self.roll_lb)
        roll_layout.addWidget(self.roll_sb)
        roll_layout.addWidget(self.key_roll)

        [roll_layout.addWidget(x) for x in [self.roll_lb, self.roll_sb, self.key_roll]]
        roll_layout.setContentsMargins(0, 5, 0, 5)
        roll_layout.setSpacing(5)
        roll_layout.setAlignment(qc.Qt.AlignLeft)

        self.bake_button = qw.QPushButton("Bake and Close")
        bake_layout.setContentsMargins(5, 10, 5, 10)
        bake_layout.setSpacing(5)
        bake_layout.addWidget(self.bake_button)

        self.delete_and_close = qw.QPushButton("Close")
        bake_layout.addWidget(self.delete_and_close)

        ik_num = len(ik_controls)
        for btn in range(ik_num):
            ik_button = button.DTButton()
            ik_button.setObjectName(ik_controls[btn])
            ik_button.setCheckable(True)
            ik_layout.addWidget(ik_button)
            self.ik_buttons.append(ik_button)

        self._connect()
        self.add_callback()
        # self.connect_callback()

    def _connect(self):
        [btn.clicked.connect(self.callback) for btn in self.ik_buttons]
        self.twist_sb.textChanged.connect(partial(self.set_value, "twist"))
        self.roll_sb.textChanged.connect(partial(self.set_value, "roll"))
        self.key_twist.clicked.connect(partial(self.add_keys, "twist"))
        self.key_roll.clicked.connect(partial(self.add_keys, "roll"))

    @undo_pm
    def add_keys(self, *args):
        pm.setKeyframe("{}_duplicate_shape.{}".format(self.name, args[0]))

    @undo_pm
    def set_value(self, *args):
        pm.setAttr("{}_duplicate_shape.{}".format(self.name, args[0]), float(args[1]))

    # duplicate shapeを格納
    # attribute changed callbackを定義
    # objのattributeが変わったらself.cbを実行する
    # self.cbとはノードのメッセージを判定して、処理を実行するメソッド
    @undo_pm
    def add_callback(self):
        sph = "{}_duplicate_shape".format(self.name)
        sel = om.MSelectionList()
        sel.add(sph)
        obj = sel.getDependNode(0)
        if self.id:
            try:
                om.MMessage.removeCallback(id)
            except:
                pass
        if self.callback_id:
            try:
                om.MMessage.removeCallback(self.callback_id)
            except:
                pass
        # addAttributeChangedCallback(node, function, clientData=None) -> id
        self.id = om.MNodeMessage.addAttributeChangedCallback(obj, self.cb)

    @undo_pm
    def cb(self, msg, plug, other_plug, data):
        if msg & om.MNodeMessage.kAttributeSet and plug.name() == '{}_duplicate_shape.twist'.format(self.name):
            self.twist_sb.setText(str(round(plug.asFloat(), 3)))

        elif msg & om.MNodeMessage.kAttributeSet and plug.name() == '{}_duplicate_shape.roll'.format(self.name):
            self.roll_sb.setText(str(round(plug.asFloat(), 3)))

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
        # shiftが押されていた場合
        if modifiers == qc.Qt.ShiftModifier:
            print('Shift+Click')
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
            print('Click')
            getBtn = self.findChildren(qw.QPushButton)
            for i in getBtn:
                if i.isChecked():
                    i.click()

            selected = []
            rect = self.rubberBand.geometry()
            for child in self.findChildren(qw.QPushButton):
                if rect.intersects(child.geometry()):
                    selected.append(child)

            for j in selected:
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
        dialog.show(dockable=True)
    else:
        dialog.show()


def delete():
    global dialog
    if dialog is None:
        return

    dialog.deleteLater()
    dialog = None
