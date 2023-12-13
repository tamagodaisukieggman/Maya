# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from functools import partial
import re
from collections import OrderedDict

import maya.cmds as cmds
import maya.api.OpenMaya as om2

from tatool.log import ToolLogging, Stage



TITLE = "UV Set Editor Plus"
NAME = "{}".format("_".join(TITLE.lower().split()))

project = "mutsunokami"

TOOL_NAME = "{} {}".format(project, TITLE)

tool_category = "Maya"

tool_version = 'v2021.10.04'
# UV のコピーペースト追加

# tool_version = 'v2021.07.13'


# 開発中はTrue、リリース時にFalse
DEV_MODE = True

# tool_logging = ToolLogging(
#                         projects=project,
#                         toolcategory=tool_category,
#                         target_stage=Stage.dev,
#                         tool_version=tool_version)

# if not DEV_MODE:
#     logger = tool_logging.getTemplateLogger(TOOL_NAME)
# else:
#     tool_logging = None
#     logger = None



def extract_num(_string, p, return_value=0):
    search = p.search(_string)
    if search:
        return int(search.groups()[0])
    else:
        return return_value

class UVSetChanger(object):

    def __init__(self):
        self.NAME = "uv_set_editor_plus_UI"
        self.TITLE = u"UV Set Editor Plus"
        self._rowcolumn_layout_name = "_{}_rowcolumn_layout".format(self.NAME)
        self._uv_set_scrolllist_name = "_{}_uv_set_scrolllist".format(self.NAME)
        self._uv_set_num_scrolllist_name = "_{}_uv_set_num_scrolllist".format(self.NAME)

        self._selections = None
        self._select_mesh_fn = []
        self._select_mesh_dagpath = []
        self._uv_sets_num_dict = None
        self.mesh_uv_values = OrderedDict()
        self.mesh_uv_ids = OrderedDict()

    def create(self):

        try:
            cmds.deleteUI(self.NAME)
        except:pass

        _list_left_width = 180
        _list_right_width = 80

        _button_width = (_list_left_width + _list_right_width) / 4

        cmds.window(self.NAME, title=self.TITLE,
                width=_list_left_width + _list_right_width, height=210)

        cmds.columnLayout(width=_list_left_width + _list_right_width + 16)

        cmds.rowLayout(numberOfColumns=2,
                        columnWidth2=[_list_left_width,
                                        _list_right_width],
                        width=_list_left_width + _list_right_width)

        cmds.text(label="UV Set Name", width=_list_left_width, backgroundColor=[0.1, 0.1, 0.1])
        cmds.text(label="count", width=_list_right_width, backgroundColor=[0.1, 0.1, 0.1])

        cmds.setParent('..')

        _scr = cmds.scrollLayout(width=_list_left_width + _list_right_width + 5,
                                height=210)

        cmds.setParent('..')

        _out = cmds.columnLayout(width=_list_left_width + _list_right_width)

        cmds.setParent(_scr)

        cmds.rowColumnLayout(self._rowcolumn_layout_name,
                            numberOfRows=1, rowHeight=[1, 500],
                            width=_list_left_width + _list_right_width
                            )

        cmds.textScrollList(self._uv_set_scrolllist_name,
                            width=_list_left_width, height=200,
                            selectCommand=partial(self.select_list),
                            doubleClickCommand=partial(self.open_rename_window),
                            ams=True)

        cmds.textScrollList(self._uv_set_num_scrolllist_name,
                            width=_list_right_width, height=200, ams=False, enable=False)
        cmds.popupMenu(parent = self._rowcolumn_layout_name, button=3)
        cmds.menuItem("Copy UVs", command=partial(self.copy_uv_value))
        cmds.menuItem("Paste UVs", command=partial(self.paste_uv_value))

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=4, columnWidth4=[_button_width,
                                                        _button_width,
                                                        _button_width,
                                                        _button_width],
                                                        width=_button_width * 4)

        cmds.button(label="New", width=_button_width, command=partial(self.create_uv_set))
        cmds.button(label="Rename", width=_button_width, command=partial(self.open_rename_window))
        cmds.button(label="Delete", width=_button_width, command=partial(self.delete_uv_set))
        cmds.button(label="Copy", width=_button_width, command=partial(self.copy_uv_set))

        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent(_out)

        cmds.showWindow(self.NAME)
        self.resize_scroll_list()
        self.refresh_list()
        cmds.scriptJob(parent=self.NAME, event=["SelectionChanged", partial(self.refresh_list)])


    def paste_uv_value(self, *args):
        if not self.mesh_uv_values:
            return

        if not self._select_mesh_fn:
            return

        _select_uvs = cmds.textScrollList(self._uv_set_scrolllist_name, q=True, selectItem=True)
        if not _select_uvs:
            return
        uv_name = _select_uvs[0]
        for dag_path, mesh_fn in zip(self._select_mesh_dagpath, self._select_mesh_fn):
            if uv_name not in mesh_fn.getUVSetNames():
                continue

            full_path_name = dag_path.fullPathName()
            if full_path_name in self.mesh_uv_values:
                u_values, v_values = self.mesh_uv_values[full_path_name]
                uv_counts, uv_ids = self.mesh_uv_ids[full_path_name]
                mesh_fn.setUVs(u_values, v_values, uv_name)
                mesh_fn.assignUVs(uv_counts, uv_ids, uv_name)
        cmds.refresh(currentView=True)

    def copy_uv_value(self, *args):
        if not self._select_mesh_fn:
            return

        _select_uvs = cmds.textScrollList(self._uv_set_scrolllist_name, q=True, selectItem=True)
        if not _select_uvs:
            return
        uv_name = _select_uvs[0]

        self.mesh_uv_values = OrderedDict()
        self.mesh_uv_ids = OrderedDict()

        for dag_path, mesh_fn in zip(self._select_mesh_dagpath, self._select_mesh_fn):
            if uv_name not in mesh_fn.getUVSetNames():
                continue
            u_values, v_values = mesh_fn.getUVs(uv_name)
            uv_counts, uv_ids = mesh_fn.getAssignedUVs(uv_name)
            self.mesh_uv_values[dag_path.fullPathName()] = [u_values, v_values]
            self.mesh_uv_ids[dag_path.fullPathName()] = [uv_counts, uv_ids]

    def copy_uv_set(self, *args):
        if not self._select_mesh_fn:
            return

        _select_uvs = cmds.textScrollList(self._uv_set_scrolllist_name, q=True, selectItem=True)
        if not _select_uvs:
            return
        for _node in self._select_mesh_dagpath:
            for _select_uv in _select_uvs:
                _uv_sets = cmds.polyUVSet(_node, q=True, allUVSets=True)
                if _uv_sets and _select_uv in _uv_sets:
                    cmds.polyUVSet(_node, copy=True, uvSet=_select_uv)

        self.refresh_list()

    def delete_uv_set(self, *args):
        if not self._select_mesh_fn:
            return
        _select_uvs = cmds.textScrollList(self._uv_set_scrolllist_name, q=True, selectItem=True)
        if not _select_uvs:
            return
        # _select_uv = _select_uv[0]
        _warning_flag = False

        for _select_uv in _select_uvs:
            if _select_uv != "map1":
                for _mesh_fn in self._select_mesh_fn:
                    _uv_sets = _mesh_fn.getUVSetNames()
                    if _uv_sets and _select_uv in _uv_sets:
                        _mesh_fn.deleteUVSet(_select_uv)
            else:
                _warning_flag = True

        if _warning_flag:
            cmds.warning(u"[ map1 ] は削除できません")
        self.refresh_list()

    def open_rename_window(self, *args):
        if not self._select_mesh_fn:
            return

        _select_uvs = cmds.textScrollList(self._uv_set_scrolllist_name, q=True, selectItem=True)
        if not _select_uvs:
            return
        _select_uv = _select_uvs[0]

        result = cmds.promptDialog(
                    title='Rename UV Set Name',
                    message='Enter Name:',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    text=_select_uv,
                    cancelButton='Cancel',
                    dismissString='Cancel')

        if result == 'OK':
            text = cmds.promptDialog(query=True, text=True)
            if text:
                self.rename_uv_set(_select_uv, text)

    def rename_uv_set(self, src_name=None, dst_name=None):
        for _mesh_fn in self._select_mesh_fn:
            _uv_sets = _mesh_fn.getUVSetNames()
            if _uv_sets:
                if dst_name in _uv_sets:
                    cmds.warning(u"[ {} ] はすでに存在します".format(dst_name))
                else:
                    if src_name in _uv_sets:
                        _mesh_fn.renameUVSet(src_name, dst_name)
        self.refresh_list()

    def create_uv_set(self, *args):
        if not self._select_mesh_fn:
            return
        for _mesh_fn in self._select_mesh_fn:
            _mesh_fn.createUVSet("")
        self.refresh_list()

    def change_uv_link(self, mesh = "", uv_sets = [], next_uv_id = 1):
        if not cmds.objExists(mesh):
            return
        for i, uv_set in enumerate(uv_sets):
            for _link in cmds.uvLink(q=True, uvSet="{}.uvSet[{}].uvSetName".format(mesh, i)):
                if _link:
                    # cmds.uvLink(make=True, uvSet="{}.uvSet[{}].uvSetName".format(mesh, next_uv_id), texture=_link)
                    cmds.uvLink(uvSet="{}.uvSet[{}].uvSetName".format(mesh, next_uv_id), texture=_link)

    def select_list(self, *args):
        if not self._select_mesh_fn:
            return

        _select_uvs = cmds.textScrollList(self._uv_set_scrolllist_name, q=True, selectItem=True)
        if not _select_uvs:
            return

        _select_uv = _select_uvs[0]

        for mesh_fn, dag_path in zip(self._select_mesh_fn, self._select_mesh_dagpath):
            _current_uv = cmds.polyUVSet(dag_path, q=True, cuv=True)
            _uv_set = mesh_fn.getUVSetNames()

            if _current_uv:
                _current_uv = _current_uv[0]
            else:
                continue

            if _current_uv in _uv_set and _select_uv in _uv_set:
                self.change_uv_link(dag_path, _uv_set, _uv_set.index(_select_uv))

            mesh_fn.setCurrentUVSetName(_select_uv)


    # def select_list_cmds(self, *args):
    #     if not self._selections:
    #         return
    #     _select_uvs = cmds.textScrollList(self._uv_set_scrolllist_name, q=True, selectItem=True)
    #     if not _select_uvs:
    #         return
    #     _select_uv = _select_uvs[0]
    #     for _node in self._selections:
    #         if cmds.objExists(_node):
    #             cmds.polyUVSet(_node, currentUVSet=True, uvSet=_select_uv)

    def remove_all_list(self, *args):
        cmds.textScrollList(self._uv_set_scrolllist_name, e=True, removeAll=True)
        cmds.textScrollList(self._uv_set_num_scrolllist_name, e=True, removeAll=True)

    def resize_scroll_list(self, uv_names=[]):
        if len(uv_names) < 15:
            cmds.rowColumnLayout(self._rowcolumn_layout_name, e=True, rowHeight=[1, 204])
        else:
            cmds.rowColumnLayout(self._rowcolumn_layout_name, e=True, rowHeight=[1, 13.5*len(uv_names)])

    def re_write_list(self, uv_names, _uv_sets_num_dict):
        [[cmds.textScrollList(self._uv_set_scrolllist_name, e=True, append=x),cmds.textScrollList(self._uv_set_num_scrolllist_name, e=True, append=_uv_sets_num_dict[x])] for x in uv_names]

    def get_selection(self, *args):
        self._select_mesh_fn = []
        self._select_mesh_dagpath = []
        _selection = cmds.ls(sl=True, type="transform", long=True)
        if not _selection:
            return
        _meshes = cmds.listRelatives(_selection, allDescendents=True, fullPath=True, type="mesh")
        if not _meshes:
            return
        _meshes = [x for x in _meshes if not cmds.getAttr("{}.intermediateObject".format(x))]

        if not _meshes:
            return
        selList = om2.MSelectionList()
        [selList.add(x) for x in _meshes]
        for x in range(selList.length()):
            dagPath = selList.getDagPath(x)
            # if dagPath.hasFn(om2.MFn.kMesh):
            self._select_mesh_dagpath.append(dagPath)
            self._select_mesh_fn.append(om2.MFnMesh(dagPath))
        self.get_uv_set_names()

    # def get_selection_cmds(self, *args):
    #     _selection = cmds.ls(sl=True, objectsOnly=True, long=True)

    #     if not _selection:
    #         _selection = cmds.ls(hilite=True, long=True)
    #         if not _selection:
    #             return
    #     self._selections = _selection
    #     self.get_uv_set_names()

    def get_uv_set_names(self, *args):
        _uv_sets_all = []
        _map1 = "map1"
        if not self._select_mesh_fn:
            return

        for mesh_fn in self._select_mesh_fn:
            _uv_set = mesh_fn.getUVSetNames()
            if _uv_set:
                _uv_sets_all.extend(_uv_set)

        if _uv_sets_all:

            p = re.compile(r'(\d+)')
            _uv_sets_all = sorted(list(set(_uv_sets_all)), key=lambda x: extract_num(x, p, float('inf')))
            if _map1 in _uv_sets_all:
                _uv_sets_all.remove(_map1)
                _uv_sets_all.insert(0, _map1)
            _uv_sets_num_dict = dict([x,0] for x in _uv_sets_all)

            for mesh_fn in self._select_mesh_fn:
                _uv_sets = mesh_fn.getUVSetNames()
                for _uv_set in _uv_sets:
                    if _uv_set in _uv_sets_num_dict.keys():
                        _uv_sets_num_dict[_uv_set] = _uv_sets_num_dict[_uv_set] + 1

            self.resize_scroll_list(_uv_sets_all)
            self.re_write_list(_uv_sets_all, _uv_sets_num_dict)

    def get_uv_set_names_cmds(self, *args):
        _uv_sets = []

        for _node in self._selections:
            _uv_set = cmds.polyUVSet(_node, q=True, allUVSets=True)
            if _uv_set:
                _uv_sets.extend(_uv_set)
        if _uv_sets:
            p = re.compile(r'(\d+)')
            _uv_sets = sorted(list(set(_uv_sets)), key=lambda x: extract_num(x, p, float('inf')))
            _uv_sets_num_dict = dict([x,0] for x in _uv_sets)

            for _node in self._selections:
                _uv_set = cmds.polyUVSet(_node, q=True, allUVSets=True)
                if _uv_set in _uv_sets:
                    _uv_sets_num_dict[_uv_set] = _uv_sets_num_dict[_uv_set] + 1

            self.resize_scroll_list(_uv_sets)
            self.re_write_list(_uv_sets, _uv_sets_num_dict)

    def refresh_list(self, *args):

        self.remove_all_list()
        self.get_selection()


def main():
    uvsc = UVSetChanger()
    uvsc.create()
    if not DEV_MODE and logger:
        logger.send_launch(u'ツール起動')
