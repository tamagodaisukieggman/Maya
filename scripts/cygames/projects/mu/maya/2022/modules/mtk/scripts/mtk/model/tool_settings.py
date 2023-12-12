# -*- coding: utf-8 -*-

from functools import partial

import maya.api.OpenMaya as om2
import maya.cmds as cmds
import maya.mel


class ToolSettings(object):
    def __init__(self):
        self.NAME = "_tool_settingsUI"
        self.TITLE = u"Tool Settings"

        self.snap_options = [u"オフ",u"相対",u"絶対"]
        
        self.select_const_options = [
                                    u"オフ",
                                    u"角度",
                                    u"境界",
                                    u"エッジループ",
                                    u"エッジリング",
                                    u"シェル",
                                    u"UV エッジループ",
                                    u"UV シェル"
                                    ]

        self.axis_mode = [
                            u"オブジェクト",
                            u"ワールド",
                            u"コンポーネント",
                            u"ペアレント",
                            u"法線",
                            u"回転軸",
                            u"ライブ軸",
                            u"カスタム"
                            ]

        self.axis_mode_rot = [
                            u"オブジェクト",
                            u"ワールド",
                            u"ジンバル",
                            u"カスタム",
                            u"コンポーネント"
                            ]

        self.axis_dict = {
                            0:u"オブジェクト",
                            1:u"ペアレント",
                            2:u"ワールド",
                            3:u"法線",
                            4:u"回転軸",
                            5:u"ライブ軸",
                            6:u"カスタム",
                            10:u"コンポーネント"
                            }

        self.axis_rot_dict = {
                            0:u"オブジェクト",
                            1:u"ワールド",
                            2:u"ジンバル",
                            3:u"カスタム",
                            10:u"コンポーネント"
                            }

        self.sym_mode = [u"オフ",
                        u"オブジェクトX",
                        u"オブジェクトY",
                        u"オブジェクトZ",
                        u"ワールドX",
                        u"ワールドY",
                        u"ワールドZ"]

        self.select_axis = ["+Y","-Y","+X","-X","+Z","-Z"]

        self._axis_menu_name = "{}_axis_menu".format(self.NAME)
        self._symmetry_menu_name = "{}_symmetry_menu".format(self.NAME)
        self._snap_menu_name = "{}_snap_menu".format(self.NAME)
        self._snap_float_field_name = "{}_snap_float_field".format(self.NAME)
        self._snap_components_relative_ck_name = "{}_snap_components_relative_ck".format(self.NAME)

        self._selection_constraint_menu_name = "{}_selection_constraint_menu".format(self.NAME)
        self._selection_constraint_float_field_name = "{}_selection_constraint_float_field".format(self.NAME)

        self._select_axis_poly_menu_name = "{}_select_axis_poly_menu".format(self.NAME)
        self._select_axis_poly_float_field_name = "{}_select_axis_poly_float_field".format(self.NAME)
        self._select_axis_poly_btn_name = "{}_select_axis_poly_btn".format(self.NAME)

        self._preseve_uv_ck_name = "{}_preseve_uv_ck".format(self.NAME)
        self._camera_base_selection_ck_name = "{}_camera_base_selection_ck".format(self.NAME)

        self._x_float_field_name = "{}_x_float_field".format(self.NAME)
        self._y_float_field_name = "{}_y_float_field".format(self.NAME)
        self._z_float_field_name = "{}_z_float_field".format(self.NAME)

        self._all_axis_btn_name = "{}_all_axis_btn".format(self.NAME)
        self._x_ck_name = "{}_x_ck".format(self.NAME)
        self._y_ck_name = "{}_y_ck".format(self.NAME)
        self._z_ck_name = "{}_z_ck".format(self.NAME)

        self._absolute_icon_ck_name = "{}_absolute_icon_ck".format(self.NAME)
        self._plus_minus_rd_name = "{}_plus_minus_rd".format(self.NAME)
        self._value_zero_btn_name = "{}_value_zero_btn".format(self.NAME)
        self._value_one_btn_name = "{}_value_one_btn".format(self.NAME)
        self._value_ten_btn_name = "{}_value_ten_btn".format(self.NAME)
        self._value_mil_btn_name = "{}_value_mil_btn".format(self.NAME)

        self._add_selection_ck_name = "{}_add_selection_ck".format(self.NAME)

        self._move_btn_labels = ["1","5","10","100"]
        self._rotate_btn_labels = ["5","10","45","90"]
        self._scale_btn_labels = ["0.5","1.25","1.5","2"]

        self.bb_size = None

        self.bb_center = None

    def create(self, *args):
        try:
            cmds.deleteUI(self.NAME)
        except:pass
        
        _separator_height = 10
        _check_box_height = 25

        cmds.window(self.NAME, title=self.TITLE, width=50, height=50)
        cmds.columnLayout(adjustableColumn=True)
        cmds.text(l=u"トランスフォーム", align="center", backgroundColor=[0.1,0.1,0.1])
        cmds.button(u"コンポーネントのトランスフォーム", command=partial(self._move_poly_compornent), height=15)
        #cmds.separator(height=_separator_height)
        cmds.rowLayout(numberOfColumns=2, columnWidth2=[100,100])

        cmds.optionMenu(self._axis_menu_name, label=u"軸", changeCommand=partial(self.set_axis), width=105)
        self._axis_menus = [cmds.menuItem(label=x) for x in self.axis_mode]

        cmds.optionMenu(self._symmetry_menu_name, label=u"sym", changeCommand=partial(self.set_sym), width=105)
        [cmds.menuItem(label=x) for x in self.sym_mode]
        cmds.setParent("..")
        cmds.separator(height=_separator_height)
        cmds.button(self._all_axis_btn_name, l=u"全軸アクティブ", width=200, height=15, command=partial(self._change_axis_icon_ck,"all"))
        cmds.rowLayout(numberOfColumns=6, columnWidth6=[20,50,10,50,10,50])
        cmds.iconTextCheckBox(self._x_ck_name,
                                style='textOnly',
                                label=u"X:",
                                value=True,
                                align="center",
                                highlightColor=[0.5,0.2,0.2],
                                changeCommand=partial(self._change_axis_icon_ck,"x"),
                                width=20)
        cmds.floatField(self._x_float_field_name,
                                    width=50,
                                    value=0.0,
                                    precision=3,
                                    enterCommand=partial(self._apply_translations,"x"))
        cmds.iconTextCheckBox(self._y_ck_name,
                                style='textOnly',
                                label=u"Y:",
                                value=True,
                                align="center",
                                highlightColor=[0.2,0.5,0.2],
                                changeCommand=partial(self._change_axis_icon_ck,"y"),
                                width=20)
        cmds.floatField(self._y_float_field_name,
                                    width=50,
                                    value=0.0,
                                    precision=3,
                                    enterCommand=partial(self._apply_translations,"y"))
        cmds.iconTextCheckBox(self._z_ck_name,
                                style='textOnly',
                                label=u"Z:",
                                value=True,
                                align="center",
                                highlightColor=[0.2,0.2,0.5],
                                changeCommand=partial(self._change_axis_icon_ck,"z"),
                                width=20)
        cmds.floatField(self._z_float_field_name,
                                    width=50,
                                    value=0.0,
                                    precision=3,
                                    enterCommand=partial(self._apply_translations,"z"))

        
        cmds.setParent("..")
        
        cmds.rowLayout(numberOfColumns=5, columnWidth5=[80,33,33,33,33])
        # cmds.iconTextCheckBox(self._absolute_icon_ck_name, label=u"絶対値", style='textOnly', width=40, backgroundColor=[0.2,0.2,0.2])

        cmds.radioButtonGrp(self._plus_minus_rd_name, numberOfRadioButtons=2,
                            select=1,label1=u"＋",label2=u"－",columnWidth2=[30,15],
                            backgroundColor=[0.4,0.2,0.2],
                            changeCommand=partial(self._change_plus_minus_rd))
        cmds.button(self._value_zero_btn_name,
                label=u"0", width=33, command=partial(self._apply_translations_btn,self._value_zero_btn_name))
        cmds.button(self._value_one_btn_name,
                label=u"1", width=33, command=partial(self._apply_translations_btn,self._value_one_btn_name))
        cmds.button(self._value_ten_btn_name,
                label=u"10", width=33, command=partial(self._apply_translations_btn,self._value_ten_btn_name))
        cmds.button(self._value_mil_btn_name,
                label=u"100", width=33, command=partial(self._apply_translations_btn,self._value_mil_btn_name))
        cmds.setParent("..")
        # cmds.separator(height=_separator_height)
        cmds.text(l=u"スナップ", align="center", backgroundColor=[0.1,0.1,0.1])
        cmds.rowLayout(numberOfColumns=3, columnWidth3=[50,50,50],
                            # backgroundColor=[0.3,0.35,0.37]
                            )
        cmds.optionMenu(self._snap_menu_name,
                            changeCommand=partial(self.set_snap), width=90)
        [cmds.menuItem(label=x) for x in self.snap_options]

        cmds.floatField(self._snap_float_field_name,
                                    width=50,
                                    value=0.0,
                                    precision=1,
                                    enterCommand=partial(self.set_snap),
                                    changeCommand=partial(self.set_snap),
                                    minValue=0.0)

        cmds.checkBox(self._snap_components_relative_ck_name, label=u"間隔維持", value=True,
                            changeCommand=partial(self.set_comp))
        cmds.setParent("..")

        # cmds.separator(height=_separator_height)
        cmds.text(l=u"選択コンストレイント", align="center", backgroundColor=[0.1,0.1,0.1])

        # cmds.separator(height=_separator_height)
        cmds.rowLayout(numberOfColumns=2, columnWidth2=[120,90]
                            # backgroundColor=[0.35,0.25,0.25]
                            )
        cmds.optionMenu(self._selection_constraint_menu_name,
                        width=120,
                        changeCommand=partial(self._change_select_constraint))

        [cmds.menuItem( label=x ) for x in self.select_const_options]
        cmds.floatField(self._selection_constraint_float_field_name,
                                    width=90,
                                    value=30.0,
                                    precision=1,
                                    enterCommand=partial(self._change_select_constraint_angle),
                                    minValue=0.0)

        cmds.setParent("..")
        cmds.text(l=u"ポリゴン選択", align="center", backgroundColor=[0.1,0.1,0.1])
        cmds.rowLayout(numberOfColumns=4, columnWidth4=[60,40,50,65])
        cmds.optionMenu(self._select_axis_poly_menu_name, width=60)
        [cmds.menuItem( label=x ) for x in self.select_axis]
        cmds.floatField(self._select_axis_poly_float_field_name,
                                    width=40,
                                    value=30.0,
                                    precision=1,
                                    minValue=0.0)
        cmds.button(self._select_axis_poly_btn_name,
                        label=u"選択", width=50, command=partial(self.select_yup))
        cmds.iconTextCheckBox(self._add_selection_ck_name,
                            label=u"追加選択", style='textOnly', align="center", width=65)
        cmds.setParent("..")
        cmds.separator(height=_separator_height)
        cmds.rowLayout(numberOfColumns=5, columnWidth5=[42,42,42,42,42])
        cmds.button(label="-10", command=partial(self._float_value_preset,-10), width=42)
        cmds.button(label="-5", command=partial(self._float_value_preset,-5), width=42)
        cmds.button(label="0", command=partial(self._float_value_preset, 0), width=42,
                        backgroundColor=[0.2,0.2,0.2])
        cmds.button(label="+5", command=partial(self._float_value_preset,5), width=42)
        cmds.button(label="+10", command=partial(self._float_value_preset,10), width=42)
        cmds.setParent("..")

        cmds.text(l=u"オプション", align="center", backgroundColor=[0.1,0.1,0.1])

        cmds.rowLayout(numberOfColumns=2, columnWidth2=[100,100])
        cmds.checkBox(self._preseve_uv_ck_name, label=u"UVを保持",
                        value=True,
                        changeCommand=partial(self._chenge_preseve_uv))

        cmds.checkBox(self._camera_base_selection_ck_name, label=u"カメラベース選択",
                        value=True,
                        changeCommand=partial(self._chenge_camera_base_selection))

        
        cmds.setParent("..")
        cmds.setParent("..")
        cmds.setParent("..")
        cmds.showWindow(self.NAME)
        self.get_setting()

        cmds.scriptJob(parent=self.NAME, event=["ToolChanged", partial(self.get_setting)])
        cmds.scriptJob(parent=self.NAME, event=["selectionConstraintsChanged", partial(self.get_setting)])
        cmds.scriptJob(parent=self.NAME, event=["SelectionChanged", partial(self.get_setting)])

    def _change_plus_minus_rd(self, *args):
        _select = cmds.radioButtonGrp(self._plus_minus_rd_name, q=True, select=True)
        if _select == 1:
            cmds.radioButtonGrp(self._plus_minus_rd_name, e=True, backgroundColor=[0.4,0.2,0.2])
        else:
            cmds.radioButtonGrp(self._plus_minus_rd_name, e=True, backgroundColor=[0.2,0.2,0.4])

    def _move_poly_compornent(self, *args):
        try:
            maya.mel.eval('MovePolygonComponent;')
        except:pass

    def _apply_translations_btn(self, _name, *args):
        current_tool = cmds.currentCtx()
        if current_tool == "moveSuperContext":
            self._apply_translations_btn_trans(_name)
        else:
            self._apply_translations_btn_rotate_scale(_name)


    def _apply_translations_btn_trans(self, _name, *args):

        _value = float(cmds.button(_name,q=True,label=True))
        current_tool = cmds.currentCtx()
        _plus_minus_flag = cmds.radioButtonGrp(self._plus_minus_rd_name, q=True, select=True)
        
        if _plus_minus_flag == 2:
            _value = _value * -1
        
        axis = cmds.optionMenu(self._axis_menu_name, q=True, value=True)
        if current_tool == "RotateSuperContext":
            if axis in self.axis_rot_dict.values():
                axis = [k for k,v in self.axis_rot_dict.items() if v == axis][0]
            else:
                axis = 0
        else:
            axis = [k for k,v in self.axis_dict.items() if v == axis][0]

        _x = cmds.iconTextCheckBox(self._x_ck_name, q=True, value=True)
        _y = cmds.iconTextCheckBox(self._y_ck_name, q=True, value=True)
        _z = cmds.iconTextCheckBox(self._z_ck_name, q=True, value=True)

        _component_flag = cmds.selectMode(q=True, component=True)

        if current_tool == "moveSuperContext":
            if axis == 1:
                if _x:
                    cmds.move(_value,0,0, localSpace=True, relative=True, worldSpaceDistance=True)
                if _y:
                    cmds.move(0,_value,0, localSpace=True, relative=True, worldSpaceDistance=True)
                if _z:
                    cmds.move(0,0,_value, localSpace=True, relative=True, worldSpaceDistance=True)
            elif axis == 0:
                if _x:
                    cmds.move(_value,0,0, objectSpace=True, relative=True, worldSpaceDistance=True)
                if _y:
                    cmds.move(0,_value,0, objectSpace=True, relative=True, worldSpaceDistance=True)
                if _z:
                    cmds.move(0,0,_value, objectSpace=True, relative=True, worldSpaceDistance=True)
            elif axis == 10:
                if _x:
                    
                    cmds.move(_value,0,0, componentSpace=True, localSpace=True, relative=True, worldSpaceDistance=True)
                if _y:
                    cmds.move(0,_value,0, componentSpace=True, localSpace=True, relative=True, worldSpaceDistance=True)
                if _z:
                    cmds.move(0,0,_value, componentSpace=True, localSpace=True, relative=True, worldSpaceDistance=True)

            else:
                if _x:
                    cmds.move(_value,0,0, worldSpace=True, relative=True)
                if _y:
                    cmds.move(0,_value,0, worldSpace=True, relative=True)
                if _z:
                    cmds.move(0,0,_value, worldSpace=True, relative=True)


        elif current_tool == "RotateSuperContext":
            if not self.bb_center:
                return
            if _component_flag:
                if axis == 1:
                    if _x:
                        cmds.rotate(_value,0,0, relative=True, worldSpace=True, pivot=self.bb_center, forceOrderXYZ=True)
                    if _y:
                        cmds.rotate(0,_value,0, relative=True, worldSpace=True, pivot=self.bb_center, forceOrderXYZ=True)
                    if _z:
                        cmds.rotate(0,0,_value, relative=True, worldSpace=True, pivot=self.bb_center, forceOrderXYZ=True)
                else:
                    if _x:
                        cmds.rotate(_value,0,0, relative=True, objectSpace=True, pivot=self.bb_center, forceOrderXYZ=True)
                    if _y:
                        cmds.rotate(0,_value,0, relative=True, objectSpace=True, pivot=self.bb_center, forceOrderXYZ=True)
                    if _z:
                        cmds.rotate(0,0,_value, relative=True, objectSpace=True, pivot=self.bb_center, forceOrderXYZ=True)
            else:
                if axis == 1:
                    if _x:
                        cmds.rotate(_value,0,0, relative=True, worldSpace=True, forceOrderXYZ=True)
                    if _y:
                        cmds.rotate(0,_value,0, relative=True, worldSpace=True, forceOrderXYZ=True)
                    if _z:
                        cmds.rotate(0,0,_value, relative=True, worldSpace=True, forceOrderXYZ=True)
                else:
                    if _x:
                        cmds.rotate(_value,0,0, relative=True, objectSpace=True, forceOrderXYZ=True)
                    if _y:
                        cmds.rotate(0,_value,0, relative=True, objectSpace=True, forceOrderXYZ=True)
                    if _z:
                        cmds.rotate(0,0,_value, relative=True, objectSpace=True, forceOrderXYZ=True)


        elif current_tool == "scaleSuperContext":
            if not self.bb_center:
                return
            if _component_flag:
                if axis == 2:
                    if _x:
                        cmds.scale(_value,1,1, relative=True, worldSpace=True, pivot=self.bb_center)
                    if _y:
                        cmds.scale(1,_value,1, relative=True, worldSpace=True, pivot=self.bb_center)
                    if _z:
                        cmds.scale(1,1,_value, relative=True, worldSpace=True, pivot=self.bb_center)
                else:
                    if _x:
                        cmds.scale(_value,1,1, relative=True, pivot=self.bb_center)
                    if _y:
                        cmds.scale(1,_value,1, relative=True, pivot=self.bb_center)
                    if _z:
                        cmds.scale(1,1,_value, relative=True, pivot=self.bb_center)
            else:
                if axis == 2:
                    if _x:
                        cmds.scale(_value,1,1, relative=True, worldSpace=True)
                    if _y:
                        cmds.scale(1,_value,1, relative=True, worldSpace=True)
                    if _z:
                        cmds.scale(1,1,_value, relative=True, worldSpace=True)
                else:
                    if _x:
                        cmds.scale(_value,1,1, relative=True)
                    if _y:
                        cmds.scale(1,_value,1, relative=True)
                    if _z:
                        cmds.scale(1,1,_value, relative=True)

        self._get_current_selections()

    def _apply_translations_btn_rotate_scale(self, _name, *args):

        _value = float(cmds.button(_name,q=True,label=True))
        current_tool = cmds.currentCtx()
        _plus_minus_flag = cmds.radioButtonGrp(self._plus_minus_rd_name, q=True, select=True)
        
        if _plus_minus_flag == 2:
            _value = _value * -1

        _values = [0.0,0.0,0.0]
        _x = cmds.iconTextCheckBox(self._x_ck_name, q=True, value=True)
        _y = cmds.iconTextCheckBox(self._y_ck_name, q=True, value=True)
        _z = cmds.iconTextCheckBox(self._z_ck_name, q=True, value=True)
        if current_tool == "scaleSuperContext":
            if _x and _y and _z:
                _values = [_value,_value,_value]
            elif _x and _y:
                _values = [_value,_value,1.0]
            elif _x and _z:
                _values = [_value,1.0,_value]
            elif _y and _z:
                _values = [1.0,_value,_value]
            elif _x:
                _values = [_value,1.0,1.0]
            elif _y:
                _values = [1.0,_value,1.0]
            elif _z:
                _values = [1.0,1.0,_value]

        else:
            if _x and _y and _z:
                _values = [_value,_value,_value]
            elif _x and _y:
                _values = [_value,_value,0.0]
            elif _x and _z:
                _values = [_value,0.0,_value]
            elif _y and _z:
                _values = [0.0,_value,_value]
            elif _x:
                _values = [_value,0.0,0.0]
            elif _y:
                _values = [0.0,_value,0.0]
            elif _z:
                _values = [0.0,0.0,_value]
        
        if current_tool == "moveSuperContext":
            cmds.manipMoveContext("Move", e=True, translate=_values)
        elif current_tool == "RotateSuperContext":
            cmds.manipRotateContext("Rotate", e=True, rotate=_values)
        elif current_tool == "scaleSuperContext":
            cmds.manipScaleContext("Scale", e=True, scale=_values)

        self._get_current_selections()

    def _apply_translations(self, _axis, *args):
        current_tool = cmds.currentCtx()
        if current_tool == "moveSuperContext":
            self._apply_translations_trans(_axis)
        else:
            self._apply_translations_rotate_scale(_axis)


    def _apply_translations_rotate_scale(self, _axis, *args):
        current_tool = cmds.currentCtx()
        axis = cmds.optionMenu(self._axis_menu_name, q=True, value=True)
        if current_tool == "RotateSuperContext":
            if axis in self.axis_rot_dict.values():
                axis = [k for k,v in self.axis_rot_dict.items() if v == axis][0]
            else:
                axis = 0
        else:
            axis = [k for k,v in self.axis_dict.items() if v == axis][0]

        if _axis == "x":
            _value = cmds.floatField(self._x_float_field_name, q=True, value=True)
        elif _axis == "y":
            _value = cmds.floatField(self._y_float_field_name, q=True, value=True)
        else:
            _value = cmds.floatField(self._z_float_field_name, q=True, value=True)
        
        if current_tool == "moveSuperContext":
            if _axis == "x":
                cmds.manipMoveContext("Move", e=True, translate=[_value,0,0])
            elif _axis == "y":
                cmds.manipMoveContext("Move", e=True, translate=[0,_value,0])
            elif _axis == "z":
                cmds.manipMoveContext("Move", e=True, translate=[0,0,_value])
        elif current_tool == "RotateSuperContext":
            if _axis == "x":
                cmds.manipRotateContext("Rotate", e=True, rotate=[_value,0,0])
            elif _axis == "y":
                cmds.manipRotateContext("Rotate", e=True, rotate=[0,_value,0])
            elif _axis == "z":
                cmds.manipRotateContext("Rotate", e=True, rotate=[0,0,_value])
        elif current_tool == "scaleSuperContext":
            if _axis == "x":
                cmds.manipScaleContext("Scale", e=True, scale=[_value,1,1])
            elif _axis == "y":
                cmds.manipScaleContext("Scale", e=True, scale=[1,_value,1])
            elif _axis == "z":
                cmds.manipScaleContext("Scale", e=True, scale=[1,1,_value])
        self._get_current_selections()


    def _apply_translations_trans(self, _axis, *args):
        current_tool = cmds.currentCtx()
        axis = cmds.optionMenu(self._axis_menu_name, q=True, value=True)
        if current_tool == "RotateSuperContext":
            if axis in self.axis_rot_dict.values():
                axis = [k for k,v in self.axis_rot_dict.items() if v == axis][0]
            else:
                axis = 0
        else:
            axis = [k for k,v in self.axis_dict.items() if v == axis][0]

        if _axis == "x":
            _value = cmds.floatField(self._x_float_field_name, q=True, value=True)
        elif _axis == "y":
            _value = cmds.floatField(self._y_float_field_name, q=True, value=True)
        else:
            _value = cmds.floatField(self._z_float_field_name, q=True, value=True)
        _component_flag = cmds.selectMode(q=True, component=True)

        if current_tool == "moveSuperContext":
            if axis == 1:
                if _axis == "x":
                    cmds.move(_value,0,0, localSpace=True, relative=True, worldSpaceDistance=True)
                elif _axis == "y":
                    cmds.move(0,_value,0, localSpace=True, relative=True, worldSpaceDistance=True)
                elif _axis == "z":
                    cmds.move(0,0,_value, localSpace=True, relative=True, worldSpaceDistance=True)
            elif axis == 0:
                if _axis == "x":
                    cmds.move(_value,0,0, objectSpace=True, relative=True, worldSpaceDistance=True)
                elif _axis == "y":
                    cmds.move(0,_value,0, objectSpace=True, relative=True, worldSpaceDistance=True)
                elif _axis == "z":
                    cmds.move(0,0,_value, objectSpace=True, relative=True, worldSpaceDistance=True)
            elif axis == 10:
                if _axis == "x":
                    cmds.move(_value,0,0, componentSpace=True, localSpace=True, relative=True, worldSpaceDistance=True)
                elif _axis == "y":
                    cmds.move(0,_value,0, componentSpace=True, localSpace=True, relative=True, worldSpaceDistance=True)
                elif _axis == "z":
                    cmds.move(0,0,_value, componentSpace=True, localSpace=True, relative=True, worldSpaceDistance=True)

            else:
                if _axis == "x":
                    cmds.move(_value,0,0, worldSpace=True, relative=True)
                elif _axis == "y":
                    cmds.move(0,_value,0, worldSpace=True, relative=True)
                elif _axis == "z":
                    cmds.move(0,0,_value, worldSpace=True, relative=True)
        
        elif current_tool == "RotateSuperContext":

            if _component_flag:
                if not self.bb_center:
                    return
                if axis == 2:
                    if _axis == "x":
                        cmds.rotate(_value,0,0, relative=True, euler=True, pivot=self.bb_center, forceOrderXYZ=True)
                    elif _axis == "y":
                        cmds.rotate(0,_value,0, relative=True, euler=True, pivot=self.bb_center, forceOrderXYZ=True)
                    elif _axis == "z":
                        cmds.rotate(0,0,_value, relative=True, euler=True, pivot=self.bb_center, forceOrderXYZ=True)
                if axis == 10:
                    if _axis == "x":
                        cmds.rotate(_value,0,0, relative=True, componentSpace=True, worldSpace=True, pivot=self.bb_center, forceOrderXYZ=True)
                    elif _axis == "y":
                        cmds.rotate(0,_value,0, relative=True, componentSpace=True, worldSpace=True, pivot=self.bb_center, forceOrderXYZ=True)
                    elif _axis == "z":
                        cmds.rotate(0,0,_value, relative=True, componentSpace=True, worldSpace=True, pivot=self.bb_center, forceOrderXYZ=True)

                else:
                    if _axis == "x":
                        cmds.rotate(_value,0,0, relative=True, objectSpace=True, pivot=self.bb_center, forceOrderXYZ=True)
                    elif _axis == "y":
                        cmds.rotate(0,_value,0, relative=True, objectSpace=True, pivot=self.bb_center, forceOrderXYZ=True)
                    elif _axis == "z":
                        cmds.rotate(0,0,_value, relative=True, objectSpace=True, pivot=self.bb_center, forceOrderXYZ=True)
            else:
                if axis == 2:
                    if _axis == "x":
                        cmds.rotate(_value,0,0, relative=True, euler=True, forceOrderXYZ=True)
                    elif _axis == "y":
                        cmds.rotate(0,_value,0, relative=True, euler=True, forceOrderXYZ=True)
                    elif _axis == "z":
                        cmds.rotate(0,0,_value, relative=True, euler=True, forceOrderXYZ=True)
                if axis == 10:
                    if _axis == "x":
                        cmds.rotate(_value,0,0, relative=True, componentSpace=True, worldSpace=True, forceOrderXYZ=True)
                    elif _axis == "y":
                        cmds.rotate(0,_value,0, relative=True, componentSpace=True, worldSpace=True, forceOrderXYZ=True)
                    elif _axis == "z":
                        cmds.rotate(0,0,_value, relative=True, componentSpace=True, worldSpace=True, forceOrderXYZ=True)

                else:
                    if _axis == "x":
                        cmds.rotate(_value,0,0, relative=True, objectSpace=True, forceOrderXYZ=True)
                    elif _axis == "y":
                        cmds.rotate(0,_value,0, relative=True, objectSpace=True, forceOrderXYZ=True)
                    elif _axis == "z":
                        cmds.rotate(0,0,_value, relative=True, objectSpace=True, forceOrderXYZ=True)

        elif current_tool == "scaleSuperContext":
            if _component_flag:
                if not self.bb_center:
                    return
                if axis == 2:
                    if _axis == "x":
                        cmds.scale(_value,1,1, relative=True, worldSpace=True, pivot=self.bb_center)
                    elif _axis == "y":
                        cmds.scale(1,_value,1, relative=True, worldSpace=True, pivot=self.bb_center)
                    elif _axis == "z":
                        cmds.scale(1,1,_value, relative=True, worldSpace=True, pivot=self.bb_center)
                else:
                    if _axis == "x":
                        cmds.scale(_value,1,1, relative=True, pivot=self.bb_center)
                    elif _axis == "y":
                        cmds.scale(1,_value,1, relative=True, pivot=self.bb_center)
                    elif _axis == "z":
                        cmds.scale(1,1,_value, relative=True, pivot=self.bb_center)
            else:
                if axis == 2:
                    if _axis == "x":
                        cmds.scale(_value,1,1, relative=True, worldSpace=True)
                    elif _axis == "y":
                        cmds.scale(1,_value,1, relative=True, worldSpace=True)
                    elif _axis == "z":
                        cmds.scale(1,1,_value, relative=True, worldSpace=True)
                else:
                    if _axis == "x":
                        cmds.scale(_value,1,1, relative=True)
                    elif _axis == "y":
                        cmds.scale(1,_value,1, relative=True)
                    elif _axis == "z":
                        cmds.scale(1,1,_value, relative=True)


    def _get_current_selections(self):
        _selection = cmds.ls(selection=True)
        
        if not _selection:
            return
        current_tool = cmds.currentCtx()

        self._get_bounding_box(_selection)
        if current_tool == "RotateSuperContext":
            self._get_rotation()
        elif current_tool == "scaleSuperContext":
            cmds.floatField(self._x_float_field_name, e=True, value=1.0)
            cmds.floatField(self._y_float_field_name, e=True, value=1.0)
            cmds.floatField(self._z_float_field_name, e=True, value=1.0)
        
    def _bounding_box_size(self, _selection):
        bb_size = cmds.polyEvaluate(_selection, boundingBoxComponent=True, accurateEvaluation=True)

        _bb_not_polygonal_flag = False

        # float[]	xmin、ymin、zmin、xmax、ymax、zmax
        if bb_size == "Nothing counted : no polygonal object is selected.":
            bb_size = cmds.exactWorldBoundingBox(_selection, calculateExactly=True)
            _bb_not_polygonal_flag = True

        # ((xmin,xmax),(ymin,ymax),(zmin,zmax))
        if str(bb_size) == "((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))":
            bb_size = cmds.polyEvaluate(_selection, boundingBox=True, accurateEvaluation=True)
        
        if _bb_not_polygonal_flag:
            bb_size = [[bb_size[0],bb_size[3]],
                        [bb_size[1],bb_size[4]],
                        [bb_size[2],bb_size[5]]]
        return bb_size

    def _bounding_box_center(self, bb_size):
        return [(bb_size[0][0] + bb_size[0][1]) / 2,
                (bb_size[1][0] + bb_size[1][1]) / 2,
                ((bb_size[2][0] + bb_size[2][1]) / 2)]

    def _get_bounding_box(self, _selection):
        bb_size = self._bounding_box_size(_selection)
        self.bb_size = bb_size

        bb_center = self._bounding_box_center(bb_size)
        self.bb_center = bb_center

        cmds.floatField(self._x_float_field_name, e=True, value=round(bb_center[0],3))
        cmds.floatField(self._y_float_field_name, e=True, value=round(bb_center[1],3))
        cmds.floatField(self._z_float_field_name, e=True, value=round(bb_center[2],3))


    def _change_edit_axis(self, _x, _y, _z):
        _axis = 0
        if _x and _y and _z:
            _axis = 3
        elif _x and _y:
            _axis = 4
        elif _y and _z:
            _axis = 5
        elif _x and _z:
            _axis = 6
        elif _x:
            _axis = 0
        elif _y:
            _axis = 1
        elif _z:
            _axis = 2
        current_tool = cmds.currentCtx()
        if current_tool == "moveSuperContext":
            cmds.manipMoveContext("Move", e=True, currentActiveHandle=_axis)
        elif current_tool == "RotateSuperContext":
            cmds.manipRotateContext("Rotate", e=True, currentActiveHandle=_axis)
        elif current_tool == "scaleSuperContext":
            cmds.manipScaleContext("Scale", e=True, currentActiveHandle=_axis)

    def _change_axis_icon_ck(self, axis, *args):
        _mod = cmds.getModifiers()
        _x = cmds.iconTextCheckBox(self._x_ck_name, q=True, value=True)
        _y = cmds.iconTextCheckBox(self._y_ck_name, q=True, value=True)
        _z = cmds.iconTextCheckBox(self._z_ck_name, q=True, value=True)
        
        if axis == "all":
            cmds.iconTextCheckBox(self._x_ck_name, e=True, value=True)
            cmds.iconTextCheckBox(self._y_ck_name, e=True, value=True)
            cmds.iconTextCheckBox(self._z_ck_name, e=True, value=True)
        elif axis == "x":
            if _mod == 4:
                cmds.iconTextCheckBox(self._x_ck_name, e=True, value=_x)
            else:
                cmds.iconTextCheckBox(self._x_ck_name, e=True, value=True)
            if _mod == 4 and _y:
                cmds.iconTextCheckBox(self._y_ck_name, e=True, value=True)
            else:
                cmds.iconTextCheckBox(self._y_ck_name, e=True, value=False)
            if _mod == 4 and _z:
                cmds.iconTextCheckBox(self._z_ck_name, e=True, value=True)
            else:
                cmds.iconTextCheckBox(self._z_ck_name, e=True, value=False)
            if not _x and not _y and not _z:
                cmds.iconTextCheckBox(self._x_ck_name, e=True, value=True)
        elif axis == "y":
            if _mod == 4 and _x:
                cmds.iconTextCheckBox(self._x_ck_name, e=True, value=True)
            else:
                cmds.iconTextCheckBox(self._x_ck_name, e=True, value=False)
            if _mod == 4:
                cmds.iconTextCheckBox(self._y_ck_name, e=True, value=_y)
            else:
                cmds.iconTextCheckBox(self._y_ck_name, e=True, value=True)
            if _mod == 4 and _z:
                cmds.iconTextCheckBox(self._z_ck_name, e=True, value=True)
            else:
                cmds.iconTextCheckBox(self._z_ck_name, e=True, value=False)
            if not _x and not _y and not _z:
                cmds.iconTextCheckBox(self._y_ck_name, e=True, value=True)
        elif axis == "z":
            if _mod == 4 and _x:
                cmds.iconTextCheckBox(self._x_ck_name, e=True, value=True)
            else:
                cmds.iconTextCheckBox(self._x_ck_name, e=True, value=False)
            if _mod ==4 and _y:
                cmds.iconTextCheckBox(self._y_ck_name, e=True, value=True)
            else:
                cmds.iconTextCheckBox(self._y_ck_name, e=True, value=False)
            if _mod == 4:
                cmds.iconTextCheckBox(self._z_ck_name, e=True, value=_z)
            else:
                cmds.iconTextCheckBox(self._z_ck_name, e=True, value=True)
            if not _x and not _y and not _z:
                cmds.iconTextCheckBox(self._z_ck_name, e=True, value=True)
        _x = cmds.iconTextCheckBox(self._x_ck_name, q=True, value=True)
        _y = cmds.iconTextCheckBox(self._y_ck_name, q=True, value=True)
        _z = cmds.iconTextCheckBox(self._z_ck_name, q=True, value=True)
        self._change_edit_axis(_x, _y, _z)


    def _float_value_preset(self, value, *args):
        # _angle1 = cmds.floatField(self._selection_constraint_float_field_name, q=True, value=True)
        _angle2 = cmds.floatField(self._select_axis_poly_float_field_name, q=True, value=True)
        # _value = cmds.floatField(self._snap_float_field_name, q=True, value=True)
        if value != 0:
            # _angle1 = _angle1 + value
            _angle2 = _angle2 + value
            # if _angle1 < 0.0:
            #     _angle1 = 0.0
            # _angle2 = _angle2 + value
            # _value =_value + value
        else:
            # _angle1 = 0.0
            _angle2 = 0.0
            # _value =0.0
        # cmds.floatField(self._selection_constraint_float_field_name, e=True, value=_angle1)
        cmds.floatField(self._select_axis_poly_float_field_name, e=True, value=_angle2)
        # cmds.floatField(self._snap_float_field_name, e=True, value=_value)
        self._change_select_constraint_angle()
        # self.set_snap()

    def _change_select_constraint_angle(self, *args):
        _value = cmds.floatField(self._selection_constraint_float_field_name,
                                q=True, value=True)
        
        cmds.polySelectConstraint(border=False,
                                borderPropagation=False,
                                shell=False,
                                crease=False,
                                angleTolerance=_value)

    def _change_select_constraint(self, *args):
        _select = cmds.optionMenu(self._selection_constraint_menu_name, q=True, select=True)
        _select = _select - 1
        _angle_flag = False
        if cmds.selectType(q=True, meshUVShell=True):
            cmds.selectType(polymeshFace=True)
        if _select == 0:
            cmds.selectMode(component=True)
            cmds.polySelectConstraint(border=False,
                                        crease=False,
                                        borderPropagation=False,
                                        anglePropagation=False,
                                        loopPropagation=False,
                                        ringPropagation=False,
                                        shell=False,
                                        uvEdgeLoopPropagation=False,
                                        uvShell=False)
        elif _select == 1:
            cmds.selectMode(component=True)
            cmds.polySelectConstraint(border=False,
                                        crease=False,
                                        borderPropagation=False,
                                        anglePropagation=True,
                                        loopPropagation=False,
                                        ringPropagation=False,
                                        shell=False,
                                        uvEdgeLoopPropagation=False,
                                        uvShell=False)
            _angle_flag = True
        elif _select == 2:
            cmds.selectMode(component=True)
            cmds.selectType(subdivMeshPoint=False,
                            subdivMeshEdge=True,
                            subdivMeshFace=False,
                            subdivMeshUV=False,
                            polymeshVertex=False,
                            polymeshEdge=True,
                            polymeshFace=False,
                            polymeshUV=False)
            cmds.polySelectConstraint(border=True,
                                        crease=False,
                                        borderPropagation=True,
                                        anglePropagation=False,
                                        loopPropagation=False,
                                        ringPropagation=False,
                                        shell=False,
                                        uvEdgeLoopPropagation=False,
                                        uvShell=False)
        elif _select == 3:
            cmds.selectMode(component=True)
            cmds.selectType(subdivMeshPoint=False,
                            subdivMeshEdge=True,
                            subdivMeshFace=False,
                            subdivMeshUV=False,
                            polymeshVertex=False,
                            polymeshEdge=True,
                            polymeshFace=False,
                            polymeshUV=False)
            cmds.polySelectConstraint(border=False,
                                        crease=False,
                                        borderPropagation=False,
                                        anglePropagation=False,
                                        loopPropagation=True,
                                        ringPropagation=False,
                                        shell=False,
                                        uvEdgeLoopPropagation=False,
                                        uvShell=False)
        elif _select == 4:
            cmds.selectMode(component=True)
            cmds.selectType(subdivMeshPoint=False,
                            subdivMeshEdge=True,
                            subdivMeshFace=False,
                            subdivMeshUV=False,
                            polymeshVertex=False,
                            polymeshEdge=True,
                            polymeshFace=False,
                            polymeshUV=False)
            cmds.polySelectConstraint(border=False,
                                        crease=False,
                                        borderPropagation=False,
                                        anglePropagation=False,
                                        loopPropagation=False,
                                        ringPropagation=True,
                                        shell=False,
                                        uvEdgeLoopPropagation=False,
                                        uvShell=False)

        if _select == 5:
            cmds.selectMode(component=True)
            cmds.polySelectConstraint(border=False,
                                        crease=False,
                                        borderPropagation=False,
                                        anglePropagation=False,
                                        loopPropagation=False,
                                        ringPropagation=False,
                                        shell=True,
                                        uvEdgeLoopPropagation=False,
                                        uvShell=False)
            
        if _select == 6:
            cmds.selectMode(component=True)
            cmds.selectType(subdivMeshPoint=False,
                            subdivMeshEdge=True,
                            subdivMeshFace=False,
                            subdivMeshUV=False,
                            polymeshVertex=False,
                            polymeshEdge=True,
                            polymeshFace=False,
                            polymeshUV=False)
            cmds.polySelectConstraint(border=False,
                                        crease=False,
                                        borderPropagation=False,
                                        anglePropagation=False,
                                        loopPropagation=False,
                                        ringPropagation=False,
                                        shell=False,
                                        uvEdgeLoopPropagation=True,
                                        uvShell=False)

        if _select == 7:
            cmds.selectMode(component=True)
            # cmds.polySelectConstraint(border=False,
            #                             crease=False,
            #                             borderPropagation=False,
            #                             anglePropagation=False,
            #                             loopPropagation=False,
            #                             ringPropagation=False,
            #                             shell=False,
            #                             uvEdgeLoopPropagation=False,
            #                             uvShell=True)
            cmds.selectType(meshUVShell=True, polymeshEdge=False, polymeshFace=False, polymeshUV=False, polymeshVertex=False)
        if _angle_flag:
            cmds.floatField(self._selection_constraint_float_field_name,
                            e=True, enable=True)
        else:
            cmds.floatField(self._selection_constraint_float_field_name,
                            e=True, enable=False)


    def _chenge_preseve_uv(self, *args):
        value = cmds.checkBox(self._preseve_uv_ck_name, q=True, value=True)
        current_tool = cmds.currentCtx()
        if current_tool == "moveSuperContext":
            cmds.manipMoveContext("Move", e=True, preserveUV=value)
        elif current_tool == "RotateSuperContext":
            cmds.manipRotateContext("Rotate", e=True, preserveUV=value)
        elif current_tool == "scaleSuperContext":
            cmds.manipScaleContext("Scale", e=True, preserveUV=value)

    def _chenge_camera_base_selection(self, *args):
        _flag = cmds.selectPref(q=True, useDepth=True)
        cmds.selectPref(useDepth=not _flag)
        # cmds.selectPref(paintSelectWithDepth=not _flag)
        cmds.checkBox(self._camera_base_selection_ck_name, e=True, value=not _flag)

    def get_axis_range(self, *args):
        _axis = cmds.optionMenu(self._select_axis_poly_menu_name,
                                         q=True,
                                         select=True)
        _axis = self.select_axis[_axis - 1]
        axis = om2.MVector(0,1,0)
        if _axis == "+X":
            axis = om2.MVector(1,0,0)
        elif _axis == "-X":
            axis = om2.MVector(-1,0,0)
        # elif _axis == "+Y":
        #     axis = om2.MVector(0,1,0)
        elif _axis == "-Y":
            axis = om2.MVector(0,-1,0)
        elif _axis == "+Z":
            axis = om2.MVector(0,0,1)
        elif _axis == "-Z":
            axis = om2.MVector(0,0,-1)

        _range = cmds.floatField(self._select_axis_poly_float_field_name,
                                        q=True, value=True)
        return axis,_range

    def select_yup(self, *args):
        _add_select_flag = cmds.iconTextCheckBox(self._add_selection_ck_name, q=True, value=True)
        if not _add_select_flag and cmds.selectMode(q=True, component=True):
            self._get_meshfn_component()
        else:
            if not self._get_meshfn():
                return
        
        axis,_range = self.get_axis_range()

        self._polys = []
        for mesh_fn,dag_path in zip(self._mesh_fns,self._dag_paths):
            _ids = []
            # matrix = om2.MFloatMatrix(dag_path.inclusiveMatrixInverse())
            if self._component and mesh_fn in self._component:
                for _type, _component in self._component[mesh_fn].items():
                    for i in _component.getElements():
                        _vec = mesh_fn.getPolygonNormal(i, space=om2.MSpace.kWorld)
                        _ang = om2.MAngle(_vec.angle(axis))
                        if _ang.asDegrees() < _range:
                            _ids.append(i)
            else:
                for i in range(mesh_fn.numPolygons):
                    _vec = mesh_fn.getPolygonNormal(i, space=om2.MSpace.kWorld)
                    _ang = om2.MAngle(_vec.angle(axis))
                    if _ang.asDegrees() < _range:
                        _ids.append(i)
            if _ids:
                self._polys.extend(["{}.f[{}]".format(mesh_fn.fullPathName(), x) for x in _ids])
        
        
        if _add_select_flag:
            cmds.select(self._polys, add=True)
        else:
            cmds.selectMode(component=True)
            cmds.selectType(smp=False, sme=False, smf=True,
                            smu=False, pv=False, pe=False, pf=True, puv=False)
            cmds.select(cl=True)
            if self._polys:
                cmds.select(self._polys, replace=True)


    def _clear_memory(self, *args):
        self._mesh_fns = []
        self._dag_paths = []
        self._component = {}

    def _get_selections(self, *args):
        _selections = cmds.ls(sl=True, type="transform")
        if not _selections:
            _selections = cmds.ls(hilite=True)
        _meshes = []
        for _selecion in _selections:
            _mesh = cmds.listRelatives(_selecion, allDescendents=True, fullPath=True, type="mesh")
            if _mesh:
                _meshes.extend(_mesh)
        return _meshes

    def _get_selections_component(self, *args):
        _selections = cmds.ls(sl=True, long=True, flatten=True)
        
        if not _selections:
            cmds.warning(u"選択が見つかりませんでした")
            return 0
        return 1

    def _get_meshfn_component(self, *args):
        self._clear_memory()
        if not self._get_selections_component():
            return
        selList = om2.MGlobal.getActiveSelectionList()

        selObj = {}
        for x in range(selList.length()):
            try:
                dag_path,mCmp = selList.getComponent(x)
            except:continue

            if dag_path.hasFn(om2.MFn.kMesh):
                _mesh_fns = om2.MFnMesh(dag_path)
                selId = {}
                cmpType = None
                self._dag_paths.append(dag_path)
                self._mesh_fns.append(_mesh_fns)
                # if mCmp.hasFn(om2.MFn.kMeshVertComponent):
                #     cmpType = "vtx"
                # elif mCmp.hasFn(om2.MFn.kMeshEdgeComponent):
                #     cmpType = "edge"
                if mCmp.hasFn(om2.MFn.kMeshPolygonComponent):
                    cmpType = "face"

                if cmpType:
                    selId[cmpType] = om2.MFnSingleIndexedComponent(mCmp)

                self._component[_mesh_fns] = selId


    def _get_meshfn(self, *args):
        self._clear_memory()
        
        _selections = self._get_selections()
        if not _selections:
            cmds.warning(u"メッシュを持った[ トランスフォームノード ]を選択してください")
            return 0

        sel_list = om2.MSelectionList()
        [sel_list.add(x) for x in _selections]
        
        for i in range(sel_list.length()):
            dag_path = sel_list.getDagPath(i)
            if dag_path.hasFn(om2.MFn.kMesh):
                self._dag_paths.append(dag_path)
                self._mesh_fns.append(om2.MFnMesh(dag_path))
        return 1

    def get_setting(self, *args):
        _tansration_flag = False
        current_tool = cmds.currentCtx()
        uv_setting = 0
        snap_setting = 0
        snap_option = 0
        snap_value = 0
        snap_comonents_relative = 1
        axis = 0
        current_axis = 0
        select_constraint = 0
        if current_tool == "moveSuperContext":
            _tansration_flag = True
            uv_setting = cmds.manipMoveContext("Move", q=True, preserveUV=True)
            snap_setting = cmds.manipMoveContext("Move", q=True, snap=True)
            snap_value = cmds.manipMoveContext("Move", q=True, snapValue=True)
            snap_option = cmds.manipMoveContext("Move", q=True, snapRelative=True)
            snap_comonents_relative = cmds.manipMoveContext("Move", q=True, snapComponentsRelative=True)

            [cmds.deleteUI(x) for x in self._axis_menus]
            self._axis_menus = [cmds.menuItem(parent=self._axis_menu_name,label=x) for x in self.axis_mode]

            axis = cmds.manipMoveContext("Move", q=True, mode=True)
            axis_name = self.axis_dict[axis]
            axis = self.axis_mode.index(axis_name) + 1
            current_axis = cmds.manipMoveContext("Move", q=True, currentActiveHandle=True)
            cmds.floatField(self._x_float_field_name, e=True, value=0.0)
            cmds.floatField(self._y_float_field_name, e=True, value=0.0)
            cmds.floatField(self._z_float_field_name, e=True, value=0.0)

            cmds.button(self._value_zero_btn_name, e=True, label=self._move_btn_labels[0])
            cmds.button(self._value_one_btn_name, e=True, label=self._move_btn_labels[1])
            cmds.button(self._value_ten_btn_name, e=True, label=self._move_btn_labels[2])
            cmds.button(self._value_mil_btn_name, e=True, label=self._move_btn_labels[3])

        elif current_tool == "RotateSuperContext":
            _tansration_flag = True
            uv_setting = cmds.manipRotateContext("Rotate", q=True, preserveUV=True)
            snap_setting = cmds.manipRotateContext("Rotate", q=True, snap=True)
            snap_option = cmds.manipRotateContext("Rotate", q=True, snapRelative=True)
            snap_value = cmds.manipRotateContext("Rotate", q=True, snapValue=True)
            [cmds.deleteUI(x) for x in self._axis_menus]
            self._axis_menus = [cmds.menuItem(parent=self._axis_menu_name,label=x) for x in self.axis_mode_rot]

            # snap_comonents_relative = cmds.manipRotateContext("Rotate", q=True, snapComponentsRelative=True)
            axis = cmds.manipRotateContext("Rotate", q=True, mode=True)
            axis_name = self.axis_rot_dict[axis]
            axis = self.axis_mode_rot.index(axis_name) + 1
            current_axis = cmds.manipRotateContext("Rotate", q=True, currentActiveHandle=True)

            cmds.button(self._value_zero_btn_name, e=True, label=self._rotate_btn_labels[0])
            cmds.button(self._value_one_btn_name, e=True, label=self._rotate_btn_labels[1])
            cmds.button(self._value_ten_btn_name, e=True, label=self._rotate_btn_labels[2])
            cmds.button(self._value_mil_btn_name, e=True, label=self._rotate_btn_labels[3])

            self._get_rotation()

        elif current_tool == "scaleSuperContext":
            _tansration_flag = True
            uv_setting = cmds.manipScaleContext("Scale", q=True, preserveUV=True)
            snap_setting = cmds.manipScaleContext("Scale", q=True, snap=True)
            snap_option = cmds.manipScaleContext("Scale", q=True, snapRelative=True)
            snap_value = cmds.manipScaleContext("Scale", q=True, snapValue=True)

            [cmds.deleteUI(x) for x in self._axis_menus]
            self._axis_menus = [cmds.menuItem(parent=self._axis_menu_name,label=x) for x in self.axis_mode]

            # snap_comonents_relative = cmds.manipScaleContext("Scale", q=True, snapComponentsRelative=True)
            axis = cmds.manipScaleContext("Scale", q=True, mode=True)
            axis_name = self.axis_dict[axis]
            axis = self.axis_mode.index(axis_name) + 1
            current_axis = cmds.manipScaleContext("Scale", q=True, currentActiveHandle=True)
            cmds.floatField(self._x_float_field_name, e=True, value=1.0)
            cmds.floatField(self._y_float_field_name, e=True, value=1.0)
            cmds.floatField(self._z_float_field_name, e=True, value=1.0)

            cmds.button(self._value_zero_btn_name, e=True, label=self._scale_btn_labels[0])
            cmds.button(self._value_one_btn_name, e=True, label=self._scale_btn_labels[1])
            cmds.button(self._value_ten_btn_name, e=True, label=self._scale_btn_labels[2])
            cmds.button(self._value_mil_btn_name, e=True, label=self._scale_btn_labels[3])
        
        if not _tansration_flag:
        # if current_tool == "selectSuperContext":
            cmds.optionMenu(self._axis_menu_name, e=True, enable=False)
            cmds.optionMenu(self._symmetry_menu_name, e=True, enable=False)
            cmds.optionMenu(self._snap_menu_name, e=True, enable=False)
            cmds.floatField(self._snap_float_field_name, e=True, enable=False)
            cmds.checkBox(self._snap_components_relative_ck_name, e=True, enable=False)
            cmds.checkBox(self._preseve_uv_ck_name, e=True, enable=False)
            cmds.button(self._all_axis_btn_name, e=True, enable=False)
            cmds.iconTextCheckBox(self._x_ck_name, e=True, enable=False)
            cmds.floatField(self._x_float_field_name, e=True, enable=False)
            cmds.iconTextCheckBox(self._y_ck_name, e=True, enable=False)
            cmds.floatField(self._y_float_field_name, e=True, enable=False)
            cmds.iconTextCheckBox(self._z_ck_name, e=True, enable=False)
            cmds.floatField(self._z_float_field_name, e=True, enable=False)
            # cmds.iconTextCheckBox(self._absolute_icon_ck_name, e=True, enable=False)
            cmds.radioButtonGrp(self._plus_minus_rd_name, e=True, enable=False)
            cmds.button(self._value_zero_btn_name, e=True, enable=False)
            cmds.button(self._value_one_btn_name, e=True, enable=False)
            cmds.button(self._value_ten_btn_name, e=True, enable=False)
            cmds.button(self._value_mil_btn_name, e=True, enable=False)
        else:
            cmds.optionMenu(self._axis_menu_name, e=True, enable=True)
            cmds.optionMenu(self._axis_menu_name, e=True, select=axis)
            cmds.optionMenu(self._symmetry_menu_name, e=True, enable=True)

            cmds.optionMenu(self._snap_menu_name, e=True, enable=True)
            if snap_setting and not snap_option:
                cmds.optionMenu(self._snap_menu_name, e=True, select=3)
            elif snap_setting:
                cmds.optionMenu(self._snap_menu_name, e=True, select=2)
            else:
                cmds.optionMenu(self._snap_menu_name, e=True, select=1)
            cmds.floatField(self._snap_float_field_name, e=True, enable=True)
            cmds.floatField(self._snap_float_field_name, e=True, value=snap_value)
            cmds.checkBox(self._snap_components_relative_ck_name, e=True, enable=True)
            
            cmds.checkBox(self._snap_components_relative_ck_name, e=True, value=snap_comonents_relative)
            cmds.checkBox(self._preseve_uv_ck_name, e=True, enable=True)
            cmds.checkBox(self._preseve_uv_ck_name, e=True, value=uv_setting)

            cmds.button(self._all_axis_btn_name, e=True, enable=True)
            cmds.iconTextCheckBox(self._x_ck_name, e=True, enable=True)
            cmds.floatField(self._x_float_field_name, e=True, enable=True)
            cmds.iconTextCheckBox(self._y_ck_name, e=True, enable=True)
            cmds.floatField(self._y_float_field_name, e=True, enable=True)
            cmds.iconTextCheckBox(self._z_ck_name, e=True, enable=True)
            cmds.floatField(self._z_float_field_name, e=True, enable=True)
            # cmds.iconTextCheckBox(self._absolute_icon_ck_name, e=True, enable=True)

            # cmds.iconTextCheckBox(self._absolute_icon_ck_name, e=True, enable=True)
            cmds.radioButtonGrp(self._plus_minus_rd_name, e=True, enable=True)
            cmds.button(self._value_zero_btn_name, e=True, enable=True)
            cmds.button(self._value_one_btn_name, e=True, enable=True)
            cmds.button(self._value_ten_btn_name, e=True, enable=True)
            cmds.button(self._value_mil_btn_name, e=True, enable=True)


        _sym = cmds.symmetricModelling(q=True, symmetry=True)
        
        if _sym:
            space = cmds.symmetricModelling(q=True, about=True)
            sAxis = cmds.symmetricModelling(q=True, axis=True)
            if space == "object":
                if sAxis == "x":
                    cmds.optionMenu(self._symmetry_menu_name, e=True, select=2)
                elif sAxis == "y":
                    cmds.optionMenu(self._symmetry_menu_name, e=True, select=3)
                elif sAxis == "z":
                    cmds.optionMenu(self._symmetry_menu_name, e=True, select=4)
            elif space == "world":
                if sAxis == "x":
                    cmds.optionMenu(self._symmetry_menu_name, e=True, select=5)
                elif sAxis == "y":
                    cmds.optionMenu(self._symmetry_menu_name, e=True, select=6)
                elif sAxis == "z":
                    cmds.optionMenu(self._symmetry_menu_name, e=True, select=7)

        _camera_base_select_flag = cmds.selectPref(q=True, useDepth=True)
        cmds.checkBox(self._camera_base_selection_ck_name, e=True, value=_camera_base_select_flag)
        _angle_value = self._get_select_constraint_angle_value()

        self._get_select_constraint_setting(_angle_value)
        self._get_current_set_axis()
        self._get_current_selections()
    
    def _get_rotation(self, *args):
        _selection = cmds.ls(selection=True, transforms=True)
        if _selection:
            _rot = cmds.getAttr("{}.r".format(_selection[0]))[0]
            cmds.floatField(self._x_float_field_name, e=True, value=_rot[0])
            cmds.floatField(self._y_float_field_name, e=True, value=_rot[1])
            cmds.floatField(self._z_float_field_name, e=True, value=_rot[2])
        else:
            cmds.floatField(self._x_float_field_name, e=True, value=0.0)
            cmds.floatField(self._y_float_field_name, e=True, value=0.0)
            cmds.floatField(self._z_float_field_name, e=True, value=0.0)

    def _get_current_set_axis(self, *args):
        current_tool = cmds.currentCtx()
        _axis = 0
        if current_tool == "moveSuperContext":
            _axis = cmds.manipMoveContext("Move", q=True, currentActiveHandle=_axis)
        elif current_tool == "RotateSuperContext":
            _axis = cmds.manipRotateContext("Rotate", q=True, currentActiveHandle=_axis)
        elif current_tool == "scaleSuperContext":
            _axis = cmds.manipScaleContext("Scale", q=True, currentActiveHandle=_axis)
        else:
            return
        if _axis == 0:
            cmds.iconTextCheckBox(self._x_ck_name, e=True, value=True)
            cmds.iconTextCheckBox(self._y_ck_name, e=True, value=False)
            cmds.iconTextCheckBox(self._z_ck_name, e=True, value=False)
        elif _axis == 1:
            cmds.iconTextCheckBox(self._x_ck_name, e=True, value=False)
            cmds.iconTextCheckBox(self._y_ck_name, e=True, value=True)
            cmds.iconTextCheckBox(self._z_ck_name, e=True, value=False)
        elif _axis == 2:
            cmds.iconTextCheckBox(self._x_ck_name, e=True, value=False)
            cmds.iconTextCheckBox(self._y_ck_name, e=True, value=False)
            cmds.iconTextCheckBox(self._z_ck_name, e=True, value=True)
        elif _axis == 3:
            cmds.iconTextCheckBox(self._x_ck_name, e=True, value=True)
            cmds.iconTextCheckBox(self._y_ck_name, e=True, value=True)
            cmds.iconTextCheckBox(self._z_ck_name, e=True, value=True)
        elif _axis == 4:
            cmds.iconTextCheckBox(self._x_ck_name, e=True, value=True)
            cmds.iconTextCheckBox(self._y_ck_name, e=True, value=True)
            cmds.iconTextCheckBox(self._z_ck_name, e=True, value=False)
        elif _axis == 5:
            cmds.iconTextCheckBox(self._x_ck_name, e=True, value=False)
            cmds.iconTextCheckBox(self._y_ck_name, e=True, value=True)
            cmds.iconTextCheckBox(self._z_ck_name, e=True, value=True)
        elif _axis == 6:
            cmds.iconTextCheckBox(self._x_ck_name, e=True, value=True)
            cmds.iconTextCheckBox(self._y_ck_name, e=True, value=False)
            cmds.iconTextCheckBox(self._z_ck_name, e=True, value=True)


    def _get_select_constraint_setting(self, _angle_value, *args):
        _angle_flag = False
        _flag = 1
        if cmds.polySelectConstraint(q=True, anglePropagation=True):
            # Angle
            _flag = 2
            _select_constraint = self.select_const_options[1]
            _angle_flag = True
        elif cmds.polySelectConstraint(q=True, borderPropagation=True):
            # Border
            _flag = 3
            _select_constraint = self.select_const_options[2]
        elif cmds.polySelectConstraint(q=True, loopPropagation=True):
            # Edge Loop
            _flag = 4
            _select_constraint = self.select_const_options[3]
        elif cmds.polySelectConstraint(q=True, ringPropagation=True):
            # Edge Ring
            _flag = 5
            _select_constraint = self.select_const_options[4]
        elif cmds.polySelectConstraint(q=True, shell=True):
            # Shell
            _flag = 6
            _select_constraint = self.select_const_options[5]
        elif cmds.polySelectConstraint(q=True, uvEdgeLoopPropagation=True):
            # Edge Loop
            _flag = 7
            _select_constraint = self.select_const_options[6]
        else:
            # OFF
            _select_constraint = self.select_const_options[0]
        if cmds.selectType(q=True, meshUVShell=True):
            # UV Shell
            _flag = 8
            _select_constraint = self.select_const_options[7]
        # cmds.optionMenu(self._selection_constraint_menu_name, e=True,
        #                     select = self.select_const_options.index(_select_constraint) + 1)
        if _angle_flag:
            cmds.floatField(self._selection_constraint_float_field_name, e=True, enable=True)
        else:
            cmds.floatField(self._selection_constraint_float_field_name, e=True, enable=False)
        cmds.optionMenu(self._selection_constraint_menu_name, e=True, select=_flag)
        cmds.floatField(self._selection_constraint_float_field_name, e=True, value=_angle_value)


    def _get_select_constraint_angle_value(self, *args):
        _value = cmds.polySelectConstraint(q=True, angleTolerance=True)
        return _value

    def set_snap(self, *args):
        _select = cmds.optionMenu(self._snap_menu_name, q=True, select=True)
        _value = cmds.floatField(self._snap_float_field_name, q=True, value=True)
        _flag = False if _select == 1 else True
        _switch = False
        if _flag:
            _switch = True if _select == 2 else False
        current_tool = cmds.currentCtx()
        if current_tool == "moveSuperContext":
            cmds.manipMoveContext("Move", e=True, snap=_flag)
            cmds.manipMoveContext("Move", e=True, snapRelative=_switch)
            cmds.manipMoveContext("Move", e=True, snapValue=_value)
        elif current_tool == "RotateSuperContext":
            cmds.manipRotateContext("Rotate", e=True, snap=_flag)
            cmds.manipRotateContext("Rotate", e=True, snapRelative=_switch)
            cmds.manipRotateContext("Rotate", e=True, snapValue=_value)
        elif current_tool == "scaleSuperContext":
            cmds.manipScaleContext("Scale", e=True, snap=_flag)
            cmds.manipScaleContext("Scale", e=True, snapRelative=_switch)
            cmds.manipScaleContext("Scale", e=True, snapValue=_value)


    def set_comp(self, *args):
        _value = cmds.checkBox(self._snap_components_relative_ck_name, q=True, value=True)
        cmds.manipMoveContext("Move", e=True, snapComponentsRelative=_value)


    def set_axis(self, *args):
        axis = cmds.optionMenu(self._axis_menu_name, q=True, value=True)

        current_tool = cmds.currentCtx()
        if current_tool == "RotateSuperContext":
            axis = [k for k,v in self.axis_rot_dict.items() if v == axis][0]
        else:
            axis = [k for k,v in self.axis_dict.items() if v == axis][0]

        if current_tool == "moveSuperContext":
            cmds.manipMoveContext("Move", e=True, mode=axis)
        elif current_tool == "RotateSuperContext":
            cmds.manipRotateContext("Rotate", e=True, mode=axis)
        elif current_tool == "scaleSuperContext":
            cmds.manipScaleContext("Scale", e=True, mode=axis)

    def set_sym(self, *args):
        _select = cmds.optionMenu(self._symmetry_menu_name, q=True, select=True)
        if _select == 1:
            cmds.symmetricModelling(e=True, topoSymmetry=False, symmetry=False)
        elif _select == 2:
            cmds.symmetricModelling(e=True, about="object", axis="x", symmetry=True)
        elif _select == 3:
            cmds.symmetricModelling(e=True, about="object", axis="y", symmetry=True)
        elif _select == 4:
            cmds.symmetricModelling(e=True, about="object", axis="z", symmetry=True)
        elif _select == 5:
            cmds.symmetricModelling(e=True, about="world", axis="x", symmetry=True)
        elif _select == 6:
            cmds.symmetricModelling(e=True, about="world", axis="y", symmetry=True)
        elif _select == 7:
            cmds.symmetricModelling(e=True, about="world", axis="z", symmetry=True)


def main():
    _tools = ToolSettings()
    _tools.create()

