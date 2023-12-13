# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

from functools import partial

import maya.cmds as cmds
import maya.mel

def seach_mesh_node(_nodes):
    _mesh_type_flag = False
    for _obj in _nodes:
        if cmds.listRelatives(_obj, type="mesh"):
            _mesh_type_flag = True
    
    return _mesh_type_flag

class MeasuringPolyMesh(object):
    def __init__(self):
        self.TITLE = u"計測ツール"
        self.NAME = u"measuring_tool_ui"
        self._window_width = 280

        self._x_field_name = "measuring_x_float_field"
        self._y_field_name = "measuring_y_float_field"
        self._z_field_name = "measuring_z_float_field"
        self._length_field_name = "measuring_length_float_field"
        self._unit_menu_name = "measuring_unit_pop_menu"

        self._button_name_a = "measuring_btnA"
        self._button_name_b = "measuring_btnB"

        self._units = ["mm","cm","m","in","ft","yd"]
        self._unit_dict = {"mm":0.1,"cm":1.0,"m":100,"in":2.54,"ft":30.48,"yd":91.44}
        self._unit_mul = 100.0

        self._x_value = 0.0
        self._y_value = 0.0
        self._z_value = 0.0

        self._length = 0.0

        self.minPosition = [0.0, 0.0, 0.0]
        self.maxPosition = [0.0, 0.0, 0.0]

        self._component_flag = False

        self.distance_group_name = "_distance_group"
        self.distance_sp_name = "_start_point_distanceDimension"
        self.distance_ep_name = "_end_point_distanceDimension"

        self.distance_x_sp_name = "_start_point_x_distanceDimension"
        self.distance_x_ep_name = "_end_point_x_distanceDimension"
        self.distance_y_sp_name = "_start_point_y_distanceDimension"
        self.distance_y_ep_name = "_end_point_y_distanceDimension"
        self.distance_z_sp_name = "_start_point_z_distanceDimension"
        self.distance_z_ep_name = "_end_point_z_distanceDimension"

        self._loc_sp = ""
        self._loc_ep = ""

        self._loc_x_sp = ""
        self._loc_x_ep = ""
        self._loc_y_sp = ""
        self._loc_y_ep = ""
        self._loc_z_sp = ""
        self._loc_z_ep = ""

        # self._get_current_scene_data()

    def _get_current_scene_data(self):
        self._current_unit = cmds.currentUnit(q=True, linear=True)

    def _change_pref_unit(self):
        self._get_current_scene_data()

        cmds.optionMenu(self._unit_menu_name,
                        edit=True,
                        select=self._units.index(self._current_unit) + 1)

        self._unit_mul = 1.0 / self._unit_dict[self._current_unit]

        cmds.floatField(self._x_field_name, edit=True, value=self._x_value * self._unit_mul)
        cmds.floatField(self._y_field_name, edit=True, value=self._y_value * self._unit_mul)
        cmds.floatField(self._z_field_name, edit=True, value=self._z_value * self._unit_mul)

    def _change_unit(self):
        self._get_current_scene_data()

        _change_unit = cmds.optionMenu(self._unit_menu_name, q=True, select=True)

        self._unit_mul = 1.0 / self._unit_dict[self._units[_change_unit - 1]]
        
        cmds.floatField(self._x_field_name, edit=True, value=self._x_value * self._unit_mul)
        cmds.floatField(self._y_field_name, edit=True, value=self._y_value * self._unit_mul)
        cmds.floatField(self._z_field_name, edit=True, value=self._z_value * self._unit_mul)

        cmds.floatField(self._length_field_name, edit=True, value=self._length * self._unit_mul)


    def create(self):
        try:
            cmds.deleteUI(self.NAME)
        except:pass

        cmds.window(self.NAME, title=self.TITLE, width=self._window_width , height=50)
        cmds.columnLayout(adjustableColumn=True, width = self._window_width + 3, height=105)

        cmds.rowLayout(numberOfColumns=6, columnWidth6=[10, 80, 10, 80, 10, 80])
        cmds.text(label="X", width = 10)
        cmds.floatField(self._x_field_name, precision=6, width=80)
        cmds.text(label="Y", width = 10)
        cmds.floatField(self._y_field_name, precision=6, width=80)
        cmds.text(label="Z", width = 10)
        cmds.floatField(self._z_field_name, precision=6, width=80)
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2, columnWidth2=[50, self._window_width - 50])
        cmds.text(label="Length")
        cmds.floatField(self._length_field_name, precision=6, width=self._window_width - 50)
        cmds.setParent("..")

        cmds.separator(height=10)
        cmds.optionMenu(self._unit_menu_name, label="", width=100, changeCommand=partial(self._change_option_menu))
        [cmds.menuItem(label=x) for x in self._units]

        cmds.rowLayout(numberOfColumns=2, columnWidth2=[self._window_width / 2, self._window_width / 2])
        cmds.button(self._button_name_a,
                    label=u"ボックス Distance 作成",
                    width=self._window_width / 2,
                    height=25,
                    command=partial(self._make_distance_dimension_box))

        cmds.button(self._button_name_b,
                    label=u"Distance 作成",
                    width=self._window_width / 2,
                    height=25,
                    enable=False,
                    command=partial(self._make_distance_dimension))
        cmds.setParent("..")
        
        cmds.setParent("..")
        cmds.setParent("..")

        cmds.showWindow(self.NAME)

        self._change_pref_unit()
        self.measuring_selection()

        cmds.scriptJob(parent=self.NAME, event=["linearUnitChanged", partial(self._change_pref_unit)])
        cmds.scriptJob(parent=self.NAME, event=["SelectionChanged", partial(self.measuring_selection)])

    def measuring_selection(self):
        _selection = cmds.ls(selection=True)
        
        if not _selection:
            cmds.button(self._button_name_a, edit=True, enable=False)
            return
        else:
            cmds.button(self._button_name_a, edit=True, enable=True)
        
        self._get_bounding_box(_selection)
        
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

        bb_center = self._bounding_box_center(bb_size)
        self.bb_bottom = bb_size[1][0]

        self._x_value = abs(bb_size[0][1] - bb_size[0][0])
        self._y_value = abs(bb_size[1][1] - bb_size[1][0])
        self._z_value = abs(bb_size[2][1] - bb_size[2][0])

        self.bb_size = bb_size
        self.bb_center = bb_center

        if len(_selection) == 2:
            cmds.button(self._button_name_b, edit=True, enable=True)
            self._get_length_two_obj(_selection)
        else:
            cmds.button(self._button_name_b, edit=True, enable=False)
        self._change_unit()

    def _get_length_two_obj(self, _selection):
        self._length = 0.0

        if cmds.selectMode(q=True, component=True) and _selection[0].split(".")[-1][:3] == "vtx":
            self._length = self._get_component_length(_selection)
        else:
            self._length = self._get_obj_length(_selection)
        cmds.floatField(self._length_field_name, edit=True, value=self._length)
    
    def _get_obj_length(self, _selection):
        _obj_A = _selection[0]
        _obj_B = _selection[1]

        _obj_A_bb = self._bounding_box_size(_obj_A)
        _obj_B_bb = self._bounding_box_size(_obj_B)
        
        self.minPosition = self._bounding_box_center(_obj_A_bb)
        self.maxPosition = self._bounding_box_center(_obj_B_bb)

        _length = self._two_point_length(self.minPosition, self.maxPosition)
        return _length

    def _two_point_length(self, position_a, position_b):
        _x_value = position_a[0] - position_b[0]
        _y_value = position_a[1] - position_b[1]
        _Z_value = position_a[2] - position_b[2]

        return ((_x_value)**2 + (_y_value)**2 + (_Z_value)**2)**0.5

    def _get_component_length(self, _selection):
        _comp_A = _selection[0]
        _comp_B = _selection[1]

        vertexs_A = []
        vertexs_B = []
        self.minPosition = cmds.pointPosition(_comp_A, world=True)
        self.maxPosition = cmds.pointPosition(_comp_B, world=True)
        _length = self._two_point_length(self.minPosition, self.maxPosition)
        return _length


    def _change_option_menu(self, _select_unit):
        self._change_unit()
        
    def _check_distance_node(self, *args):
        _loc_sp = cmds.ls(self.distance_sp_name)
        _loc_ep = cmds.ls(self.distance_ep_name)

        if _loc_sp:
            self._loc_sp = _loc_sp[0]
        else:
            self._loc_sp = ""
        
        if _loc_ep:
            self._loc_ep = _loc_ep[0]
        else:
            self._loc_ep = ""
    
    def _make_custum_locator(self, _name):
        _locator = cmds.createNode("transform",
                                name=_name, skipSelect=True)

        _locator_shape = cmds.createNode("locator",
                                name="{}Shape".format(_name),
                                skipSelect=True, parent=_locator)

    def _make_distance_dimension_box(self, *args):
        
        _selection = cmds.ls(selection=True)
        _hilite = cmds.ls(hilite=True)
        
        bb_size = zip(*self.bb_size)

        _loc_sp1, _loc_ep1, _dist1 = self._make_distance(bb_size[0],
                                                [bb_size[0][0], bb_size[0][1], bb_size[1][2]])

        _loc_sp2, _loc_ep2, _dist2 = self._make_distance([bb_size[0][0], bb_size[0][1], bb_size[1][2]],
                                                [bb_size[1][0], bb_size[0][1], bb_size[1][2]])

        _loc_sp3, _loc_ep3, _dist3 = self._make_distance(bb_size[0],
                                                [bb_size[0][0], bb_size[1][1], bb_size[0][2]])

        _grp = cmds.group(name=self.distance_group_name, empty=True)
        cmds.parent(_loc_sp1, _loc_ep1, _dist1, _loc_sp2, _loc_ep2, _dist2, _loc_sp3, _loc_ep3, _dist3, _grp)
        
        if _selection:
            cmds.select(_selection, replace=True)
        if _hilite:
            cmds.hilite(_hilite)

    def _make_distance(self, min_positon, max_positon):
        _loc_sp = cmds.spaceLocator()
        cmds.move(min_positon[0], min_positon[1], min_positon[2])
        
        _loc_ep = cmds.spaceLocator()
        cmds.move(max_positon[0], max_positon[1], max_positon[2])
        
        _dist_shape = cmds.distanceDimension(startPoint=min_positon, endPoint=max_positon)
        _dist = cmds.listRelatives(_dist_shape, allParents=True)[0]
        return _loc_sp, _loc_ep, _dist


    def _make_distance_dimension(self, *args):
        
        _selection = cmds.ls(selection=True)
        _hilite = cmds.ls(hilite=True)
        
        _loc_sp, _loc_ep, _dist = self._make_distance(self.minPosition,self.maxPosition)

        _grp = cmds.group(name=self.distance_group_name, empty=True)
        cmds.parent(_loc_sp, _loc_ep, _dist, _grp)
        
        if _selection:
            cmds.select(_selection, replace=True)
        if _hilite:
            cmds.hilite(_hilite)

def main():
    proc = MeasuringPolyMesh()
    proc.create()

#main()