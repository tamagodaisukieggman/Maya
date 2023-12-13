# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from enum import Enum
from functools import partial

import maya.api.OpenMaya as om2
import maya.cmds as cmds


class MoveType(Enum):
    CENTER = 0
    BOTTOM = 1
    ORIGIN = 2


class SphericalNormal(object):
    def __init__(self):
        self.TITLE = u"Spherical Normal Tool"
        self.NAME = u"spherica_normal_tool_apiver_ui"
        self._window_width = 300
        self._window_height = 125

        self._locator_name = "_mtku_spherica_normal_center_locator"

        self._move_locator_to_center_btn = "{}_move_center_locator_btn".format(self.NAME)
        self._move_locator_to_bottom_btn = "{}_bottom_center_btn".format(self.NAME)
        self._move_locator_to_origin_btn = "{}_move_origin_btn".format(self.NAME)

        self._registration_mesh_btn = "{}_registration_mesh_btn".format(self.NAME)

        self._spherical_normal_btn = "{}_spherical_normal_btn".format(self.NAME)
        self._select_locator_btn = "{}_select_locator_btn".format(self.NAME)
        self._select_meshes_btn = "{}_select_meshes_btn".format(self.NAME)

        self._center_locator = None
        self._component_flag = False

        self._clear_memory()

    def create(self, visible=True):
        try:
            cmds.deleteUI(self.NAME)
        except:pass

        _separator_height = 15

        cmds.window(self.NAME,
                    title=self.TITLE,
                    width=self._window_width +2 ,
                    height=self._window_height + 2,
                    closeCommand=partial(self._delete_locator))

        cmds.menuBarLayout()
        cmds.menu(label="ヘルプ", helpMenu=True)
        cmds.menuItem(label="Spherical Normal ツールのヘルプ", image="help.png", command=self._show_help)

        cmds.columnLayout(adjustableColumn=True, width = self._window_width, height=self._window_height)

        cmds.text(label=u"メッシュ登録", backgroundColor=[0.1, 0.1, 0.1], height=_separator_height)
        cmds.button(self._registration_mesh_btn,
                    label=u"法線を編集するメッシュを登録",
                    width=self._window_width,
                    command=partial(self._registration_mesh))

        cmds.text(label=u"中心ロケータ移動", backgroundColor=[0.1, 0.1, 0.1], height=_separator_height)
        cmds.rowLayout(
                        adjustableColumn=1,
                        numberOfColumns=3,
                        columnWidth2=[self._window_width / 2,
                                        self._window_width / 2],
                        width=self._window_width)
        cmds.button(self._move_locator_to_center_btn,
                    label=u"登録メッシュの中心",
                    width=self._window_width / 2.5 - 5,
                    command=partial(self._move_locator, MoveType.CENTER))

        cmds.button(self._move_locator_to_bottom_btn,
                    label=u"登録メッシュの中心下限",
                    width=self._window_width / 2.5 - 5,
                    command=partial(self._move_locator, MoveType.BOTTOM))

        cmds.button(self._move_locator_to_origin_btn,
                    label=u"原点",
                    width=self._window_width / 5 - 5,
                    command=partial(self._move_locator, MoveType.ORIGIN))

        cmds.setParent("..")
        cmds.text(label=u"選択", backgroundColor=[0.1, 0.1, 0.1], height=_separator_height)
        cmds.rowLayout(adjustableColumn=1,
                        numberOfColumns=2,
                        columnWidth2=[self._window_width / 2,
                                        self._window_width / 2],
                        width=self._window_width)

        cmds.button(self._select_locator_btn,
                    label=u"中心ロケータ",
                    width=self._window_width / 2 - 5,
                    command=partial(self._select_locator))
        cmds.button(self._select_meshes_btn,
                    label=u"登録メッシュ",
                    width=self._window_width / 2 - 5,
                    command=partial(self._select_meshes))
        cmds.setParent("..")

        if visible is True:
            cmds.showWindow(self.NAME)

        self._reset_UI()
        cmds.scriptJob(parent=self.NAME, event=["SceneOpened", partial(self._reset_all)])

    def _reset_UI(self, *args):
        _loc_flag = False
        _dag_flag = False

        if self._dag_paths:
            _dag_flag = True

        if self._center_locator:
            _loc_flag = True

        if _dag_flag:
            cmds.button(self._select_meshes_btn, edit=True, enable=True)
        else:
            cmds.button(self._select_meshes_btn, edit=True, enable=False)

        if _loc_flag:
            cmds.button(self._select_locator_btn, edit=True, enable=True)
        else:
            cmds.button(self._select_locator_btn, edit=True, enable=False)

        if _loc_flag and _dag_flag:
            cmds.button(self._move_locator_to_center_btn, edit=True, enable=True)
            cmds.button(self._move_locator_to_bottom_btn, edit=True, enable=True)
            cmds.button(self._move_locator_to_origin_btn, edit=True, enable=True)
        else:
            cmds.button(self._move_locator_to_center_btn, edit=True, enable=False)
            cmds.button(self._move_locator_to_bottom_btn, edit=True, enable=False)
            cmds.button(self._move_locator_to_origin_btn, edit=True, enable=False)

    def _select_meshes(self, *args):
        if self._dag_paths and cmds.objExists(self._dag_paths[0]):
            cmds.select(self._dag_paths, r=True)
        else:
            cmds.warning(u"[ 登録されたメッシュ ]が見当たりません")
            cmds.button(self._select_meshes_btn, edit=True, enable=False)

    def _select_locator(self, *args):
        if not self._check_locator():
            return
        cmds.select(self._center_locator, r=True)

    def _reset_all(self, *args):
        self._clear_memory()
        self._delete_locator()
        self._reset_UI()

    def _check_memory(self, *args):
        return self._dag_paths

    def _clear_memory(self, *args):
        self._mesh_fns = []
        self._dag_paths = []
        self._component = dict()

    def _registration_mesh(self, *args):
        _meshs, _vtxs = self._get_selections()

        if not _vtxs and not _meshs:
            cmds.warning("Please Select Transform Node")

            return

        self._clear_memory()

        if _vtxs:
            self._get_meshfn_component(_vtxs)
        else:
            self._get_meshfn(_meshs)

    def _get_meshfn_component(self, _selection):

        selList = om2.MSelectionList()
        [selList.add(x) for x in _selection]

        for x in range(selList.length()):
            try:
                dag_path,mCmp = selList.getComponent(x)
            except:continue

            if dag_path.hasFn(om2.MFn.kMesh):
                _mesh_fns = om2.MFnMesh(dag_path)
                cmpType = None
                self._dag_paths.append(dag_path)
                self._mesh_fns.append(_mesh_fns)
                if mCmp.hasFn(om2.MFn.kMeshVertComponent):
                    cmpType = "vtx"

                if cmpType:
                    self._component[_mesh_fns] = om2.MFnSingleIndexedComponent(mCmp)

        if not self._component:
            cmds.warning("Plese Select Mesh Vertex")
            return

        cmds.select(cl=True)
        self._create_center_locator()
        self._move_locator(MoveType.CENTER)
        self._spherical_normal_component()
        self._reset_UI()

    def _get_meshfn(self, _selection):

        sel_list = om2.MSelectionList()
        [sel_list.add(x) for x in _selection]

        for i in range(sel_list.length()):
            dag_path = sel_list.getDagPath(i)
            if dag_path.hasFn(om2.MFn.kMesh):
                self._dag_paths.append(dag_path)
                self._mesh_fns.append(om2.MFnMesh(dag_path))

        cmds.select(cl=True)
        self._create_center_locator()
        self._move_locator(MoveType.CENTER)
        self._spherical_normal()
        self._reset_UI()

    def _delete_locator(self, *args):
        _locator = cmds.ls("*{}*".format(self._locator_name))
        if _locator:
            for _loc in _locator:
                try:
                    cmds.delete(_loc)
                except:
                    pass
        self._center_locator = None
        self._reset_UI()

    def _check_locator(self, *args):
        _flag = False
        if not self._center_locator:
            _center_locator = cmds.ls(self._locator_name, type="transform")
            if _center_locator:
                self._center_locator = _center_locator
                _flag = True
        else:
            _flag = True

        return _flag

    def _move_locator(self, move_type: MoveType, *args):
        if not self._check_locator():
            return
        if not self._dag_paths:
            return
        if not self._get_center():
            return
        cmds.select(self._center_locator, r=True)
        if move_type == MoveType.CENTER:
            cmds.move(self.bb_center[0], self.bb_center[1], self.bb_center[2],
                                    self._center_locator, worldSpace=True)
        elif move_type == MoveType.BOTTOM:
            cmds.move(self.bb_center[0], self.bb_bottom, self.bb_center[2],
                                    self._center_locator, worldSpace=True)
        elif move_type == MoveType.ORIGIN:
            cmds.move(0, 0, 0, self._center_locator, worldSpace=True)

    def _create_center_locator(self, *args):
        self._delete_locator()

        self._center_locator = cmds.createNode("transform",
                                name=self._locator_name, skipSelect=True)

        _locator_shape = cmds.createNode("locator",
                                name="{}Shape".format(self._locator_name),
                                skipSelect=True, parent=self._center_locator)

        cmds.setAttr("{}.overrideEnabled".format(_locator_shape), True)
        cmds.setAttr("{}.overrideColor".format(_locator_shape), 9)
        cmds.select(self._center_locator, r=True)

        if self._component_flag:
            cmds.scriptJob(parent=self.NAME,
                                attributeChange=["{}.translate".format(self._locator_name),
                                partial(self._spherical_normal_component)])
        else:
            cmds.scriptJob(parent=self.NAME,
                            attributeChange=["{}.translate".format(self._locator_name),
                            partial(self._spherical_normal)])
        cmds.setToolTo( 'moveSuperContext' )
        self._reset_UI()

    def _get_selections(self, *args):

        # 現在の選択
        _selections = cmds.ls(sl=True)

        # 選択トランスフォームノード
        _transform_nodes = cmds.ls(sl=True ,type="transform")

        _meshes = []

        # 選択トランスフォームノード以下に含まれるメッシュノードを取得
        for _transform_node in _transform_nodes:
            _mesh = cmds.listRelatives(_transform_node, allDescendents=True, fullPath=True, type="mesh")
            if _mesh:
                _meshes.extend(_mesh)

            _selections.remove(_transform_node)

        _vtx = cmds.polyListComponentConversion(_selections, tv=True)
        _vtx = cmds.filterExpand(_vtx, sm=31, ex=True)

        if len(_meshes):
            self._component_flag = False

        else:
            self._component_flag = True

        return _meshes, _vtx

    def _get_center(self, *args):
        self._bb = None
        self.bb_bottom = 0.0
        self.bb_center = [0.0, 0.0, 0.0]

        if self._component_flag:
            _selection = []
            for mesh_fn,_dag in zip(self._mesh_fns,self._dag_paths):
                _name = ["{}.vtx[{}]".format(_dag, x) for x in self._component[mesh_fn].getElements()]
                _selection.extend(cmds.ls(_name))
        else:
            _selection = cmds.ls(self._dag_paths)

        if not _selection:
            return False
        cmds.select(_selection, r=True)
        if self._component_flag:
            bb_size = cmds.polyEvaluate(_selection, boundingBoxComponent=True, accurateEvaluation=True)
        else:
            bb_size = cmds.polyEvaluate(_selection, boundingBox=True, accurateEvaluation=True)
        _p1 = om2.MPoint(bb_size[0][0], bb_size[1][0], bb_size[2][0])
        _p2 = om2.MPoint(bb_size[0][1], bb_size[1][1], bb_size[2][1])
        self._bb = om2.MBoundingBox(_p1, _p2)

        self.bb_center = self._bb.center
        self.bb_bottom = self.bb_center[1] - (self._bb.height / 2)
        return True

    def _spherical_normal_component(self, *args):
        _values = cmds.getAttr("{}.t".format(self._center_locator))[0]

        _center = om2.MFloatVector(_values[0], _values[1], _values[2])

        for mesh_fn,_dag in zip(self._mesh_fns,self._dag_paths):
            _component = self._component[mesh_fn]
            matrix = om2.MFloatMatrix(_dag.inclusiveMatrixInverse())
            _elements = _component.getElements()
            _positons = [mesh_fn.getPoint(x, om2.MSpace.kWorld) for x in _elements]
            _positons = [om2.MFloatVector(x[0],x[1],x[2]) for x in _positons]
            mesh_fn.setVertexNormals([(x-_center).transformAsNormal(matrix) for x in _positons], _elements)

    def _spherical_normal(self, *args):

        _values = cmds.getAttr("{}.t".format(self._center_locator))[0]

        _center = om2.MFloatVector(_values[0], _values[1], _values[2])

        for mesh_fn,_dag in zip(self._mesh_fns,self._dag_paths):

            matrix = om2.MFloatMatrix(_dag.inclusiveMatrixInverse())
            _positons = [om2.MFloatVector(x[0],x[1],x[2]) for x in mesh_fn.getPoints(om2.MSpace.kWorld)]

            mesh_fn.setVertexNormals([(x - _center).transformAsNormal(matrix) for x in _positons], range(mesh_fn.numVertices))

    def _show_help(self, *args):
        cmds.showHelp("https://wisdom.cygames.jp/pages/viewpage.action?pageId=604741864", absolute=True)


def main():
    proc = SphericalNormal()
    proc.create()
